#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class RSCRemoveTrash(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'p', 'class_': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class_': 'image_table'},  # Figures
            {'name': 'a', 'class_': 'simple'},  # Logo
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
        ]
        parser = ParserPaper(html_str, debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class_': 'bold italic', 'string': parser.compile('First')}]
        )
        return parser.raw_html


class RSCCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, debugging=False)
        parser.create_tag_sections()
        return parser.raw_html


class RSCCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Create tag from selection function in ParserPaper
        parser = ParserPaper(html_str, debugging=False)
        parser.create_tag_from_selection(
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        parser.save_soup_to_file('RSCCreateTagAbstract.html', prettify=True)
        return parser.raw_html


class RSCCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'li', 'class_': 'kwd'}])
        parser.get_title(rules=[
                {'name': 'h1', 'recursive': True},
                {'name': 'h2', 'class_': 'subtitle', 'recursive': True}
            ]
        )
        # Create tag from selection function in ParserPaper
        parameters = {'name': parser.compile('^section_h[1-6]'), 'recursive': False}
        parser.deal_with_sections(parameters)
        result = {
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Sections': parser.data_sections
        }
        return result


RSCSoup = Soup()
RSCSoup.add_ingredient(RSCRemoveTrash)
RSCSoup.add_ingredient(RSCCreateTags)
RSCSoup.add_ingredient(RSCCreateTagAbstract)
RSCSoup.add_ingredient(RSCCollect)

