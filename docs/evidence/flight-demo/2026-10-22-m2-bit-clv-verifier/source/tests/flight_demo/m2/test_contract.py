"""Fail-closed generator and static stack checker tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools/flight_demo/m2' / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


generator = module('generate')
stack = module('stack_check')


def sequence(address, operations):
    lines = []
    for encoded, op in operations:
        lines.append(f' {address:x}: {encoded}  {op}')
        address += len(encoded.split())
    return '\n'.join(lines) + '\n'


def adjust(lo, hi):
    return [('18', 'clc'), ('a5 02', 'lda $2'), ('69 ' + lo, 'adc #$' + lo),
            ('85 02', 'sta $2'), ('a5 03', 'lda $3'), ('69 ' + hi, 'adc #$' + hi),
            ('85 03', 'sta $3')]


BIT_CLV = [('2c b0 5a', 'bit $5ab0'), ('b8', 'clv')]


class ContractTests(unittest.TestCase):
    def test_generated_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            generator.generate(destination=Path(directory))
            for name in ('interfaces/generated/m2_pr1.h', 'interfaces/generated/m2_tables.c',
                         'memory/m2-pr1-ledger.json'):
                self.assertEqual((ROOT/name).read_bytes(), (Path(directory)/name).read_bytes())

    def test_every_profile_field_rejects_drift_before_write(self):
        data = json.loads((ROOT/'interfaces/m2_pr1.json').read_text())
        mutations=[]
        for section in ('constants','memory'):
            for key in data[section]:
                changed=json.loads(json.dumps(data));changed[section][key]+=1;mutations.append(changed)
        for key in ('fixture','camera','units','frame','identity'):
            changed=json.loads(json.dumps(data));changed[key]='INVALID';mutations.append(changed)
        changed=json.loads(json.dumps(data));changed['records']['M2Point'][0][1]='int16_t';mutations.append(changed)
        for changed in mutations:
            with tempfile.TemporaryDirectory() as directory:
                root=Path(directory);(root/'interfaces').mkdir()
                (root/'interfaces/m2_pr1.json').write_text(json.dumps(changed))
                with self.assertRaises(ValueError):generator.generate(root)
                self.assertFalse((root/'interfaces/generated').exists())

    def test_stack_rejects_growth_loop_and_indirect_call(self):
        for body in (' 1000: 48  pha\n 1001: 4c 00 10  jmp $1000',
                     ' 1000: 20 00 10  jsr $1000\n 1003: 60  rts',
                     ' 1000: 6c 00 20  jmp ($2000)'):
            with self.assertRaises(ValueError):stack.check('00001000 <main>:\n'+body)

    def test_stack_balanced_call(self):
        code='''00000010 <__do_init_stack>:
 10: a9 00  lda #$0
 12: 85 02  sta $2
 14: a9 d0  lda #$d0
 16: 85 03  sta $3
00001000 <main>:
 1000: 48  pha
 1001: 20 00 20  jsr $2000
 1004: 68  pla
 1005: 60  rts
00002000 <leaf>:
 2000: 48  pha
 2001: 68  pla
 2002: 60  rts
'''
        self.assertEqual(stack.check(code)['hardware_bytes_main_including_entry_return'],6)

    def test_software_stack_nested_and_unbalanced(self):
        allocate=adjust('f8','ff');release=adjust('08','00')
        main='00001000 <main>:\n'+sequence(0x1000,allocate+[('20 00 20','jsr $2000')]+release+[('60','rts')])
        leaf='00002000 <leaf>:\n'+sequence(0x2000,allocate+release+[('60','rts')])
        self.assertEqual(stack.check(main+leaf)['software_dynamic_bytes'],16)
        broken='00002000 <leaf>:\n'+sequence(0x2000,allocate+[('60','rts')])
        with self.assertRaises(ValueError):stack.check(main+broken)
        with self.assertRaises(ValueError):stack.check(main+leaf.replace('sta $2','sta $2,x'))

    def test_bit_clv_stack_neutral(self):
        fixtures = [[BIT_CLV[0]], [BIT_CLV[1]], BIT_CLV,
                    [('24 02', 'bit $2')], [('24 03', 'bit $3')],
                    [('89 40', 'bit #$40')], [('3c b0 5a', 'bit $5ab0,x')],
                    [('34 02', 'bit $2,x')]]
        for operations in fixtures:
            with self.subTest(operations=operations):
                code = '00001000 <main>:\n' + sequence(
                    0x1000, operations + [('60', 'rts')])
                result = stack.check(code)
                self.assertEqual(result['hardware_bytes_main_including_entry_return'], 2)
                self.assertEqual(result['software_dynamic_bytes'], 0)
                self.assertEqual(result['software_constant_adjustments'], 0)
                self.assertEqual(result['call_entries_checked'], 1)

    def test_bit_clv_both_conditional_successors(self):
        # Even when CLV fixes V, the proof must visit both BVS/BVC successors.
        # BIT's N/Z flags likewise must not prune BMI/BPL/BEQ/BNE paths.
        for encoded, branch in [('70', 'bvs'), ('50', 'bvc'), ('30', 'bmi'),
                                ('10', 'bpl'), ('f0', 'beq'), ('d0', 'bne')]:
            code = f'''00001000 <main>:
 1000: 2c b0 5a  bit $5ab0
 1003: b8  clv
 1004: {encoded} 0a  {branch} $1010
 1006: 48  pha
 1007: 68  pla
 1008: 4c 12 10  jmp $1012
 1010: 48  pha
 1011: 68  pla
 1012: 60  rts
'''
            with self.subTest(branch=branch, path='balanced'):
                self.assertEqual(stack.check(code)[
                    'hardware_bytes_main_including_entry_return'], 3)
            for address in ['1007', '1011']:
                with self.subTest(branch=branch, bad_path=address):
                    broken = code.replace(address + ': 68  pla', address + ': b8  clv')
                    with self.assertRaisesRegex(ValueError,
                            'unbalanced (stack at control-flow join|return)'):
                        stack.check(broken)

    def test_bit_clv_nested_accounting(self):
        def fixture(prefix):
            main = prefix + adjust('f8', 'ff') + [
                ('48', 'pha'), ('20 00 20', 'jsr $2000'), ('68', 'pla')]
            leaf = prefix + adjust('f8', 'ff') + [('48', 'pha'), ('68', 'pla')]
            release = adjust('08', '00') + [('60', 'rts')]
            return ('00001000 <main>:\n' + sequence(0x1000, main + release)
                    + '00002000 <leaf>:\n' + sequence(0x2000, leaf + release))

        before = stack.check(fixture([]))
        after = stack.check(fixture(BIT_CLV))
        self.assertEqual(after, before)
        self.assertEqual(after['hardware_bytes_main_including_entry_return'], 6)
        self.assertEqual(after['software_dynamic_bytes'], 16)

    def test_bit_clv_preserves_rejection_guards(self):
        fixtures = [
            ([('02', 'kil'), ('60', 'rts')], 'unrecognized instruction: kil'),
            ([('6c 00 20', 'jmp ($2000)')], 'indirect or unknown transfer'),
            ([('20 00 10', 'jsr $1000'), ('60', 'rts')], 'recursive call graph'),
            ([('48', 'pha'), ('60', 'rts')], 'unbalanced return'),
            ([('68', 'pla'), ('60', 'rts')], 'stack underflow'),
            ([('85 02', 'sta $2'), ('60', 'rts')], 'software stack pointer writes'),
            ([('95 02', 'sta $2,x'), ('60', 'rts')], 'software stack pointer writes'),
            (adjust('f8', 'ff') + [('60', 'rts')], 'unbalanced return'),
            (adjust('08', '00') + [('60', 'rts')], 'software stack underflow'),
            ([('9a', 'txs'), ('60', 'rts')], 'unrecognized instruction: txs'),
        ]
        for body, message in fixtures:
            with self.subTest(body=body):
                code = '00001000 <main>:\n' + sequence(0x1000, BIT_CLV + body)
                with self.assertRaisesRegex(ValueError, message):
                    stack.check(code)

    def test_bit_clv_growth_loop_rejected_on_either_branch(self):
        for encoded, branch in [('70', 'bvs'), ('50', 'bvc')]:
            code = '00001000 <main>:\n' + sequence(0x1000, BIT_CLV + [
                ('48', 'pha'), (encoded + ' f9', branch + ' $1000'),
                ('68', 'pla'), ('60', 'rts')])
            with self.subTest(branch=branch):
                with self.assertRaisesRegex(ValueError, 'unbalanced stack at control-flow join'):
                    stack.check(code)

    def test_bit_clv_stack_limits_unchanged(self):
        for pushes in [253, 254]:
            operations = BIT_CLV + [('48', 'pha')] * pushes + [('68', 'pla')] * pushes
            code = '00001000 <main>:\n' + sequence(0x1000, operations + [('60', 'rts')])
            with self.subTest(hardware_bytes=pushes + 2):
                if pushes == 253:
                    self.assertEqual(stack.check(code)[
                        'hardware_bytes_main_including_entry_return'], 255)
                else:
                    with self.assertRaisesRegex(ValueError, 'stack envelope exceeded'):
                        stack.check(code)
        for allocate, release, size in [('00 f0', '00 10', 4096),
                                         ('ff ef', '01 10', 4097)]:
            operations = BIT_CLV + adjust(*allocate.split()) + adjust(*release.split())
            code = '00001000 <main>:\n' + sequence(0x1000, operations + [('60', 'rts')])
            with self.subTest(software_bytes=size):
                if size == 4096:
                    self.assertEqual(stack.check(code)['software_dynamic_bytes'], size)
                else:
                    with self.assertRaisesRegex(ValueError, 'stack envelope exceeded'):
                        stack.check(code)


if __name__=='__main__':unittest.main()
