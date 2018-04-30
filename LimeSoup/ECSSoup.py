#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


class ECSRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
                Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'em'}]
        # parser.operation_tag_remove_space(rules)
        # Remove some specific all span that are inside of a paragraph 'p'
        parser.strip_tags(rules)
        tags = parser.soup.find_all(**{'name': 'p'})
        for tag in tags:
            tags_inside_paragraph = tag.find_all(**{'name': 'span'})
            for tag_inside_paragraph in tags_inside_paragraph:
                tag_inside_paragraph.replace_with_children()
        # Remove some specific span that are inside of a span and p
        parser.strip_tags(rules)
        tags = parser.soup.find_all(**{'name': re.compile('span|p')})
        for tag in tags:
            for rule in rules:
                tags_inside_paragraph = tag.find_all(**rule)
                for tag_inside_paragraph in tags_inside_paragraph:
                    tag_inside_paragraph.replace_with_children()
        # Recreating the ParserPaper bug in beautifulsoup
        html_str = str(parser.soup)
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        return parser.raw_html


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
            {'name': 'div', 'id': 'license-1'},  # License
            {'name': 'ul', 'class': 'history-list'},  # some historical information of the paper
            {'name': 'ul', 'class': 'copyright-statement'}
        ]
        parser = ParserPaper(html_str, debugging=False)
        parser.remove_tags(rules=list_remove)
        rules = [
            {'name': 'span', 'class': 'highwire-journal-article-marker-start'},
            {'name': 'ul', 'class': 'epreprint-list'}
        ]

        parser.strip_tags(rules)
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
        obj['DOI'] = ''
        return {'obj': obj, 'html_txt': parser.raw_html}


class ECSCreateTags(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):
        html_str = parser_obj['html_txt']
        obj = parser_obj['obj']
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, debugging=False)
        parser.change_name_tag_sections()
        #  Create the Introduction section.
        parser.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'div', 'class': parser.compile('article fulltext-view')},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        return {'obj': obj, 'html_txt': parser.raw_html}


class ECSDealDivWithNoHeading(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):
        html_str = parser_obj['html_txt']
        obj = parser_obj['obj']
        parser = ParserPaper(html_str, debugging=False)
        #  Remove the content inside of empty div tags for ECS
        # TODO: Need to improve, the recovered paragraphs go to wrong section.
        rules = [
            {'name': 'div', 'class': 'subsection'},
            {'name': 'div', 'class': 'section'}
        ]
        for rule in rules:
            tags = parser.soup.find_all(**rule)
            for tag in tags:
                tag_close_sibling = tag
                while True:
                    tag_close_sibling = tag_close_sibling.previous_sibling
                    if tag_close_sibling is None:
                        break
                    if tag_close_sibling.name is None:
                        continue
                    if 'section_h' in tag_close_sibling.name:
                        tag_close_sibling.append(tag)
                        break
        parser.strip_tags(rules)
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
ECSSoup.add_ingredient(ECSRemoveTagsSmallSub())
ECSSoup.add_ingredient(ECSRemoveTrash())
ECSSoup.add_ingredient(ECSCollectTitleKeywords())
ECSSoup.add_ingredient(ECSCreateTags())
ECSSoup.add_ingredient(ECSDealDivWithNoHeading())
ECSSoup.add_ingredient(ECSCollect())

