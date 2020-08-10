from mack import parser
import unittest


class TokenizerTest(unittest.TestCase):
    def test_tokenize(self):
        actual = list(parser.Tokenizer.tokenize("Hello World! I am testing the ToKENiZEr funcTIoN! $XC$"))
        expected = ["hello", "world", "i", "am", "testing", "the", "tokenizer", "function", "xc"]
        self.assertEqual(expected, actual)
