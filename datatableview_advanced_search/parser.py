# -*- coding: utf-8 -*-
"""jira_lex.py: Django datatableview_advanced_search"""

from __future__ import unicode_literals
from __future__ import print_function

import logging

import sys

from lexer import AdvancedSearchLexer
import ply.yacc as yacc

__author__ = 'Steven Klass'
__date__ = '2/28/18 9:20 AM'
__copyright__ = 'Copyright 2018 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

compa2lookup = {
    '=': 'exact',
    '~=': 'contains',
    '>': 'gt',
    '>=': 'gte',
    '<': 'lt',
    '<=': 'lte',
}


class AdvancedSearchParser(object):
    tokens = AdvancedSearchLexer.tokens

    def __init__(self, **kwargs):
        self.name_map = kwargs.pop('name_map', {})
        self.lexer = AdvancedSearchLexer(**kwargs).lexer
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_expression_paren(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]


    def p_expression_compare(self, p):
        """expression : variable COMPARE value"""

        lookup = compa2lookup[p[2]]

        field = p[1]

        if lookup:
            field = '%s__%s' % (field, lookup)

        # In some situations (which ones?), python
        # refuses unicode strings as dict keys for
        # Q(**d)
        field = str(field)

        d = {field: p[3]}

        from django.db.models import Q
        p[0] = Q(**d)


    def p_expression_in(self, p):
        """expression : variable IN list"""
        from django.db.models import Q
        p[0] = Q({str('%s__in' % (p[1])): p[3]})


    def p_list(self, p):
        """list : LBRACK list_vals RBRACK"""
        p[0] = p[2]


    def p_list_vals(self, p):
        """list_vals : value COMMA value
                     | list_vals COMMA value"""
        if isinstance(p[1], list):
            if isinstance(p[3], list):
                p[0] = p[1] + p[3]
            else:
                p[0] = p[1] + [p[3]]
        else:
            if isinstance(p[3], list):
                p[0] = [p[1]] + p[3]
            else:
                p[0] = [p[1]] + [p[3]]


    def p_expression_not(self, p):
        """expression : NOT expression"""
        p[0] = ~ p[2]


    def p_expression_and(self, p):
        """expression : expression AND expression"""
        p[0] = p[1] & p[3]


    def p_expression_or(self, p):
        """expression : expression OR expression"""
        p[0] = p[1] | p[3]


    precedence = (
        ('left', 'AND'),
        ('left', 'OR'),
        ('right', 'NOT'),
    )


    def p_value(self, p):
        '''value : variable
                 | number
                 | DATE'''
        p[0] = p[1]


    def p_variable(self, p):
        '''variable : WORD
                    | SINGLE_QUOTE_WORD
                    | DOUBLE_QUOTE_WORD'''
        p[0] = p[1]


    def p_number(self, p):
        '''number : INT
                  | FLOAT'''
        p[0] = p[1]


    def p_error(self, p):
        if p:
            print("Parsing error around token: '%s'" % p.value)
        else:
            print("Parsing error: unexpected end of expression")

    def parse(self, text):
        return self.parser.parse(text, self.lexer)


def main(args):
    """Main - $<description>$"""
    logging.basicConfig(
        level=logging.DEBUG, datefmt="%H:%M:%S", stream=sys.stdout,
        format="%(asctime)s %(levelname)s [%(filename)s] (%(name)s) %(message)s")

    # Test it out
    data = '''
    (foo='bar\'s' AND x=1) OR (ya IN [2, 3, -3.5]) AND datestamp >= 1/25/2018 AND X="THe OTH3R"
    '''

    m = AdvancedSearchParser()
    print(m.parse(data)) # Test it


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="$<description>$")
    sys.exit(main(parser.parse_args()))
