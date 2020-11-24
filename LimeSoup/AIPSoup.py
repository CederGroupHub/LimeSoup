#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re
from bs4 import BeautifulSoup

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_aip import ParserPaper

__author__ = 'Zach Jensen'
__maintainer__ = 'Zach Jensen'
__email__ = 'zjensen@mit.edu'
__version__ = '0.3.0'

class AIPRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [
                 {'name': 'sub'},
                 {'name': 'sup'},
                 {'name': 'i'},
                 {'name': 'b'},
                 {'name': 'em', 'class': re.compile("EmphasisTypeItalic *")}, 
                 {'name': 'strong', 'class': re.compile("EmphasisTypeBold *")},
                 {'name': 'span', 'class':'InlineEquation'},
                 {'name': 'span', 'class':'InternalRef'},
                 {'name': 'mi'},
                #  {'name': 'mtext'},  # this was removing important spaces for units embedded in math text
                 {'name': 'mrow'},
                 {'name': 'msub'},
                 {'name': 'msup'},
                 {'name': 'named-content'},
                 {'name': 'a', 'class': 'ref headerSection'},
                 {'name': 'a', 'title': 'Open Figure Viewer'}
                ]
        parser.operation_tag_remove_space(rules)
        # Remove some specific all span that are inside of a paragraph 'p'
        parser.strip_tags(rules)
        # tags = parser.soup.find_all(**{'name': 'p'})
        # parser.strip_tags(rules)
        html_str = str(parser.soup)
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)

        return parser.raw_html

class AIPRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper 
        list_remove = [
            {'name': 'span', 'class': 'ref-lnk'}, #references in text
            {'name': 'table'},  # gets rid of tables and equations
            {'name': 'div', 'class': 'caption'},  # figure captions
            {'name': 'div', 'class': "table-article"},  # table label
            {'name': 'div', 'class': 'ack'},
            # {'name': 'span', 'class': 'equationTd inline-formula'}, # in line equations, this has been taken out  to remove because it was found that important numbers and even chemical compounds were wrapped in this tag
            {'name': 'div', 'class': 'NLM_sec-type_supplementary-material'}, # supplimental information
            {'name': 'div', 'class': 'footnote'},  # remove table footnotes
        ]
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}]
        )
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
        rules = [{'name': 'div'}]
        parser.strip_tags(rules)
        rules = [{'name': 'span', 'id': parser.compile('^sect[0-9]+$')}]  # some span are heading
        _ = parser.strip_tags(rules)
        return parser.raw_html


class AIPGetUntitledParagraphs(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_for_untitled_sections()
        return parser.raw_html


class AIPHandleLists(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.handle_lists()
        return parser.raw_html


class AIPCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'span', 'class': 'Keyword'}])
        parser.get_title(rules=[
                {'name': 'h1', 'recursive': True},
            ]
        )
        print(type(parser.title))
        print(parser.title)
        if parser.title is not None:
            parser.title = re.sub('&ensp;', ' ', parser.title)
            parser.title = re.sub('&thinsp', ' ', parser.title)
            parser.title = re.sub('&emsp', ' ', parser.title)
        parser.get_doi()
        parser.get_journal()
        # Create tag from selection function in ParserPaper
        data = list()
        soup = BeautifulSoup(html_str, 'html.parser')
        parser.deal_with_sections()
        data = parser.data_sections

        if len(data) == 0:  # this means there are no headers at all, so all paragraphs will be collected
            abstract_tag = parser.soup.find('div', class_='hlFld-Abstract')
            if abstract_tag:
                abstract=dict()
                ab_text = abstract_tag.find('div', class_='NLM_paragraph').text.strip()
                ab_text = re.sub(r'[\n] *', ' ', ab_text) 
                ab_text = re.sub(r' {2,}', ' ', ab_text)
                abstract['content'] = [ab_text]
                abstract['name'] = 'Abstract'
                abstract['type'] = 'section_h2'
                data = [abstract]+data

        obj = {
            'DOI': parser.doi,
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': parser.journal_name,
            'Sections': data
        }

        def section_type_corrector(dictionary):
            new_num = int(dictionary['type'][-1])-3
            dictionary['type'] = dictionary['type'][:-1]+str(new_num)
            for content in dictionary['content']:
                if type(content) == dict:
                    section_type_corrector(content)
        for section in obj['Sections']:
            section_type_corrector(section)

        return obj

AIPSoup = Soup(parser_version=__version__)
AIPSoup.add_ingredient(AIPRemoveTagsSmallSub())
AIPSoup.add_ingredient(AIPHandleLists())
AIPSoup.add_ingredient(AIPRemoveTrash())
AIPSoup.add_ingredient(AIPCreateTags())
# AIPSoup.add_ingredient(AIPReplaceDivTag())
AIPSoup.add_ingredient(AIPGetUntitledParagraphs())
AIPSoup.add_ingredient(AIPCollect())