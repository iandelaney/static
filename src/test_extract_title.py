import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_strips_whitespace(self):
        markdown = "#    Hello world   "
        self.assertEqual(extract_title(markdown), "Hello world")

    def test_extract_title_from_multiline_markdown(self):
        markdown = """
This is a paragraph

# My Title

Another paragraph
"""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_raises_if_no_h1(self):
        markdown = """
## Not the title

Just some text
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()