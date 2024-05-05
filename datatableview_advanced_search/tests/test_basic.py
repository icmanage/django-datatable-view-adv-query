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
    def test_randLines(self):
        lexer = AdvancedSearchLexer()
        comp = compiler()



if __name__ == "__main__":
    unittest.main()

class AdvancedSearchDataTableTestSuite(unittest.TestCase):
    def setUp(self):
        self.data_table = AdvancedSearchDataTable()

    def test_get_table_map(self):
        # Test whether get_table_map returns the correct dictionary
        expected_map = {
            "column1_name": ["source1", "source2"],
            "column2_name": ["source3"],
            # Add more expected mappings here based on your columns and sources
        }
        self.assertEqual(self.data_table.get_table_map(), expected_map)

    def test_normalize_config_search(self):
        # Test whether normalize_config_search returns the correct normalized search string
        config = {"search": " Test Query "}
        query_config = {}
        normalized_search = self.data_table.normalize_config_search(config, query_config)
        self.assertEqual(normalized_search, "Test Query")

    def test_search(self):
        # Test the search method with a mock queryset and config
        # Mock queryset
        class MockQuerySet:
            @staticmethod
            def filter(q):
                return "Filtered Queryset"

            @staticmethod
            def distinct():
                return "Distinct Queryset"

        mock_queryset = MockQuerySet()

        # Mock config
        config = {
            "column_searches": {
                "column1": "search_term1",
                "column2": "search_term2",
            },
            "search": "global_search_term",
            "search_fields": ["field1", "field2"],
        }

        self.assertEqual(self.data_table.search(mock_queryset), "Distinct Queryset")

    def test_parse_advanced_search_string(self):
        # Test whether _parse_advanced_search_string correctly compiles the search string
        search_string = "Test Query"
        compiled_query = self.data_table._parse_advanced_search_string(search_string)
        self.assertIsInstance(compiled_query, Q)

if __name__ == '__main__':
    unittest.main()
