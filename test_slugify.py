"""Tests for slugify.slugify, written from the public specification.

Specification under test:
  * lowercase the input;
  * replace every maximal run of characters that are NOT an ASCII lowercase
    letter (a-z) or ASCII digit (0-9) with a single hyphen;
  * strip leading/trailing hyphens;
  * return "" for an empty string or a string of only separators.
"""

import unittest

from slugify import slugify


class SlugifyRequiredExamplesTests(unittest.TestCase):
    def test_required_examples(self):
        cases = [
            ("Hello, World!", "hello-world"),
            ("  DeepSeek   Harness  ", "deepseek-harness"),
            ("Agent 123", "agent-123"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


class SlugifyEmptyAndSeparatorOnlyTests(unittest.TestCase):
    def test_empty_string_returns_empty_string(self):
        self.assertEqual(slugify(""), "")

    def test_only_punctuation_and_separators_returns_empty_string(self):
        cases = [
            "!!!",
            "???",
            "   ",
            ",.;:-_?!",
            "\t\n\r",
            "---",
            "@#$%",
            " -_- ",
        ]
        for raw in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), "")


class SlugifySeparatorHandlingTests(unittest.TestCase):
    def test_consecutive_separators_collapse_to_one_hyphen(self):
        cases = [
            ("hello___world", "hello-world"),
            ("hello   world", "hello-world"),
            ("hello!!!world", "hello-world"),
            ("hello\t\nworld", "hello-world"),
            ("hello-_-world", "hello-world"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)

    def test_mixed_separators_collapse_to_one_hyphen(self):
        cases = [
            ("one .,; two", "one-two"),
            ("a!!!  ???b", "a-b"),
            ("A . , ; B", "a-b"),
            ("foo\tbar\nbaz", "foo-bar-baz"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)

    def test_single_separator_becomes_single_hyphen(self):
        cases = [
            ("hello world", "hello-world"),
            ("hello-world", "hello-world"),
            ("hello_world", "hello-world"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


class SlugifyDigitTests(unittest.TestCase):
    def test_digits_are_preserved(self):
        cases = [
            ("12345", "12345"),
            ("Agent 123", "agent-123"),
            ("version 2", "version-2"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)

    def test_letters_and_digits_are_split_only_where_input_had_separator(self):
        cases = [
            ("abc123", "abc123"),
            ("123abc", "123abc"),
            ("a1b2c3", "a1b2c3"),
            ("abc 123", "abc-123"),
            ("123 456", "123-456"),
            ("ABC 123 def", "abc-123-def"),
            ("a1  b2", "a1-b2"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


class SlugifyCaseTests(unittest.TestCase):
    def test_uppercase_input_is_lowercased(self):
        cases = [
            ("HELLO", "hello"),
            ("HELLO WORLD", "hello-world"),
            ("PyThOn", "python"),
            ("ABC123", "abc123"),
            ("MiXeD CaSe", "mixed-case"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


class SlugifyTrimmingTests(unittest.TestCase):
    def test_leading_and_trailing_separators_are_stripped(self):
        cases = [
            ("--hello--", "hello"),
            ("  hello  ", "hello"),
            ("...hello...", "hello"),
            ("!!! Hello !!!", "hello"),
            ("\t hello \n", "hello"),
            ("-_-hello-_-", "hello"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)

    def test_result_never_starts_or_ends_with_a_hyphen(self):
        for raw in ["  Hello, World!  ", "!!!a!!!", "---b---", "c", "-_-"]:
            with self.subTest(raw=raw):
                result = slugify(raw)
                self.assertFalse(result.startswith("-"), repr(result))
                self.assertFalse(result.endswith("-"), repr(result))


class SlugifyCombinedTests(unittest.TestCase):
    def test_combined_realistic_inputs(self):
        cases = [
            ("  Hello,   World!!! 2024  ", "hello-world-2024"),
            ("DeepSeek -- Harness__v2", "deepseek-harness-v2"),
            ("A1  B2\tC3", "a1-b2-c3"),
            ("  Agent 123: Ready?  ", "agent-123-ready"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


if __name__ == "__main__":
    unittest.main()
