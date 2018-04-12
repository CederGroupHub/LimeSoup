#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_elsevier import ParserPaper


__author__ = 'Ziqin (Shaun) Rong, Tiago Botari'
__maintainer__ = 'Nicolas Mingione'
__email__ = 'nicolasmingione@lbl.gov'


class ElsevierRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper ECS
        list_remove = [{'name': 'xocs:meta'},
                       {'name': 'tail'}]
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml


class ElsevierCreateTags(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        # This create a standard of sections tag name
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.create_tag_sections()
        return parser.raw_xml

class ElsevierMoveJournalName(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.move_title(rule={'name': 'xocs:srctitle'})
        return parser.raw_xml


class ElsevierCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.create_abstract(rule={'name': 'dc:description'})
        return parser.raw_xml


class ElsevierReplaceSectionTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.strip_tags(rules=[{'name': 'ce:section'}])
        return parser.raw_xml

class ElsevierRenameSectionTitleTag(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper(xml_str, parser_type='lxml-xml', debugging=False)
        parser.rename_tag({'name': 'section-title'}, 'section_title')
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
        # Create tag from selection function in ParserPaper
        parser.deal_with_sections()
        data = parser.data_sections
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj, 'xml_txt': parser.raw_xml}


"""
Error where the paper has paragraphs (content) that is not inside of a tag,
problem to recover these paragraphs. 
"""
ElsevierSoup = Soup()
ElsevierSoup.add_ingredient(ElsevierMoveJournalName())
ElsevierSoup.add_ingredient(ElsevierCreateTagAbstract())
ElsevierSoup.add_ingredient(ElsevierRemoveTrash())
ElsevierSoup.add_ingredient(ElsevierCreateTags())
ElsevierSoup.add_ingredient(ElsevierReplaceSectionTag())
ElsevierSoup.add_ingredient(ElsevierRenameSectionTitleTag())
ElsevierSoup.add_ingredient(ElsevierCollect())
