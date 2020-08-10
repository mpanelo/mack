from mack import index_io
import unittest
import os


class UniquePathGeneratorTest(unittest.TestCase):
    def test_generate(self):
        root = "fake_root_dir"
        path_generator = index_io.UniquePathGenerator(root, prefix="mack", extension="txt")
        self.assertEqual(os.path.join(root, "mack_000.txt"), path_generator.generate())
        self.assertEqual(os.path.join(root, "mack_001.txt"), path_generator.generate())
        self.assertEqual(os.path.join(root, "mack_002.txt"), path_generator.generate())
