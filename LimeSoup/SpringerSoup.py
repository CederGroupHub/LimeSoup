#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_springer import ParserPaper


__author__ = 'Alex van Grootel'
__maintainer__ = 'Alex van Grootel'
__email__ = 'agrootel@mit.edu'
__version__ = '0.2.2'


class SpringerFindJournalName(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [
            {'name': 'span', 'class':'JournalTitle'}
        ]
        ParserPaper.journal_name = parser.get(rules)
        return parser.raw_html


class SpringerRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [#{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'sup'},
                 {'name': 'em', 'class': 'EmphasisTypeItalic '},
                 {'name': 'strong', 'class': 'EmphasisTypeBold '}
                # {'name': 'span', 'class': 'small_caps'},
                ]
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


class SpringerRemoveTrash(RuleIngredient):
    # TODO: error in two papers: 10.1039/B802997K - 10.1039/B717130G, some heading inside a span tag:
    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'div', 'class': 'Table'},  # Table
            {'name': 'div', 'class': 'HeaderArticleNotes'},  # submitted date
            {'name': 'p', 'class': 'skip-to'}, # Navigation links
            {'name': 'header', 'class': 'header u-interface'}, #search
            {'name': 'p', 'class': 'icon--meta-keyline-before'}, #published date and info
            {'name': 'h2', 'class': 'Heading u-jsHide'}, #Authors title
            {'name': 'ul', 'class': 'composite-layer authors'}, #Authors
            {'name': 'div', 'class': 'article-context__container'}, #article context
            {'name': 'div', 'class': 'banner'}, #search
            {'name': 'aside', 'class': 'article-complementary-left'}, #Journal images
            # {'name': 'div', 'class': 'ArticleHeader article-context'}, #article header
            {'name': 'figure', 'class': 'Figure'}, #Figures
            {'name': 'aside', 'class': 'article-about'}, #About paper
            {'name': 'aside', 'class': 'article-complementary-right u-interface'}, #Article actions
            {'name': 'footer', 'class': 'footer'}, #Article footer
            {'name': 'div', 'class': 'ArticleCopyright content'}, #Copyright
            {'name': 'h2', 'id': 'copyrightInformation'}, #copyright title
            {'name': 'div', 'class': 'Acknowledgments'}, #Acknowledgements
            {'name': 'aside', 'class': 'Bibliography'}, #Acknowledgements
        ]
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}]
        )
        return parser.raw_html

class SpringerCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_sections()
        return parser.raw_html


class SpringerCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Create tag from selection function in ParserPaper
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_from_selection(
            rule={'name': 'section', 'class': 'Abstract'},
            name_new_tag='h2'
        )
        # Guess introductions
        parser.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'section_h1'},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        return parser.raw_html


class SpringerReplaceDivTag(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'div'}]
        parser.strip_tags(rules)
        rules = [{'name': 'span', 'id': parser.compile('^sect[0-9]+$')}]  # some span are heading
        _ = parser.strip_tags(rules)
        return parser.raw_html

class SpringerReplaceDivTagPara(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = {'name': 'div', 'class': 'Para'}
        parser.rename_tag(rules, 'p')
        return parser.raw_html

class SpringerCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        # parser.get_keywords(rules=[{'name': 'li', 'class': 'kwd'}])
        # journal_name = parser.get([{'name': 'a', 'title': 'Link to journal home page'}])
        parser.get_title(rules=[
                {'name': 'h1', 'class' :'ArticleTitle', 'recursive': True},
            ]
        )
        # Create tag from selection function in ParserPaper
        data = list()
        
        parser.deal_with_sections()
        data = parser.data_sections
        
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': ParserPaper.journal_name,
            'Sections': data
        }

        return {'obj': obj, 'html_txt': parser.raw_html}


"""
Error where the paper has paragraphs (content) that is not inside of a tag,
problem to recover these paragraphs. 
"""
SpringerSoup = Soup(parser_version=__version__)
SpringerSoup.add_ingredient(SpringerFindJournalName())
SpringerSoup.add_ingredient(SpringerRemoveTagsSmallSub())
SpringerSoup.add_ingredient(SpringerRemoveTrash())
SpringerSoup.add_ingredient(SpringerCreateTags())
SpringerSoup.add_ingredient(SpringerCreateTagAbstract())
SpringerSoup.add_ingredient(SpringerReplaceDivTag())
SpringerSoup.add_ingredient(SpringerReplaceDivTagPara())
SpringerSoup.add_ingredient(SpringerCollect())