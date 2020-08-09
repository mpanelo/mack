from mack import fs
import collections
import os
import shutil
import tempfile
import unittest


class FSTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = [tempfile.mkstemp(dir=self.temp_dir) for _ in range(100)]

    def tearDown(self):
        for temp_file, _ in self.temp_files:
            os.close(temp_file)
        shutil.rmtree(self.temp_dir)

    def test_batch_read(self):
        for test_case in FSTest._data_provider():
            result = list(fs.batch_read(self.temp_dir, test_case.batch_size))
            self.assertEqual(test_case.expected, len(result))

    @staticmethod
    def _data_provider():
        TestCase = collections.namedtuple("TestCase", "expected batch_size")

        return [
            TestCase(expected=1, batch_size=100),
            TestCase(expected=2, batch_size=50),
            TestCase(expected=10, batch_size=10)
        ]