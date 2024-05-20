# -*- coding: utf-8 -*-
import os

from datatableview_advanced_search.lexer import AdvancedSearchLexer
from datatableview_advanced_search.parser import AdvancedSearchParser
import unittest
from datatableview_advanced_search.datatables import AdvancedSearchDataTable
from django.db.models import Q
from datatableview_advanced_search.__init__ import compiler


class ParserTestSuite(unittest.TestCase):
    """Basic test cases."""

    def tearDown(self) :
        filename = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "datatableview_advanced_search/parsetab.py",
        )
        filename2 = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "datatableview_advanced_search/parser.out",
        )
        for pathname in [filename2, filename]:
            if os.path.exists(pathname):
                os.remove(pathname)

    def test_in_numbers(self):
        parser = AdvancedSearchParser()
        q = parser.parse("A IN [1,2,3.0]")
        self.assertEqual("(AND: ('A__in', [1, 2, 3.0]))", "{}".format(q))

    def test_map_file_single(self):
        name_map = {"ab": ["a__name"]}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("ab = 2.3")
        self.assertEqual("(AND: ('a__name__exact', 2.3))", "{}".format(q))

    def test_map_file(self):
        name_map = {"ab": ["a__name", "b__name"]}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("ab = 2.3")
        self.assertEqual(
            "(OR: ('a__name__exact', 2.3), ('b__name__exact', 2.3))", "{}".format(q)
        )

    def test_map_file_field_not_found(self):
        name_map = {"ab": ["a__name", "b__name"]}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("aC = 2.3")
        self.assertEqual("(AND: ('aC__exact', 2.3))", "{}".format(q))

    def test_map_file_in_single(self):
        name_map = {"ab": "a__name"}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("ab IN [2.3, 3.0]")
        self.assertEqual("(AND: ('a__name__in', [2.3, 3.0]))", "{}".format(q))

    def test_map_file_in(self):
        name_map = {"ab": ["a__name", "b__name"]}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("ab IN [2.3, 3.0]")
        self.assertEqual(
            "(OR: ('a__name__in', [2.3, 3.0]), ('b__name__in', [2.3, 3.0]))",
            "{}".format(q),
        )

    def test_map_file_in_field_not_found(self):
        name_map = {"ab": ["a__name", "b__name"]}
        parser = AdvancedSearchParser(name_map=name_map)
        q = parser.parse("aC IN [2.3, 3.0]")
        self.assertEqual("(AND: ('aC__in', [2.3, 3.0]))", "{}".format(q))

    def test_digits_near_words(self):
        parser = AdvancedSearchParser()
        q = parser.parse('(ID=94 OR product~="1p1")')
        self.assertEqual(
            "(OR: ('ID__exact', 94), ('product__contains', '1p1'))", "{}".format(q)
        )

class MockToken:
        def __init__(self, value):
            self.value = value
            self.lexer = self

        def __init__(self, value, lexmatch):
            self.value = value
            self.lexmatch = lexmatch
            self.lexer= self

class MockLexMatch:
    def __init__(self, matched_value):
        self.matched_value = matched_value

    def group(self, group_name):
        # For simplicity, assuming group_name is not used in this example
        return self.matched_value if self.matched_value else None

class LexerTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_in_numbers(self):
        lexer = AdvancedSearchLexer()
        self.assertTrue(lexer.test("A IN [1,2,3.0]", print_output=False))

    def test_digits_near_words(self):
        lexer = AdvancedSearchLexer()
        self.assertTrue(lexer.test('(ID=94 OR product~="1p1")', print_output=False))

    def test_digits_near_words_two(self):
        lexer = AdvancedSearchLexer()
        self.assertTrue(lexer.test("(ID=94 OR product~=1p1)", print_output=False))

    def test_digits_near_words_three(self):
        lexer = AdvancedSearchLexer()
        self.assertTrue(
            lexer.test(
                "test_run_iteration~=1p19_2018.02.20_20:41:19", print_output=True
            )
        )



    def test_the_int(self):
        lexer=AdvancedSearchLexer()
        test_cases = ["123", "+456", "789", "987654321", "-123", "-456"]
        for test_case in test_cases:
            token = MockToken(test_case, "word")
            returned_token = lexer.t_INT(token)
            self.assertEqual(returned_token.value, int(test_case))

    def test_errors_in_int(self):
        lexer = AdvancedSearchLexer()
        test_cases=["abc", "12a", "-+123", "+-456"]
        for invalid_case in test_cases:
            token = MockToken(invalid_case, "word")
            self.assertRaises(ValueError, lexer.t_INT, token)


    def test_SINGLE_QUOTE_WORD(self):
        #make into dict
        lexer = AdvancedSearchLexer()
        test_cases = ["'word'", "'some_word'", "'with_123'", "'abc:def'", "'with space'", "'with.dec'",
                      "'with\\'singlequote'", "'with\"doublequote'"]
        expected_values = ["word", "some_word", "with_123", "abc:def", "with space", "with.dot", "with'singlequote",
                           'with"doublequote']
        counter = 0
        for test_case in test_cases:
            token = MockToken(test_case, MockLexMatch(expected_values[counter]))
            returned_token = lexer.t_SINGLE_QUOTE_WORD(token)
            self.assertEqual(returned_token.value, expected_values[counter])
            counter += 1


    """" def test_t_SINGLE_QUOTE_WORD_invalid(self):
        
        lexer = AdvancedSearchLexer()
        invalid_cases = ["''", "' '", "'   '", "'abc: def'", "'abc.def'", "'with$specialchar'", "'with\\\\backslash'",
                         "'with'extraquote'", "'with\"extraquote'"]
        for invalid_case in invalid_cases:
            # Mock a token object with a lexmatch attribute
            token = MockToken(invalid_case, MockLexMatch(""))
            with self.assertRaises(ValueError):
                lexer.t_SINGLE_QUOTE_WORD(token)
                """

if __name__ == "__main__":
    unittest.main()