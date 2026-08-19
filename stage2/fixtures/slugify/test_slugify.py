import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_simple_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_collapses_whitespace(self):
        self.assertEqual(slugify("hello   world\tagain"), "hello-world-again")

    def test_replaces_punctuation_runs(self):
        self.assertEqual(slugify("API: design & testing"), "api-design-testing")

    def test_removes_leading_and_trailing_separators(self):
        self.assertEqual(slugify("---Already Sluggy!---"), "already-sluggy")

    def test_preserves_numbers(self):
        self.assertEqual(slugify("Qwen 3.8 27B"), "qwen-3-8-27b")


if __name__ == "__main__":
    unittest.main()
