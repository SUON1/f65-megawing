"""Composition contract admission; no target execution or output mutation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('full_generate', ROOT/'tools/flight_demo/m2_full/generate.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class FullContractTests(unittest.TestCase):
    def test_generated_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            generator.generate(destination=target)
            for path in ['interfaces/generated/m2_full.h', 'memory/m2-full-ledger.json']:
                self.assertEqual((ROOT/path).read_bytes(), (target/path).read_bytes())

    def test_any_source_drift_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'interfaces').mkdir()
            source = (ROOT/'interfaces/m2_full.json').read_bytes()
            (root/'interfaces/m2_full.json').write_bytes(source+b' ')
            with self.assertRaises(ValueError):
                generator.generate(root)
            self.assertFalse((root/'interfaces/generated').exists())
            self.assertFalse((root/'memory').exists())

    def test_resource_and_mapping_closure(self):
        data = json.loads((ROOT/'interfaces/m2_full.json').read_text())
        self.assertEqual(data['tile_offset']+data['tiles']*data['tile_bytes'],data['blank_offset'])
        self.assertEqual(data['blank_offset']+data['tile_bytes'],data['store_bytes'])
        self.assertLessEqual(data['store_bytes'],65536)
        self.assertEqual(data['screen_bytes'],40*25*2)
        self.assertEqual(data['reserve_allocation'],0)
        for key in ['output_ntsc','output_pal']:
            width,height,x,y,scale=data[key]
            self.assertEqual(2*x+scale*data['width'],width)
            self.assertEqual(2*y+scale*data['height'],height)


if __name__ == '__main__':
    unittest.main()
