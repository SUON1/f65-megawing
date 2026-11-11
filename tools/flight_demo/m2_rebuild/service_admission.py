"""Replay static qualification of the exact sealed M2 SERVICE1 image."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile

import linked_admission
import service_costs
import stack_admission
import startup_check

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'docs/evidence/flight-demo/2026-10-30-m2-extended-resident'
XEMU_COMMIT = '40dfef0d1d5f56be2469492715c12bdb32c75b67'
HICKUP_SHA = '21f5b58549c61a886bfcdd4e73e3200b2c36790b8ba21ad6bbdaa59fefb8e7a4'
CHECKPOINT = '53ea27cbcd145be625c6e6602eac1f232e41b0cc'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}


def verify_seal(path):
    members = json.loads(path.read_text())
    for name, expected in members.items():
        if identity(path.parent / name) != expected:
            raise ValueError('sealed evidence changed: ' + name)
    return {'members': len(members), 'sha256': sha(path.read_bytes())}


def trap_check(prg, names, references):
    # Compare the independently fetched primary sources with the exact Git
    # objects before reading the emulator's built-in HICKUP array.
    git = ['git', '-C', str(references)]
    if subprocess.check_output([*git, 'rev-parse', 'HEAD'], text=True).strip() != XEMU_COMMIT:
        raise ValueError('Xemu source commit changed')
    source_ids = {}
    files = ['targets/mega65/' + name + '.c' for name in
             ('hypervisor', 'inject', 'io_mapper', 'memory_mapper', 'memcontent', 'mega65', 'sdcard')]
    for name in [*files, 'xemu/cpu65.c', 'xemu/cpu65_mega65_timings.h']:
        path = references / name
        expected = subprocess.check_output([*git, 'show', XEMU_COMMIT + ':' + name])
        if path.read_bytes() != expected:
            raise ValueError('Xemu source bytes changed: ' + name)
        source_ids[name] = identity(path)
    expected = json.loads((OLD / 'emulator-identities.json').read_text())['artifacts']
    emulator = {name: identity(Path(row['path'])) for name, row in expected.items()}
    if any(emulator[name]['sha256'] != row['sha256'] for name, row in expected.items()):
        raise ValueError('pinned Xemu, ROM or SDL identity changed')
    source = (references / 'targets/mega65/memcontent.c').read_text()
    array = re.search(r'meminitdata_hickup\[MEMINITDATA_HICKUP_SIZE\]\s*=\s*\{([^}]+)\}', source)[1]
    firmware = bytes(int(value, 16) for value in re.findall(r'0x([0-9a-fA-F]{2})\b', array))
    image = Path(expected['xemu']['path']).read_bytes()
    offset = image.find(firmware)
    if len(firmware) != 16384 or sha(firmware) != HICKUP_SHA or offset != 631104:
        raise ValueError('built-in HICKUP does not match the pinned executable')
    # Known closed path only. Verify dispatch index, private JSR/RTS, all
    # writes and the leave instruction against the binary's firmware bytes.
    slices = {
        0x8000: '4c048cea',                     # trap 0 vector
        0x8c04: '78d8297eaa7c0c8c',             # SEI; CLD; mask A and jump indexed
        0x8c7c: 'c38c',                         # $8c0c + ($70 & $7e)
        0x8cc3: 'ad7dd649048d7dd68d40d64c1682', # ROM protect, saved A, then return path
        0x8216: '2024a2ad47d609018d47d68d7fd6', # private call, saved carry, leave
        0xa224: '48a9828d80d6683860',           # buffer unmap; no medium I/O
    }
    for at, expected_bytes in slices.items():
        data = bytes.fromhex(expected_bytes)
        if firmware[at - 0x8000:at - 0x8000 + len(data)] != data:
            raise ValueError('built-in HICKUP trap path changed')
    wrapper = names['r0fc_rom_toggle']
    if linked_admission.image_bytes(prg, wrapper, 13) != bytes.fromhex('0878da5adb7b48a9708d40d6ea'):
        raise ValueError('application trap number/selector/wrapper changed')
    return {
        'status': 'PASS for this static built-in selector path, conditional on fresh session identity',
        'xemu_commit': XEMU_COMMIT, 'xemu_inputs': source_ids, 'emulator_rom_and_sdl': emulator,
        'built_in_hickup': {'bytes': len(firmware), 'sha256': HICKUP_SHA, 'file_offset': offset},
        'raw_trap_slices_by_address': {f'{address:04x}': data for address, data in slices.items()},
        'user_trap_pc': wrapper + 9, 'return_pc': wrapper + 12,
        'entry_conditions': ['VIC-IV I/O visible, canonical zero MAP/mask/megabytes and B=$02',
                             'CPU DDR/data $2f/$35, E=1 page-one stack, D=0 and IRQ masked',
                             'ROM overlays and cartridge lines disabled; no cartridge or firmware override',
                             'no queued Hypervisor trap, fresh ROM and no pre-vector pending NMI'],
        'privileged_execution': 'trap 0 A=$70; private $8000-$bfff, B=$bf, SP=$beff; no IRQ/NMI entry while privileged',
        'privileged_hardware_stack_peak_bytes': 3, 'privileged_software_stack_bytes': 0,
        'privileged_write_addresses': ['D67D', 'D640', 'D680', 'D647', 'D67F'],
        'D680_82': 'clear buffer mapping/error state only; no medium command or data transfer',
        'restoration': 'Xemu restores saved PC, MAP masks/MB/offsets, B, stack page/SP, E/I/D/P, I/O mode and CPU ports. VIC D030 and cartridge state are untouched by the traced firmware. User A and carry are deliberate results; the app wrapper restores saved P/X/Y/Z/B.',
        'resident_integrity': 'no user-RAM store; private stack writes and saved registers do not alias resident or software SP',
        'failure': 'CF001 rejects bad carry, B or ROM-protect result before the clock/ticks. Other return invariants rely on the pinned firmware and entry conditions. A late NMI latches terminal fault.',
        'unproven': 'actual pre-SYS MAP/NMI state, identity of running HICKUP after boot/upgrade, return visibility and external NMI arrival envelope on fresh PAL and NTSC',
    }


def qualify(packet, host, references):
    result = json.loads((packet / 'result.json').read_text())
    if result['head'] != CHECKPOINT or result['execution_admitted'] or result['reserve_used'] != 0:
        raise ValueError('target provenance or admission identity differs')
    target_seal = verify_seal(packet / 'seal.json')
    host_seal = verify_seal(host / 'seal.json')
    for path, digest in result['inputs'].items():
        if sha((ROOT / path).read_bytes()) != digest:
            raise ValueError('linked source input changed: ' + path)
    with tarfile.open(packet / 'source.tar.gz', 'r:gz') as archive:
        if set(archive.getnames()) != result['inputs'].keys():
            raise ValueError('source archive inventory differs')
        for path, digest in result['inputs'].items():
            if sha(archive.extractfile(path).read()) != digest:
                raise ValueError('source archive bytes differ: ' + path)
    link_map = result['link_map']
    if sha(gzip.decompress((packet / link_map['file']).read_bytes())) != link_map['raw_sha256']:
        raise ValueError('lossless raw linker map identity changed')
    prg = (packet / 'UNADMITTED.prg').read_bytes()
    elf = (packet / 'UNADMITTED.prg.elf').read_bytes()
    dis = (packet / 'UNADMITTED.disassembly').read_text()
    sym = (packet / 'UNADMITTED.symbols').read_text()
    ins, names = stack_admission.parse(dis, sym)
    header = linked_admission.image_bytes(prg, 0x2001, names['_start'] - 0x2001)
    # Follow the two linked BASIC lines through the SYS token and decimal PC.
    entry = re.fullmatch(rb'\x0a\x20\x0a\x00\xfe\x02 0\x00\x15\x20\x14\x00\x9e (\d+)\x00\x00\x00', header)
    if entry is None or int(entry[1]) != names['_start']:
        raise ValueError('BASIC RUN/SYS entry does not select the linked canonical prefix')
    handlers = stack_admission.Graph(ins)
    for handler in ('r0f_pf_irq', 'r0f_pf_nmi'):
        handlers.walk(names[handler], mode='interrupt')
    writes = {operand for address in handlers.reachable
              for op, operand, _ in [ins[address]] if op in stack_admission.WRITES}
    expected = {'$d019'} | {f'${names[name]:x}' for name in
                             ('r0f_pf_irq_count', 'r0f_pf_irq_seq', 'r0f_pf_irq_seen', 'r0f_pf_nmi_seen')}
    expected.add(f"${names['r0f_pf_irq_count'] + 1:x}")
    if writes != expected or handlers.call_edges:
        raise ValueError('interrupt writer closure changed')
    report = {
        'identity': result['identity'], 'checkpoint': CHECKPOINT, 'target': target_seal,
        'host': host_seal, 'target_prg_sha256': sha(prg), 'source_members': len(result['inputs']),
        'basic_run_sys_entry': names['_start'],
        'load': linked_admission.check_load(prg, elf, result),
        'startup_prefix': startup_check.check(dis, sym, prg),
        'initialization': linked_admission.check_initialization(prg, dis, sym),
        'application_mapping': linked_admission.check_application_mapping(dis, sym),
        'application_stack': stack_admission.check(dis, sym),
        'cf001_trap': trap_check(prg, names, references),
        'interrupt_writes': sorted(writes),
        'async_camera_generation_writer': False,
        'writer_scope': 'main is the only caller of camera edges and renderer dispatch; handlers only touch the addresses above; CF001 occurs during startup and runtime has no DMA submission',
        'service': service_costs.measure(prg, dis, sym,
            (references / 'xemu/cpu65_mega65_timings.h').read_bytes(), (host / 'host.txt').read_text()),
        'target_executed': False, 'xemu': 'NOT RUN', 'runtime_admission': 'BLOCKED',
        'programs': {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in
                     (Path(__file__), Path(service_costs.__file__), Path(linked_admission.__file__),
                      Path(stack_admission.__file__), Path(startup_check.__file__))},
    }
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--references', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(qualify(args.packet, args.host, args.references), indent=2))
    # This command verifies the evidence and signals non-admission separately.
    sys.exit(1)
