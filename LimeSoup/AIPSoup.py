#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_aip import ParserPaper

__author__ = 'Zach Jensen'
__maintainer__ = 'Zach Jensen'
__email__ = 'zjensen@mit.edu'
__version__ = '0.3.0'

class AIPRemoveTagsSmallSub(RuleIngredient):
    # Gets rid of sub/sup scripts, bold, italics, etc but keeps text
    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [

        ]
        parser.operation_tag_remove_space(rules)
        
        return parser.raw_html

class AIPRemoveTrash(RuleIngredient):
    # Removes tags and their content we don't want
    @staticmethod
    def _parse(html_str):
        list_remove = [

        ]

        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_html

class AIPCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_sections()
        return parser.raw_html

class AIPReplaceDivTag(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = []
        parser.strip_tags(rules)
        return parser.raw_html      

class AIPCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[])
        parser.get_title(rules=[])
        parser.get_journal(rules=[])
        parser.get_doi(rules=[])
        # Create tag from selection function in ParserPaper
        parser.deal_with_sections()
        data = parser.data_sections
        
        obj = {
            'DOI': parser.doi,
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': parser.journal,
            'Sections': data
        }

        return obj

AIPSoup = Soup(parser_version=__version__)
AIPSoup.add_ingredient(AIPRemoveTagsSmallSub())
AIPSoup.add_ingredient(AIPRemoveTrash())
AIPSoup.add_ingredient(AIPCreateTags())
AIPSoup.add_ingredient(AIPReplaceDivTag())
AIPSoup.add_ingredient(AIPCollect())