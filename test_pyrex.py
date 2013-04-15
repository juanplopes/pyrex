import unittest
import pyrex

class TestPyrex(unittest.TestCase):
    def test_single_literal(self):
        self.assertEqual((0, 1), pyrex.rex('a').match('a'))

    def test_single_literal_matching_multiple_times(self):
        self.assertEqual((0, 1), pyrex.rex('a').match('aa'))

    def test_double_literal(self):
        self.assertEqual((0, 2), pyrex.rex('aa').match('aa'))

    def test_double_literal_matching_multiple_times(self):
        self.assertEqual((0, 2), pyrex.rex('aa').match('aaaa'))

    def test_simple_repetition(self):
        self.assertEqual((0, 2), pyrex.rex('a+').match('aa'))

    def test_simple_repetition_with_optional(self):
        self.assertEqual((0, 2), pyrex.rex('a+?').match('aa'))

    def test_simple_repetition_zero_or_more(self):
        self.assertEqual((0, 2), pyrex.rex('a*').match('aa'))

    def test_simple_repetition_zero_or_one(self):
        self.assertEqual((0, 2), pyrex.rex('aa?').match('aa'))

    def test_options_simple(self):
        self.assertEqual((0, 2), pyrex.rex('ab|aa').match('aab'))

    def test_grouping_simple(self):
        self.assertEqual((0, 5), pyrex.rex('a(ab)+').match('aabab'))

    def test_would_never_end(self):
        self.assertEqual(None, pyrex.rex('(.+.+)+y').match('a'*29))

    def test_will_match_greedly(self):
        self.assertEqual((0, 30), pyrex.rex('(.+.+)+y').match('a'*29+'y'))

    def test_article_specially_crafted_regex(self):
        self.assertEqual((0, 30), pyrex.rex('a?'*30+'a'*30).match('a'*30))

        
if __name__ == "__main__":
    unittest.main()
