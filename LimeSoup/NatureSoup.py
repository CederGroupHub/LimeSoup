#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re
import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.implemented_parsers import ParserNature


__author__ = 'Jason Madeano'
__maintainer__ = 'Jason Madeano'
__email__ = 'Jason.Madeano@shell.com'

# TODO: Some articles only have abstract (or title). These articles are only viewable as pdf

class InvalidArticleException(Exception):
    '''
    This exception should be raised whenever the article seems to be invalid. The dataset
    seems to have many articles that are news/reviews rather than journal articles and
    there are also quite a few articles that were improperly downloaded and lack html content.
    '''

    def __init__(self):
        exc = 'This appears to be either an empty journal article or a news/review article.'
        Exception.__init__(self, exc)


class NatureRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserNature(html_str, debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'b'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'a', 'data-track-action':'figure anchor'},
                 {'name': 'a', 'data-track-action':'supplementary material anchor'}]

        # First manually delete all 'sup's that include reference numbers
        [s.extract() for s in parser.soup.find_all('sup') if s.find('a')]
        #[s.extract() for s in parser.soup.find_all('sup') if s.find('a', {'data-track-action':'reference anchor'})]

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
        parser = ParserNature(html_str, debugging=False)
        return parser.raw_html


class NatureRemoveTrash(RuleIngredient):
    '''
    Selects the article div and removes all of the excess (ie. the sidebar,
    Nature contact info, etc). Also strips the items listed below.
    '''
    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'li', 'itemprop':'citation'},  # Citations/References
            {'name': 'div', 'id': 'article-comments-section'},  # Comments
            {'name': 'figure'},  # Figures
            {'name': 'code'}  # Code inside the HTML
        ]
        parser = ParserNature(html_str, debugging=False)

        # Only take 'main' article component: filter out header, sidebar, etc
        parser.soup = parser.soup.find('div', role = 'main')

        if parser.soup is None:
            raise InvalidArticleException()

        parser.remove_tags(rules=list_remove)

        return parser.raw_html


class NatureCollect(RuleIngredient):

    @staticmethod
    def parse(html_str):
        parser = ParserNature(html_str, debugging=False)
        # Collect DOI, Journal Name and Title from the paper using ParserPaper

        try:        #This is for newer articles (2000-present)
            DOI_link = parser.get([{'name':'a', 'data-track-action':'view doi'}]) #https://doi.org/10.1038/srep30829
            DOI = "/".join(DOI_link.split('/')[-2:]) #converts link to DOI:     above => 10.1038/srep30829
            article_flag = 0

        except AttributeError:  #This is for older articles
            try:
                article_flag = 1
                DOI_link = parser.soup.find(True, {'data-component':'article-info-list'})
                DOI = str(DOI_link.find('abbr').nextSibling).strip()[1:]
            except Exception as e:
                raise InvalidArticleException()

        parser.set_title()
        parser.set_keywords()
        journal_name = parser.get([{'name':'i'}])

        data = list()

        # Navigate to the actual article body
        article_body = parser.soup.find('div', class_ = 'article-body clear')

        if article_body.section is None:
            raise InvalidArticleException()

        for section in article_body.find_all("section"):
            try:
                section_title = parser.get_section_title(section.div)
                # print(f'TITLE:{section_title}')

            # News/Review articles do not have section headers, will not be parsed
            except Exception as e:
                print(f"Section Title ERROR: {e}")
                raise InvalidArticleException()
                break

            # Stop collecting data once any of these sections are reached
            if section_title.lower() in ['references', 'additional information',
                                         'change history', 'author information']:
                if data == []:
                    raise InvalidArticleException()
                break

            section_content = parser.deal_with_section(section.div, article_flag)
            data += [{"name": section_title, "content": section_content}]

        obj = {
            'DOI': DOI,
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj}#, 'html_txt':parser.raw_html}

NatureSoup = Soup()
NatureSoup.add_ingredient(NatureRemoveTagsSmallSub())
NatureSoup.add_ingredient(NatureRemoveTrash())
NatureSoup.add_ingredient(NatureCollect())
