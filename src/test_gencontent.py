import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_normal(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_extract_title_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("Hello")
    
    def test_title_on_second_line(self):
        md = "Hello\n# This is the title"
        self.assertEqual(extract_title(md), "This is the title")
    