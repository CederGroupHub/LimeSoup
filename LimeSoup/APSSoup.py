#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_aps import ParserPaper
import re


__author__ = ''
__maintainer__ = 'Haihao Liu'
__email__ = 'hhliu@mit.edu'
__version__ = '0.2'


class APSRemoveTrash(RuleIngredient):
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

class APSCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        # try:
            # This create a standard of sections tag name
        parser.create_tag_sections()
        # except:
        #     pass
        return parser.raw_xml

class APSReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        parser.change_name_tag_sections()
        return parser.raw_xml

class APSReformat(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper(new_xml, parser_type='lxml',debugging=False)
        return parser.raw_xml

class APSCollect(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        # Collect information from the paper using ParserPaper
        journal_name = parser.get(rules=[{"name": "journal-title"}])
        parser.get_title(rules=[
            {'name': 'article-title'}
        ]
        )
        doi = parser.get(rules=[
            {'name': 'article-id',
            'pub-id-type': 'doi'}
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
            'DOI': doi[0],
            'Keywords': [],
            'Title': parser.title,
            'Journal': journal_name[0],
            'Sections': data
        }
        return {'obj': obj, 'xml_txt': parser.raw_xml}


APSSoup = Soup(parser_version=__version__)
APSSoup.add_ingredient(APSReformat())
APSSoup.add_ingredient(APSRemoveTrash())
# APSSoup.add_ingredient(APSCreateTags())
APSSoup.add_ingredient(APSReplaceSectionTag())
APSSoup.add_ingredient(APSCollect())
