"""Qualify and observe a pinned, reset-only CF001 bootstrap.

The native debugger stops at Xemu's existing pre-opcode breakpoint path.
Only the three monitor controls are writable. All guest and firmware state is
read directly so reading CIA status does not acknowledge a pending interrupt.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import linked_admission
import service_admission
import stack_admission
import startup_check


PRG_SHA = '0e81aa0e2f1440fc12bbd8530afac0c8d98b7f638f0f603a4d60b2af318f79cb'
IMAGE_BASE = 0x100000000
# Offsets in the hash-pinned x86_64 Mach-O. Each has a RIP-relative
# operand or control-flow anchor in the static report.
INJECT = 0x28830
PRE_OPCODE = 0x4615
POST_BREAK_JUMP = 0x4660
UPDATE_EMULATOR = 0x4e80
BREAKPOINT_PC = 0xe553c
STEP_CYCLES = 0xe5560
PAUSED = 0xec400
CPU = 0xa79f18
CIA1 = 0x138340
CIA2 = 0x122190
RAM = 0x9e1a90
HICKUP = 0x11e170
MAP = 0x9e1a7c
CPU_PORT = 0xfc4a4
IO_MODE = 0x9e1a61
VIC = 0xa69a90
D6 = 0x9e1700
D7 = 0x93f960
ROM_PROTECT = 0xfc8c8
IN_HYPERVISOR = 0xa79f61
IN_DMA = 0x9e0110
CPU_READ_ADDRESS = 0xa7afe0


def sha(data):
    return hashlib.sha256(data).hexdigest()


def static(packet, references):
    prg = (packet / 'BOOT-ONLY.prg').read_bytes()
    if sha(prg) != PRG_SHA:
        raise ValueError('restricted PRG hash changed')
    dis = (packet / 'BOOT-ONLY.disassembly').read_text()
    sym = (packet / 'BOOT-ONLY.symbols').read_text()
    ins, names = stack_admission.parse(dis, sym)
    graph = stack_admission.Graph(ins, stack_admission.stack_effects(ins, names))
    graph.walk(names['__do_init_stack'])
    end = names['__m2re_noinit_end']
    terminal = names['main'] + 16
    if (ins[terminal] != ('bra', f'${terminal:x}', b'\x80\xfe')
        or ins[terminal - 3][:2] != ('sty', f"${names['m2_boot_outcome']:x}")):
        raise ValueError('restricted outcome/terminal path changed')
    forbidden = [name for name, address in names.items() if address in graph.reachable
                 and name.startswith(('cfclock', 'm1_tick', 'm2rb_dispatch', 'm2rb_platform_init',
                                      'r0f_pf_start_irq', 'cfrom_restore', 'cfaudio', 'cfdma'))]
    if forbidden or {address for address in graph.reachable
                     if ins[address][:2] == ('sta', '$d640')} != {names['r0fc_rom_toggle'] + 9}:
        raise ValueError('unsafe linked closure or unexpected trap site')
    # Report the linked BASIC dialect/SYS form before relying on the debugger
    # pre-opcode stop at the entry PC.
    header = linked_admission.image_bytes(prg, 0x2001, names['_start'] - 0x2001)
    entry = re.fullmatch(rb'\x0a\x20\x0a\x00\xfe\x02 0\x00\x15\x20\x14\x00\x9e (\d+)\x00\x00\x00', header)
    if entry is None or int(entry[1]) != names['_start']:
        raise ValueError('BASIC SYS destination changed')
    load = linked_admission.check_load(prg, (packet / 'BOOT-ONLY.prg.elf').read_bytes(),
                                       {'resident_end': end, 'resident_bytes': end - 0x2001})
    trap = service_admission.trap_check(prg, names, references)
    return {
        'status': 'PASS with required pre-opcode debugger checks', 'PRG_sha256': PRG_SHA,
        'scope': 'isolated reset-only CF001 trace; no reachable clock, Graphics or simulation service',
        'load': load, 'prefix': startup_check.check(dis, sym, prg),
        'initialization': linked_admission.check_initialization(prg, dis, sym),
        'map': linked_admission.check_application_mapping(dis, sym),
        'stack': stack_admission.check(dis, sym), 'terminal': terminal,
        'cf001': trap,
        'checkpoints': {'sys': names['_start'], 'canonical': names['m2re_startup_done'],
                        'pre_trap': names['r0fc_rom_toggle'] + 9, 'privileged': 0x8000,
                        'return': names['r0fc_rom_toggle'] + 12, 'terminal': terminal},
        'symbols': {name: names[name] for name in ('m2_boot_outcome', 'cffault', 'cfreclaimed', 'r0f_pf_nmi_seen')},
        'startup_stop_basis': 'host stop in PRG injection before memcpy; arm the exact SYS address and one-opcode mode. Validate before each guest continuation.',
    }


class Observer:
    def __init__(self, debugger, config, report):
        import lldb
        self.lldb = lldb
        self.debugger = debugger
        self.config = config
        self.report = report
        self.process = None

    def wait(self, prior):
        end = time.monotonic() + 90
        while time.monotonic() < end:
            state = self.process.GetState()
            if state == self.lldb.eStateStopped and self.process.GetStopID() > prior:
                return self.process.GetSelectedThread().GetFrameAtIndex(0).GetPC()
            if state in (self.lldb.eStateExited, self.lldb.eStateCrashed, self.lldb.eStateDetached):
                raise RuntimeError(f'debuggee stopped before planned milestone: state {state}, exit {self.process.GetExitStatus()}')
            time.sleep(0.01)
        raise RuntimeError('debuggee did not reach the planned stop within 90 seconds')

    def read(self, offset, count):
        error = self.lldb.SBError()
        data = self.process.ReadMemory(self.base + offset, count, error)
        if error.Fail() or len(data) != count:
            raise RuntimeError(f'cannot read pinned process offset {offset:#x}: {error}')
        return data

    def value(self, offset, count=1):
        return int.from_bytes(self.read(offset, count), 'little')

    def arm(self, guest_pc):
        # These are the UART monitor's breakpoint, single-step and pause
        # controls. No emulator CPU register or guest memory is written.
        for offset, value in ((BREAKPOINT_PC, guest_pc), (STEP_CYCLES, 0), (PAUSED, 0)):
            error = self.lldb.SBError()
            if self.process.WriteMemory(self.base + offset, struct.pack('<I', value), error) != 4 or error.Fail():
                raise RuntimeError('cannot set pinned monitor control')
            if self.value(offset, 4) != value:
                raise RuntimeError('pinned monitor control readback failed')

    def snapshot(self, name, pc):
        cpu = self.read(CPU, 72)
        status = struct.unpack_from('<4I', cpu, 36)
        flags = {'E': bool(cpu[28]), 'N': bool(cpu[32] & 128), 'Z': bool(cpu[32] & 2),
                 **{key: bool(value) for key, value in zip('CVDI', status)}}
        row = {'name': name, 'pc': int.from_bytes(cpu[52:54], 'little'),
               'previous_pc': int.from_bytes(cpu[54:56], 'little'),
               'axyz': list(cpu[:3]) + [cpu[16]], 'base_page': cpu[19],
               'hardware_sp': (cpu[21] << 8) | cpu[3], 'flags': flags,
               'software_sp': self.value(RAM + 0x202, 2),
               'irq_level': int.from_bytes(cpu[60:64], 'little'),
               'nmi_edge': int.from_bytes(cpu[64:68], 'little'),
               'cia1_icr_mask_data': list(self.read(CIA1 + 0x56, 2)),
               'cia2_icr_mask_data': list(self.read(CIA2 + 0x56, 2)),
               'map_hi_mb_lo_mb_hi_offset_lo_offset_mask': list(struct.unpack('<4IB', self.read(MAP, 17))),
               'cpu_port_ddr_data': list(self.read(CPU_PORT, 2)), 'io_mode': self.value(IO_MODE),
               'd030': self.value(VIC + 0x30), 'video_6f': self.value(VIC + 0x6f),
               'cartridge_fb_fd': [self.value(D7 + reg) for reg in (0xfb, 0xfd)],
               'd67d': self.value(D6 + 0x7d), 'rom_protection': self.value(ROM_PROTECT),
               'privileged': bool(self.value(IN_HYPERVISOR)), 'dma': bool(self.value(IN_DMA)),
               'hardware_stack_sha256': sha(self.read(RAM + 0x100, 0x100)),
               'fetch_page_base': self.value(CPU_READ_ADDRESS + (pc >> 8) * 4, 4)}
        if row['pc'] != pc or row['dma'] or self.value(BREAKPOINT_PC, 4) != pc or self.value(STEP_CYCLES, 4) != 0:
            raise RuntimeError(f'{name}: pre-opcode breakpoint or single-step state differs')
        return row

    def check(self, row, admission, prg):
        name = row['name']
        flags = row['flags']
        rom_expected = admission['cf001']['emulator_rom_and_sdl']['rom']['sha256']
        if row['nmi_edge'] or row['cia2_icr_mask_data'][0] & 31 or (row['irq_level'] and not flags['I']):
            raise RuntimeError(f'{name}: asynchronous interrupt could enter the restricted path')
        if row['privileged'] != (name == 'privileged'):
            raise RuntimeError(f'{name}: unexpected privileged mode')
        origin = admission['load']['origin']
        if self.read(RAM + origin, len(prg) - 2) != prg[2:]:
            raise RuntimeError(f'{name}: physical PRG payload differs')
        row['resident_sha256'] = sha(self.read(RAM + origin, admission['load']['resident_end'] - origin))
        standard = self.config['standard']
        if bool(row['video_6f'] & 128) != (standard == 'NTSC'):
            raise RuntimeError('live VIC standard differs from requested trace')
        if name == 'sys':
            # The first 32 KiB normal policy is identity. MAP also preserves
            # this entry when its selected low megabyte AND offset sum to zero.
            # The slot table can still hold the lazy resolver sentinel.
            _, lo_mb, _, lo_offset, mask = row['map_hi_mb_lo_mb_hi_offset_lo_offset_mask']
            pc = row['pc']
            physical = pc + (lo_mb + lo_offset if mask & (1 << (pc >> 13)) else 0)
            row['derived_sys_physical_fetch'] = physical
            if physical != pc or row['fetch_page_base'] not in (pc & 0xff00, 0x20000000):
                raise RuntimeError('SYS fetch does not resolve to the loaded bank-zero bytes')
            return
        if name != 'privileged':
            if (row['map_hi_mb_lo_mb_hi_offset_lo_offset_mask'] != [0, 0, 0, 0, 0]
                or row['base_page'] != 2 or row['hardware_sp'] >> 8 != 1
                or row['cpu_port_ddr_data'] != [0x2f, 0x35] or row['io_mode'] != 3
                or row['d030'] & 0xb9 or not flags['E'] or not flags['I'] or flags['D']
                or row['cartridge_fb_fd'][0] & 2 or row['cartridge_fb_fd'][1] & 0xc0 != 0xc0):
                raise RuntimeError(f'{name}: canonical application context differs')
        if name in ('pre_trap', 'privileged', 'return'):
            firmware = self.read(HICKUP, 0x4000)
            row['live_hickup_sha256'] = sha(firmware)
            row['physical_rom_sha256'] = sha(self.read(RAM + 0x20000, 0x20000))
            if row['physical_rom_sha256'] != rom_expected:
                raise RuntimeError(f'{name}: physical ROM differs from pinned input')
            for address, expected in admission['cf001']['raw_trap_slices_by_address'].items():
                offset = int(address, 16) - 0x8000
                data = bytes.fromhex(expected)
                if firmware[offset:offset + len(data)] != data:
                    raise RuntimeError(f'{name}: live privileged instruction path differs at ${address}')
            row['live_cf001_slices_match'] = True
        if name == 'pre_trap' and (row['axyz'][0] != 0x70 or not row['rom_protection'] or not row['d67d'] & 4):
            raise RuntimeError('CF001 selector or pre-trap ROM protection differs')
        if name == 'privileged':
            row['saved_context_d640_d658'] = self.read(D6 + 0x40, 25).hex()
            if row['base_page'] != 0xbf or row['hardware_sp'] != 0xbeff or not flags['I']:
                raise RuntimeError('CF001 private base or stack differs')
        if name == 'return':
            before = next(stage for stage in self.report['stops'] if stage['name'] == 'pre_trap')
            for key in ('hardware_sp', 'software_sp', 'hardware_stack_sha256', 'resident_sha256',
                        'cpu_port_ddr_data', 'io_mode', 'd030', 'cartridge_fb_fd'):
                if row[key] != before[key]:
                    raise RuntimeError('CF001 return changed ' + key)
            if (row['rom_protection'] or row['d67d'] != before['d67d'] ^ 4
                or row['axyz'][0] != row['d67d'] or row['axyz'][1:] != before['axyz'][1:] or not flags['C']):
                raise RuntimeError('CF001 return result differs')
        if name == 'terminal':
            row['terminal_state'] = {key: self.value(RAM + address) for key, address in admission['symbols'].items()}
            if row['terminal_state'] != {'m2_boot_outcome': 1, 'cffault': 0, 'cfreclaimed': 1, 'r0f_pf_nmi_seen': 0}:
                raise RuntimeError('restricted bootstrap reached terminal fault')

    def run(self, admission, prg):
        config = self.config
        self.debugger.SetAsync(True)
        target = self.debugger.CreateTarget(config['executable'])
        module = target.GetModuleAtIndex(0)
        for offset in (INJECT, PRE_OPCODE):
            bp = target.BreakpointCreateBySBAddress(module.ResolveFileAddress(IMAGE_BASE + offset))
            if bp.GetNumLocations() != 1:
                raise RuntimeError('pinned host breakpoint could not be resolved')
        launch = self.lldb.SBLaunchInfo(config['arguments'])
        launch.SetWorkingDirectory(config['working_directory'])
        launch.SetEnvironmentEntries(config['environment'], False)
        launch.SetLaunchFlags(self.lldb.eLaunchFlagDebug)
        launch.AddOpenFileAction(1, config['stdout'], False, True)
        launch.AddOpenFileAction(2, config['stderr'], False, True)
        error = self.lldb.SBError()
        self.process = target.Launch(launch, error)
        if error.Fail() or not self.process.IsValid():
            raise RuntimeError(f'cannot launch pinned debugger child: {error}')
        first = self.wait(0)
        self.base = module.GetObjectFileHeaderAddress().GetLoadAddress(target)
        if first != self.base + INJECT:
            raise RuntimeError('first host stop was not the pre-copy injection callback')
        self.report['injection_stop'] = hex(first - self.base)
        prefix_event_fence = None
        for name in ('sys', 'canonical', 'pre_trap', 'privileged', 'return', 'terminal'):
            pc = admission['checkpoints'][name]
            prior = self.process.GetStopID()
            self.arm(pc)
            error = self.process.Continue()
            if error.Fail():
                raise RuntimeError(f'{name}: cannot resume debugger child: {error}')
            stopped = self.wait(prior)
            thread = self.process.GetSelectedThread()
            previous = self.report['stops'][-1]['pc'] if self.report['stops'] else None
            # Rosetta LLDB may expose the native single-step over the existing
            # breakpoint's JMP. This position is still before cpu65_step.
            if (stopped == self.base + POST_BREAK_JUMP and thread.GetStopReason() == self.lldb.eStopReasonTrace
                and self.value(CPU + 52, 2) == previous and self.value(BREAKPOINT_PC, 4) == pc
                and self.value(STEP_CYCLES, 4) == 0 and self.value(PAUSED, 4) == 0):
                self.report.setdefault('native_breakpoint_steps', []).append(name)
                prior = self.process.GetStopID()
                error = self.process.Continue()
                if error.Fail():
                    raise RuntimeError(f'{name}: cannot finish native breakpoint step: {error}')
                stopped = self.wait(prior)
            if stopped != self.base + PRE_OPCODE:
                raise RuntimeError(f'{name}: unexpected host stop at image offset {stopped - self.base:#x}')
            row = self.snapshot(name, pc)
            self.report['stops'].append(row)
            self.check(row, admission, prg)
            if name == 'sys':
                # Until the early vectors are installed, abort before any host
                # input pump can post RESTORE. CIA2 is masked and no edge is pending.
                prefix_event_fence = target.BreakpointCreateBySBAddress(
                    module.ResolveFileAddress(IMAGE_BASE + UPDATE_EMULATOR))
                if prefix_event_fence.GetNumLocations() != 1:
                    raise RuntimeError('host input fence could not be resolved')
            if name == 'canonical':
                target.BreakpointDelete(prefix_event_fence.GetID())
                self.report['pre_vector_host_input_fence'] = 'PASS; no input pump between SYS and canonical state'
        self.report['status'] = 'PASS at the restricted Xemu diagnostic tier'


def observe(debugger, command, _result, _internal):
    config = json.loads(Path(command).read_text())
    output = Path(config['result'])
    if output.exists():
        raise ValueError('boot trace capture already exists')
    admission = json.loads(Path(config['static']).read_text())
    prg = Path(config['prg']).read_bytes()
    report = {'status': 'FAIL', 'standard': config['standard'], 'stops': [], 'rendering_executed': False}
    observer = Observer(debugger, config, report)
    try:
        if (sha(prg) != PRG_SHA or admission['PRG_sha256'] != PRG_SHA
            or sha(Path(config['executable']).read_bytes()) != admission['cf001']['emulator_rom_and_sdl']['xemu']['sha256']):
            raise ValueError('static and live diagnostic identities differ')
        observer.run(admission, prg)
    except Exception as error:
        report['failure'] = str(error)
    finally:
        if observer.process and observer.process.IsValid():
            observer.process.Kill()
        with output.open('x') as stream:
            stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('standard', 'status')} | {'failure': report.get('failure')}))


def __lldb_init_module(debugger, _internal):
    debugger.HandleCommand('command script add -f boot_trace.observe f65-boot-observe')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--references', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(static(args.packet, args.references), indent=2))
