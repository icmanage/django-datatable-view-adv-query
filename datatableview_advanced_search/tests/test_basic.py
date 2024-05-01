# -*- coding: utf-8 -*-
import os

from datatableview_advanced_search.lexer import AdvancedSearchLexer
from datatableview_advanced_search.parser import AdvancedSearchParser
import unittest
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


if __name__ == "__main__":
    unittest.main()
