#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_elsevier import ParserPaper


__author__ = ''
__maintainer__ = 'Nicolas Mingione'
__email__ = 'nicolasmingione@lbl.gov'


class ElsevierRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper
        list_remove = [{'name': 'xocs:meta'},
                       {'name': 'tail'},
                       {'name': 'ce:cross-refs'},
                       {'name': 'ce:cross-ref'}]
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml

class ElsevierSpaceBeforeFormula(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.parse_formula(rules=[{'name': 'formula'}])
        return parser.raw_xml

class ElsevierCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class ElsevierMoveJournalName(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.move_journal_name(rule={'name': 'xocs:srctitle'})
        except:
            pass
        return parser.raw_xml


class ElsevierCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.create_abstract(rule={'name': 'dc:description'})
        except:
            pass
        return parser.raw_xml


class ElsevierReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.strip_tags(rules=[{'name': 'ce:section'}])
        except:
            pass
        return parser.raw_xml

class ElsevierRenameSectionTitleTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        try:
            parser.rename_tag({'name': 'section-title'}, 'section_title')
        except:
            pass
        return parser.raw_xml

class ElsevierReformat(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper(new_xml, parser_type='lxml-xml',debugging=False)
        return parser.raw_xml

class ElsevierCollect(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'ce:keyword'}])
        journal_name = parser.get([{'name': 'ce:srctitle'}])
        parser.get_title(rules=[
            {'name': 'ce:title'}
        ]
        )
        try:
            # Create tag from selection function in ParserPaper
            parser.deal_with_sections()
            data = parser.data_sections
        except: # If Elsevier gives only the abstract OR gives only the raw text
            data = []
            try:
                abstract = parser.get_abstract(rule={'name': 'dc:description'})
                if len(abstract) > 0:
                    data.append(abstract)
            except:
                pass
            try:
                raw_text = parser.raw_text(rule={'name': 'xocs:rawtext'})
                if len(raw_text) > 0:
                    data.append(raw_text)
            except:
                pass
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj, 'xml_txt': parser.raw_xml}


ElsevierSoup = Soup(parser_version='0.2.2')
ElsevierSoup.add_ingredient(ElsevierReformat())
ElsevierSoup.add_ingredient(ElsevierSpaceBeforeFormula())
ElsevierSoup.add_ingredient(ElsevierMoveJournalName())
ElsevierSoup.add_ingredient(ElsevierCreateTagAbstract())
ElsevierSoup.add_ingredient(ElsevierRemoveTrash())
ElsevierSoup.add_ingredient(ElsevierCreateTags())
ElsevierSoup.add_ingredient(ElsevierReplaceSectionTag())
ElsevierSoup.add_ingredient(ElsevierRenameSectionTitleTag())
ElsevierSoup.add_ingredient(ElsevierCollect())
