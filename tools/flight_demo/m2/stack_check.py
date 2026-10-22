"""Bound hardware stack on the linked PR1 probe's direct-control-flow graph.

Reject unknown transfers, unequal join depths, recursion and unbalanced returns.
This is a compile-time bound, not target execution or interrupt-stack evidence.
"""
import re


def check(disassembly):
    instructions = {}
    names = {}
    for line in disassembly.splitlines():
        label = re.match(r'^([0-9a-f]+) <([^>]+)>:', line)
        if label:
            names[label[2]] = int(label[1], 16)
        match = re.match(r'^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2} )+\s*(\w+)\s*(.*)$', line)
        if match:
            instructions[int(match[1], 16)] = (match[2], match[3].split(';')[0].strip())
    addresses = sorted(instructions)
    following = dict(zip(addresses, addresses[1:]))
    branches = {'bcc', 'bcs', 'beq', 'bne', 'bmi', 'bpl', 'bvc', 'bvs'}
    pushes = {'pha', 'phx', 'phy', 'phz', 'php'}
    pulls = {'pla', 'plx', 'ply', 'plz', 'plp'}
    # BIT and CLV change flags, not stacks; both branch successors stay checked.
    ordinary = set('adc and asl bit clc cli clv cmp cpx cpy dec dew dex dey eor inc inw inx iny lda ldx ldy lsr ora rol ror sbc sec sei sta stx sty stz tax tay txa tya'.split())
    # Admit only the compiler's explicit, constant 16-bit SP adjustment.
    # Every other SP write remains a hard failure, including indexed writes.
    software_effect = {}
    admitted_writes = set()
    for i, address in enumerate(addresses):
        window = addresses[i:i+7]
        if len(window) != 7:
            continue
        ops = [instructions[a] for a in window]
        if (ops[0] == ('clc', '') and ops[1] == ('lda', '$2')
            and ops[3] == ('sta', '$2') and ops[4] == ('lda', '$3')
            and ops[6] == ('sta', '$3') and ops[2][0] == ops[5][0] == 'adc'):
            lo = re.fullmatch(r'#\$([0-9a-f]{1,2})', ops[2][1])
            hi = re.fullmatch(r'#\$([0-9a-f]{1,2})', ops[5][1])
            if lo and hi:
                adjustment = int(lo[1], 16) + 256 * int(hi[1], 16)
                if adjustment >= 32768:
                    adjustment -= 65536
                software_effect[window[6]] = -adjustment
                admitted_writes.update((window[3], window[6]))
    init = names.get('__do_init_stack')
    if init is not None:
        offset = addresses.index(init)
        window = addresses[offset:offset+4]
        if [instructions[a] for a in window] == [
            ('lda', '#$0'), ('sta', '$2'), ('lda', '#$d0'), ('sta', '$3')]:
            admitted_writes.update((window[1], window[3]))
    writes = {address for address, (op, operand) in instructions.items()
              if op in {'sta', 'stx', 'sty', 'stz', 'inc', 'dec', 'inw', 'dew', 'asl', 'lsr', 'rol', 'ror'}
              and re.match(r'^\$[23]\b', operand)}
    if writes != admitted_writes:
        raise ValueError('software stack pointer writes need fresh accounting')
    cache = {}

    def walk(entry, ancestors):
        if entry in cache:
            return cache[entry]
        if entry in ancestors:
            raise ValueError('recursive call graph')
        pending = [(entry, 0, 0)]
        depths = {}
        peak = 0
        software_peak = 0
        returned = False
        while pending:
            address, depth, software_depth = pending.pop()
            if address in depths:
                if depths[address] != (depth, software_depth):
                    raise ValueError('unbalanced stack at control-flow join')
                continue
            depths[address] = (depth, software_depth)
            software_depth += software_effect.get(address, 0)
            if software_depth < 0:
                raise ValueError('software stack underflow')
            software_peak = max(software_peak, software_depth)
            op, operand = instructions[address]
            if op not in ordinary | branches | pushes | pulls | {'rts', 'jmp', 'bra', 'jsr'}:
                raise ValueError('unrecognized instruction: ' + op)
            if op in pushes:
                depth += 1
            elif op in pulls:
                depth -= 1
            if depth < 0:
                raise ValueError('stack underflow')
            peak = max(peak, depth)
            if op == 'rts':
                if depth != 0 or software_depth != 0:
                    raise ValueError('unbalanced return')
                returned = True
                continue
            if op in {'brk', 'rti', 'txs', 'tys', 'phw'}:
                raise ValueError('unsupported stack instruction: ' + op)
            if op in branches | {'jmp', 'bra', 'jsr'}:
                target = re.match(r'^\$([0-9a-f]+)\b', operand)
                if not target:
                    raise ValueError(f'indirect or unknown transfer at {address:x}: {op} {operand}')
                destination = int(target[1], 16)
                if op == 'jsr':
                    callee_hardware, callee_software = walk(destination, ancestors | {entry})
                    peak = max(peak, depth + 2 + callee_hardware)
                    software_peak = max(software_peak, software_depth + callee_software)
                else:
                    pending.append((destination, depth, software_depth))
                    if op in {'jmp', 'bra'}:
                        continue
            pending.append((following[address], depth, software_depth))
        if not returned:
            raise ValueError('no reachable return')
        cache[entry] = (peak, software_peak)
        return cache[entry]

    hardware, software = walk(names['main'], set())
    high = hardware + 2
    if high >= 256 or software > 4096:
        raise ValueError('stack envelope exceeded')
    return {'hardware_bytes_main_including_entry_return': high,
            'software_dynamic_bytes': software,
            'software_constant_adjustments': len(software_effect),
            'call_entries_checked': len(cache),
            'scope': 'direct-call probe; no IRQ/NMI or executed high-water claim'}
