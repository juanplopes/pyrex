import unittest
import pyrex

class TestPyrex(unittest.TestCase):
    def test_single_literal(self):
        self.assertEqual([(0, 1)], list(pyrex.rex('a').match('a')))

    def test_single_literal_matching_multiple_times(self):
        self.assertEqual([(0, 1), (1, 1)], list(pyrex.rex('a').match('aa')))

    def test_double_literal(self):
        self.assertEqual([(0, 2)], list(pyrex.rex('aa').match('aa')))

    def test_double_literal_matching_multiple_times(self):
        self.assertEqual([(0, 2), (1, 2), (2, 2)], list(pyrex.rex('aa').match('aaaa')))

    def test_simple_repetition(self):
        self.assertEqual([(0, 1), (0, 2), (1, 1)], list(pyrex.rex('a+').match('aa')))

    def test_simple_repetition_zero_or_more(self):
        self.assertEqual([(0, 1), (0, 2), (1, 1)], list(pyrex.rex('a*').match('aa')))

    def test_simple_repetition_zero_or_one(self):
        self.assertEqual([(0, 1), (0, 2), (1, 1)], list(pyrex.rex('aa?').match('aa')))

    def test_options_simple(self):
        self.assertEqual([(0, 2), (1, 2)], list(pyrex.rex('ab|aa').match('aab')))

    def test_grouping_simple(self):
        self.assertEqual([(0, 3), (0, 5)], list(pyrex.rex('a(ab)+').match('aabab')))



        
if __name__ == "__main__":
    unittest.main()
