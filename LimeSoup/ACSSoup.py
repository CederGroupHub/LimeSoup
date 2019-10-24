#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_acs import ParserPaper
import re

__author__ = ''
__maintainer__ = 'Nicolas Mingione'
__email__ = 'nicolasmingione@lbl.gov'
__version__ = '0.3.0'


class ACSRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper
        list_remove = [
            {'name': 'ref-list'},
            {'name': 'xref', 'ref-type': 'bibr'},
            {'name': 'table-wrap'},
            {'name': 'fig'},
        ]
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml

class ACSCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class ACSReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        parser.change_name_tag_sections()
        return parser.raw_xml

class ACSReformat(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper(new_xml, parser_type='lxml',debugging=False)
        return parser.raw_xml

class ACSCollect(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        # Collect information from the paper using ParserPaper
        try:
            journal_name = next(x for x in parser.get(rules=[{"name": "journal-title"}]))
        except StopIteration:
            journal_name = None

        parser.get_title(rules=[
            {'name': 'article-title'}
        ]
        )
        doi = parser.get(rules=[
            {'name': 'article-id',
            'pub-id-type': 'doi'}
        ])

        keywords = parser.get(rules=[
            {'name':'kwd'}
        ])


        parser.deal_with_sections()
        data = parser.data_sections
        parser.create_abstract(rule={'name': 'abstract'})
        if len(data) == 1:
            parser.soup.front.decompose()
            parser.soup.back.decompose()
            body = parser.soup.find_all('p')
            for paras in body:
                p = re.sub('\n*\s+\n*',' ',paras.text.strip())
                p = re.sub('\s,\s',', ',p)
                p = re.sub('\s.\s','. ',p)
                if p[-1] == '.' and p[-2] == ' ':
                    p = p[:-2] + '.'
                data.append(parser.create_section(name='', type_section='section_h2', content=[p]))

        obj = {
            'DOI': doi,
            'Keywords': keywords,
            'Title': parser.title,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


ACSSoup = Soup(parser_version=__version__)
ACSSoup.add_ingredient(ACSReformat())
ACSSoup.add_ingredient(ACSRemoveTrash())
# ACSSoup.add_ingredient(ACSCreateTags())
ACSSoup.add_ingredient(ACSReplaceSectionTag())
ACSSoup.add_ingredient(ACSCollect())
