"""Both branch arms and fail-closed stack/control-flow regressions."""
import hashlib
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("admission_stack", ROOT /
    "tools/flight_demo/m2_rebuild/stack_admission.py")
STACK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STACK)


def ins(op, operand="", raw="ea"):
    return op, operand, bytes.fromhex(raw)


class StackAdmission(unittest.TestCase):
    def test_second_branch_arm_is_checked(self):
        code = {0x1000: ins("beq", "$1004", "f0 02"),
                0x1002: ins("rts", raw="60"),
                0x1004: ins("pha", raw="48"), 0x1005: ins("rts", raw="60")}
        with self.assertRaisesRegex(ValueError, "unbalanced return"):
            STACK.Graph(code).walk(0x1000)
        code[0x1005] = ins("pla", raw="68")
        code[0x1006] = ins("rts", raw="60")
        self.assertEqual(STACK.Graph(code).walk(0x1000), (1, 0, True))

    def test_unknown_indirect_recursion_underflow_and_growing_loop_rejected(self):
        cases = [({0x1000: ins("brk", raw="00")}, "unsupported"),
                 ({0x1000: ins("jsr", "($2000)", "20 00 20")}, "unknown"),
                 ({0x1000: ins("jsr", "$1000", "20 00 10")}, "recursive"),
                 ({0x1000: ins("pla", raw="68")}, "underflow"),
                 ({0x1000: ins("pha", raw="48"),
                   0x1001: ins("bra", "$1000", "80 fd")}, "unequal")]
        for code, error in cases:
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                STACK.Graph(code).walk(0x1000)

    def test_nonreturning_terminal_is_bounded_and_does_not_fall_through(self):
        code = {0x1000: ins("jsr", "$2000", "20 00 20"),
                0x2000: ins("sei", raw="78"),
                0x2001: ins("jmp", "$2000", "4c 00 20")}
        self.assertEqual(STACK.Graph(code).walk(0x1000), (2, 0, False))

    def test_cld_bit_clv_keep_both_flag_outcomes(self):
        code = {0x1000: ins("cld", raw="d8"), 0x1001: ins("bit", "$20", "24 20"),
                0x1003: ins("clv", raw="b8"), 0x1004: ins("rts", raw="60")}
        self.assertEqual(STACK.Graph(code).walk(0x1000), (0, 0, True))

    def test_return_domains_do_not_mix(self):
        for op, mode in [("rti", "call"), ("rts", "interrupt")]:
            with self.subTest(op=op), self.assertRaisesRegex(ValueError, "return domain"):
                STACK.Graph({0x1000: ins(op)}).walk(0x1000, mode=mode)
        self.assertEqual(STACK.Graph({0x1000: ins("rti")}).walk(0x1000, mode="interrupt"),
                         (0, 0, True))

    def test_software_allocation_and_unknown_writes(self):
        ops = [("clc", "", "18"), ("lda", "$2", "a5 02"),
               ("adc", "#$fc", "69 fc"), ("sta", "$2", "85 02"),
               ("lda", "$3", "a5 03"), ("adc", "#$ff", "69 ff"),
               ("sta", "$3", "85 03")]
        code = {}; at = 0x1000
        for op, operand, raw in ops:
            code[at] = ins(op, operand, raw); at += len(code[at][2])
        effects = STACK.stack_effects(code, {})
        self.assertEqual(effects, {at - 2: 4})
        code[at] = ins("rts", raw="60")
        with self.assertRaisesRegex(ValueError, "unbalanced return"):
            STACK.Graph(code, effects).walk(0x1000)
        for operand in ["$2", "$3", "$2,x"]:
            with self.subTest(operand=operand), self.assertRaisesRegex(ValueError, "SP writes"):
                STACK.stack_effects({0x1000: ins("sta", operand, "85 02")}, {})

    def test_raw_long_branch_base_and_instruction_boundary(self):
        bad = {0x1000: ins("bra", "$fff", "83 fd ff"),
               0x1003: ins("rts", raw="60")}
        with self.assertRaisesRegex(ValueError, "instruction boundary"):
            STACK.branch_targets(bad)
        good = {0x1000: ins("bra", "$1000", "83 fe ff")}
        STACK.branch_targets(good)
        with self.assertRaisesRegex(ValueError, "disagreement"):
            STACK.branch_targets({0x1000: ins("bra", "$1003", "83 fe ff")})

    def test_interrupt_mapping_traps_and_all_direct_page_forms_rejected(self):
        cases = [("map", ""), ("sta", "$d640"), ("stx", "$d650"),
                 ("sty", "$d67f"), ("stz", "$d649"), ("inc", "$d640"),
                 ("lda", "$22"), ("sta", "$22,x"), ("lda", "($22),y"),
                 ("sta", "[$22],z")]
        for op, operand in cases:
            with self.subTest(op=op, operand=operand), self.assertRaises(ValueError):
                STACK.handler_effects({0x1000: ins(op, operand)}, {0x1000})
        STACK.handler_effects({0x1000: ins("lda", "#$1")}, {0x1000})

    def test_branch_into_partial_stack_initialization_rejected(self):
        code = {0x1000: ins("lda", "#$0", "a9 00"), 0x1002: ins("sta", "$2", "85 02"),
                0x1004: ins("lda", "#$d0", "a9 d0"), 0x1006: ins("sta", "$3", "85 03"),
                0x2000: ins("jmp", "$1004", "4c 04 10")}
        with self.assertRaisesRegex(ValueError, "partial software SP"):
            STACK.stack_effects(code, {"__do_init_stack": 0x1000})

    def test_nm_alias_is_used_for_software_stack_initialization(self):
        text = """00001000 <another_alias>:
    1000: a9 00        lda #$0
    1002: 85 02        sta $2
    1004: a9 d0        lda #$d0
    1006: 85 03        sta $3
"""
        code, names = STACK.parse(text, "00001000 00000000 T __do_init_stack\n")
        self.assertEqual(STACK.stack_effects(code, names), {})


if __name__ == "__main__":
    unittest.main()
