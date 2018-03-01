# -*- coding: utf-8 -*-
"""__init__.py: Django datatableview_advanced_search package container"""

from __future__ import unicode_literals
from __future__ import print_function

from lexer import AdvancedSearchLexer
import parser

__author__ = 'Steven Klass'
__version_info__ = (0, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__date__ = '3/1/18 9:22 AM'
__copyright__ = 'Copyright 2018 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]
__license__ = 'See the file LICENSE.txt for licensing information.'


def compiler(expression, debug=False, log=None):
    adv_lexer = AdvancedSearchLexer()
    adv_lexer.build()

    adv_parser = parser.adv_search_yacc(module=parser, debug=debug, debuglog=log)
    return adv_parser.parse(expression, lexer=adv_lexer.lexer)