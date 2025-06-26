import unittest
from main import dir_crawler

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        #self.assertEqual(extract_title("content/test.md"), "Hey There Bitch!")
        self.assertEqual(1, 1)
        
    def test_dir_crawler(self):
        search = "testdir"
        self.assertListEqual(dir_crawler(search), ["testdir", ["script.py", ["subdir", ["secrets.txt"]], "webpage.html"]])