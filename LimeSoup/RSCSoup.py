#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Ziqin (Shaun) Rong, Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


class RSCRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'}]
        parser.operation_tag_remove_space(rules)
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


class RSCRemoveTrash(RuleIngredient):
    # TODO: error in two papers: 10.1039/B802997K - 10.1039/B717130G, some heading inside a span tag:
    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'p', 'class': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class': 'image_table'},  # Figures
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class': 'table_caption'},  # Remove table caption
            {'name': 'div', 'class': 'rtable__wrapper'},  # Remove table itself
            {'name': 'div', 'class': 'left_head'}, # Navigation links
            {'name': 'table'},  # Remove Footnote
        ]
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}]
        )
        # file = open('LimeSoup/test/new_rsc_papers/test.html', 'w')
        # file.write(parser.raw_html)
        return parser.raw_html


class RSCCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_sections()
        # file2 = open('LimeSoup/test/new_rsc_papers/test2.html', 'w')
        # file2.write(parser.raw_html)
        return parser.raw_html


class RSCCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Create tag from selection function in ParserPaper
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_from_selection(
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        # Guess introductions
        parser.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'section_h1'},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        # file3 = open('LimeSoup/test/new_rsc_papers/test3.html', 'w')
        # file3.write(parser.raw_html)
        # x=y
        return parser.raw_html


class RSCReplaceDivTag(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'div'}]
        parser.strip_tags(rules)
        rules = [{'name': 'span', 'id': parser.compile('^sect[0-9]+$')}]  # some span are heading
        _ = parser.strip_tags(rules)
        return parser.raw_html


class RSCCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'li', 'class': 'kwd'}])
        journal_name = parser.get([{'name': 'a', 'title': 'Link to journal home page'}])
        parser.get_title(rules=[
                {'name': 'h1', 'recursive': True},
                {'name': 'h2', 'class': 'subtitle', 'recursive': True}
            ]
        )
        # Create tag from selection function in ParserPaper
        data = list()
        """
        Can deal with multiple Titles in the same paper
        """
        for i_item, item in enumerate(parser.soup.find_all('section_h1')):
            parser.soup = item
            parser.deal_with_sections()
            data += parser.data_sections
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj, 'html_txt': parser.raw_html}


"""
Error where the paper has paragraphs (content) that is not inside of a tag,
problem to recover these paragraphs. 
"""
RSCSoup = Soup()
RSCSoup.add_ingredient(RSCRemoveTagsSmallSub())
RSCSoup.add_ingredient(RSCRemoveTrash())
RSCSoup.add_ingredient(RSCCreateTags())
RSCSoup.add_ingredient(RSCCreateTagAbstract())
RSCSoup.add_ingredient(RSCReplaceDivTag())
RSCSoup.add_ingredient(RSCCollect())
