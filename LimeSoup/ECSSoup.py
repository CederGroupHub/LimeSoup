#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


class ECSRemoveTrash(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper ECS
        obj = dict()
        list_remove = [
            {'name': 'div', 'class_': 'section-nav'},  # Navigation buttons
            {'name': 'div', 'class_': 'contributors'},  # Authors
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class_': 'fig pos-float odd'},  # Figures
            {'name': 'div', 'id': 'ref-list-1'},  # References
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'span', 'class_': 'kwd-group-title'},  # Keyword labels
            {'name': 'div', 'class_': 'table-caption'},  # Caption Table
            {'name': 'div', 'class_': 'table-inline'},  # Table in line
            {'name': 'div', 'id': 'fn-group-1'},  # Footnotes
            {'name': 'div', 'id': 'license-1'}  # License
        ]
        parser = ParserPaper(html_str, debugging=False)
        parser.remove_tags(rules=list_remove)
        return {'obj': obj, 'html_txt': parser.raw_html}


class ECSCollectTitleKeywords(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):
        html_str = parser_obj['html_txt']
        obj = parser_obj['obj']
        parser = ParserPaper(html_str, debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'li', 'class_': 'kwd'}])
        parser.get_title(rules=[
                {'name': 'h1', 'recursive': True},
                {'name': 'h2', 'class_': 'subtitle', 'recursive': True}
        ])
        obj['Title'] = parser.title
        obj['Keywords'] = parser.keywords
        return {'obj': obj, 'html_txt': parser.raw_html}


class ECSCreateTags(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):
        html_str = parser_obj['html_txt']
        obj = parser_obj['obj']
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, debugging=False)
        parser.change_name_tag_sections()
        parser.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'div', 'class': parser.compile('article fulltext-view')},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        # the follow line is to solve the problem of sections that contain only section
        parser.strip_tags(rules=[
            {'name': 'div', 'class': 'subsection'},
            {'name': 'div', 'class': 'section'}
        ])
        #parser.rename_tag(rule={'name': 'div', 'class': 'subsection'}, new_name='section_h4')
        parser.save_soup_to_file('test_inside_ECSSOUP.html')
        return {'obj': obj, 'html_txt': parser.raw_html}


class ECSCollect(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):
        html_str = parser_obj['html_txt']
        obj = parser_obj['obj']
        parser = ParserPaper(html_str, debugging=False)
        # Collect information from the paper using ParserPaper
        # Create tag from selection function in ParserPaper
        parser.deal_with_sections()
        obj['Sections'] = parser.data_sections
        return {'obj': obj, 'html_txt': parser.raw_html}


ECSSoup = Soup()
ECSSoup.add_ingredient(ECSRemoveTrash())
ECSSoup.add_ingredient(ECSCollectTitleKeywords())
ECSSoup.add_ingredient(ECSCreateTags())
ECSSoup.add_ingredient(ECSCollect())

