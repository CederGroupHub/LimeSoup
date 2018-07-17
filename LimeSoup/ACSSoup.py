#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_acs import ParserPaper


__author__ = ''
__maintainer__ = 'Nicolas Mingione'
__email__ = 'nicolasmingione@lbl.gov'


class ACSRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper
        list_remove = [{'name': 'ref-list'}]
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml

class ACSCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class ACSCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.create_abstract(rule={'name': 'abstract'})
        except:
            pass
        return parser.raw_xml


class ACSReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.strip_tags(rules=[{'name': 'sec'}])
        except:
            pass
        return parser.raw_xml

class ACSRenameSectionTitleTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.rename_tag({'name': 'section-title'}, 'section_title')
        except:
            pass
        return parser.raw_xml

class ACSReformat(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper(new_xml, parser_type='lxml-xml',debugging=False)
        return parser.raw_xml

class ACSCollect(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        # Collect information from the paper using ParserPaper
        journal_name = parser.get([{'name': 'journal-title'}])
        parser.get_title(rules=[
            {'name': 'article-title'}
        ]
        )
        doi = parser.get(rules=[{'name': 'article-id'}])
        print (doi)
        print (parser.title)
        try:
            # Create tag from selection function in ParserPaper
            parser.deal_with_sections()
            data = parser.data_sections
        except: # If Elsevier gives only the abstract OR gives only the raw text
            data = []
            try:
                abstract = parser.get_abstract(rule={'name': 'abstract'})
                if len(abstract) > 0:
                    data.append(abstract)
            except:
                pass
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj, 'xml_txt': parser.raw_xml}


ACSSoup = Soup()
# ACSSoup.add_ingredient(ACSReformat())
# ACSSoup.add_ingredient(ACSCreateTagAbstract())
# ACSSoup.add_ingredient(ACSRemoveTrash())
# ACSSoup.add_ingredient(ACSCreateTags())
# ACSSoup.add_ingredient(ACSReplaceSectionTag())
# ACSSoup.add_ingredient(ACSRenameSectionTitleTag())
ACSSoup.add_ingredient(ACSCollect())
