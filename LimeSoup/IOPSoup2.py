#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_IOP2 import ParserPaper


__author__ = ''
__maintainer__ = 'Nicolas Mingione'
__email__ = 'nicolasmingione@lbl.gov'
__version__ = '0.3.0'


class IOPRemoveTrash(RuleIngredient):
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

class IOPCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class IOPReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml', debugging=False)
        parser.change_name_tag_sections()
        return parser.raw_xml

class IOPReformat(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper(new_xml, parser_type='lxml',debugging=False)
        return parser.raw_xml

class IOPCollect(RuleIngredient):

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
        parser.deal_with_sections()
        data = parser.data_sections
        parser.create_abstract(rule={'name': 'abstract'})

        obj = {
            'DOI': doi,
            'Keywords': [],
            'Title': parser.title,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


IOPSoup2 = Soup(parser_version=__version__)
IOPSoup2.add_ingredient(IOPReformat())
IOPSoup2.add_ingredient(IOPRemoveTrash())
IOPSoup2.add_ingredient(IOPCreateTags())
IOPSoup2.add_ingredient(IOPReplaceSectionTag())
IOPSoup2.add_ingredient(IOPCollect())


# if __name__ == '__main__':
#     filename = "RCR_84_9_981.xml"
#     with open(filename, "r", encoding="utf-8") as f:
#         paper = f.read()

#     parsed_paper = IOPSoup2.parse(paper)
#     for key in parsed_paper:
#         print(key, ":", parsed_paper[key])
#     print(parsed_paper )
    # data = parsed_paper["obj"] 
