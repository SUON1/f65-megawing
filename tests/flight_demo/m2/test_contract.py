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
        def sequence(address, operations):
            lines=[]
            for encoded, op in operations:
                lines.append(f' {address:x}: {encoded}  {op}')
                address += len(encoded.split())
            return '\n'.join(lines)+'\n'

        def adjust(lo, hi):
            return [('18','clc'),('a5 02','lda $2'),('69 '+lo,'adc #$'+lo),
                    ('85 02','sta $2'),('a5 03','lda $3'),('69 '+hi,'adc #$'+hi),
                    ('85 03','sta $3')]

        allocate=adjust('f8','ff');release=adjust('08','00')
        main='00001000 <main>:\n'+sequence(0x1000,allocate+[('20 00 20','jsr $2000')]+release+[('60','rts')])
        leaf='00002000 <leaf>:\n'+sequence(0x2000,allocate+release+[('60','rts')])
        self.assertEqual(stack.check(main+leaf)['software_dynamic_bytes'],16)
        broken='00002000 <leaf>:\n'+sequence(0x2000,allocate+[('60','rts')])
        with self.assertRaises(ValueError):stack.check(main+broken)
        with self.assertRaises(ValueError):stack.check(main+leaf.replace('sta $2','sta $2,x'))


if __name__=='__main__':unittest.main()
