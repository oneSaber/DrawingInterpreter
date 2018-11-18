import unittest
from Lexer import Scanner

class LexerTest(unittest.TestCase):
    def setUp(self):
        self.scanner = Scanner("helloworld")
    def tearDown(self):
        pass
    def testscanfile(self):
        # self.assertEqual(self.scanner.scanFile(),,"message")
        pass