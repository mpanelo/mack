from mack import index_io
import os
import unittest


class UniquePathGeneratorTest(unittest.TestCase):
    def test_generate(self):
        root = "fake_root_dir"
        path_generator = index_io.UniquePathGenerator(root, prefix="mack", extension="txt")
        self.assertEqual(os.path.join(root, "mack_000.txt"), path_generator.generate())
        self.assertEqual(os.path.join(root, "mack_001.txt"), path_generator.generate())
        self.assertEqual(os.path.join(root, "mack_002.txt"), path_generator.generate())


class IndexLookupTableTest(unittest.TestCase):
    def setUp(self):
        self.filename = "tmp_lookup_table.txt"
        with open(self.filename, "w") as file:
            file.writelines("{};{}\n".format(char, i) for i, char in enumerate("abcdefgh"))

    def tearDown(self):
        os.remove(self.filename)

    def test_lookup(self):
        table = index_io.IndexLookupTable(src=self.filename)

        for i, key in enumerate("abcdefgh"):
            segment_file_name = table[key]
            self.assertEqual(str(i), segment_file_name)
