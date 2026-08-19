import unittest

from slugify import slugify


class SlugifyCompatibilityTests(unittest.TestCase):
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

    def test_removes_boundary_underscores(self):
        self.assertEqual(slugify("___Already Sluggy___"), "already-sluggy")

    def test_preserves_internal_underscores(self):
        self.assertEqual(slugify("Snake_Case"), "snake_case")

    def test_preserves_unicode_letters_and_numbers(self):
        self.assertEqual(slugify("Café 東京 １２"), "café-東京-１２")

    def test_empty_input(self):
        self.assertEqual(slugify(""), "")

    def test_punctuation_only_input(self):
        self.assertEqual(slugify("!?..."), "")


if __name__ == "__main__":
    unittest.main()
