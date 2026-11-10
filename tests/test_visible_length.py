"""Regression tests: visible_length must not go negative on control chars.

wcwidth() returns -1 for non-printable control characters (BEL, NUL,
backspace, ...), so summing it raw under-measures the visible width of
any line containing them and text_wrap then overfills the line.
Control characters occupy no columns and must count as zero.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamdown.sdlib import visible_length


class VisibleLengthTests(unittest.TestCase):
    def test_plain_ascii(self):
        self.assertEqual(visible_length("hello"), 5)

    def test_ansi_escapes_not_counted(self):
        self.assertEqual(visible_length("a\x1b[31mX\x1b[0m"), 2)

    def test_bel_takes_no_width(self):
        self.assertEqual(visible_length("a\x07b"), 2)

    def test_nul_and_backspace_take_no_width(self):
        self.assertEqual(visible_length("\x00\x08"), 0)

    def test_cjk_still_double_width(self):
        self.assertEqual(visible_length("あ"), 2)


if __name__ == "__main__":
    unittest.main()
