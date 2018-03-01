# -*- coding: utf-8 -*-
"""jira_lex.py: Django datatableview_advanced_search"""

from __future__ import unicode_literals
from __future__ import print_function

import logging

import lexer
import ply.yacc as yacc

__author__ = 'Steven Klass'
__date__ = '2/28/18 9:20 AM'
__copyright__ = 'Copyright 2018 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

tokens = lexer.tokens

compa2lookup = {
    '=': 'exact',
    '~=': 'contains',
    '>': 'gt',
    '>=': 'gte',
    '<': 'lt',
    '<=': 'lte',
}


def p_expression_paren(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_compare(p):
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


def p_expression_in(p):
    """expression : variable IN list"""
    from django.db.models import Q
    p[0] = Q({str('%s__in' % (p[1])): p[3]})


def p_list(p):
    """list : LBRACK list_vals RBRACK"""
    p[0] = p[2]


def p_list_vals(p):
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


def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = ~ p[2]


def p_expression_and(p):
    """expression : expression AND expression"""
    p[0] = p[1] & p[3]


def p_expression_or(p):
    """expression : expression OR expression"""
    p[0] = p[1] | p[3]


precedence = (
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'NOT'),
)


def p_value(p):
    '''value : variable
             | number
             | DATE'''
    p[0] = p[1]


def p_variable(p):
    '''variable : WORD
                | SINGLE_QUOTE_WORD
                | DOUBLE_QUOTE_WORD'''
    p[0] = p[1]


def p_number(p):
    '''number : INT
              | FLOAT'''
    p[0] = p[1]


def p_error(p):
    if p:
        print("Parsing error around token: '%s'" % p.value)
    else:
        print("Parsing error: unexpected end of expression")


adv_search_yacc = yacc.yacc