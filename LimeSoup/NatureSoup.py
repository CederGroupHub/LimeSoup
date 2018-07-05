#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re, bs4, json

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
                 {'name': 'i'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'}]

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
            {'name': 'code'},  # Code inside the HTML
            {'name': 'div', 'class': 'figure-at-a-glance'}, # Copy of all figures
            {'name': 'a', 'data-track-action':'figure anchor'}, # Figure Link
            {'name': 'a', 'data-track-action':'supplementary material anchor'} # Supplementary Link
        ]
        parser = ParserNature(html_str, debugging=False)

        # # Only take 'main' article component: filter out header, sidebar, etc
        # parser.soup = parser.soup.find('div', role = 'main')
        # if parser.soup is None:
        #     raise InvalidArticleException()

        parser.remove_tags(rules=list_remove)

        return parser.raw_html



class NatureCollectMetadata(RuleIngredient):
    '''
    Collect metadata such as Title, Journal Name, DOI and Content Type.
    '''

    @staticmethod
    def _parse(html_str):
        parser = ParserNature(html_str, debugging=False)
        error_message, valid_article = '', True # Assume no error
        doi, journal, title, type = None, None, None, None

        try:
            # The majority of nature articles have a script tag that contains
            # all of the valuable metadata in structure json format.
            pattern = re.compile(r'.*dataLayer.*')
            script = parser.soup.find('script', text = pattern)

            if script:
                script = script.get_text()

                # Extract the correct script and convert to python dictionary
                dict = re.search('\[(.*)\]', script)
                dict = dict.group(1)
                dict = json.loads(dict)['content']

                doi = dict['article']['doi']
                journal = dict['category']['legacy']['webtrendsContentGroup']
                title = dict['contentInfo']['title']
                type = dict['category']['contentType']

            else: # Some articles don't include script, but the metadata still exists
                doi = parser.soup.find('meta', {'name':'dc.identifier'})
                title = parser.soup.find('meta', {'name':'dc.title'})
                journal = parser.soup.find('meta', {'name':'WT.cg_n'})
                type = parser.soup.find('meta', {'name': 'WT.cg_s'})

                if doi: doi = doi['content'][4:]
                if title: title = title['content']
                if journal: journal = journal['content']
                if type: type = type['content'].lower()

                # Some articles have improperly downloaded HTML, these are flagged
                if doi is None or type is None:
                    error_message = "Error: Try Redownloading HTML File"
                    # os.startfile(article)

            if type and type not in ['letter', 'article']:
                error_message = "Error: Not Letter/Article"

        except Exception as e:
            print(e)
            error_message = "THERE WAS AN ERROR HERE"

        if error_message:
            valid_article = False
            title = error_message

        obj = {
            'Valid Article': valid_article,
            'Content Type': type.lower(),
            'DOI': doi,
            'Title': [title],
            'Keywords': [parser.keywords],
            'Journal': journal,
            'Sections': []
        }

        return [obj, parser.raw_html]


class NatureCollect(RuleIngredient):

    @staticmethod
    def _parse(parser_obj):

        obj, html_str = parser_obj
        parser = ParserNature(html_str, debugging=False)

        # No need to parse further if the article is invalid
        valid_article = obj['Valid Article']
        if not valid_article: return obj

        print("VALID)
        # parser.set_title()
        parser.set_keywords()

        data = list()

        # Navigate to the actual article body
        article_body = parser.soup.find('div', {'class': 'article-body clear'})

        if article_body is None or article_body.section is None:
            raise InvalidArticleException()
            valid_article = False

        for section in article_body.find_all("section"):
            try:
                section_title = parser.get_section_title(section.div)
                # print(f'TITLE:{section_title}')

            # News/Review articles do not have section headers, will not be parsed
            except Exception as e:
                print(f"Section Title ERROR: {e}")
                raise InvalidArticleException()
                valid_article = False
                break

            # Stop collecting data once any of these sections are reached
            if section_title.lower() in ['references', 'additional information',
                                         'change history', 'author information']:
                if data == []:
                    print("No Data ERROR")
                    raise InvalidArticleException()
                    valid_article = False
                break

            section_content = parser.deal_with_section(section.div)
            data += [{"type": "section_h2",
                      "name": section_title,
                      "content": section_content}]

        obj['Valid Article'] = valid_article
        obj['Keywords'] = parser.keywords
        obj['Sections'] = data

        # obj = {
        #     'Valid Article': valid_article,
        #     'DOI': parser.DOI,
        #     'Title': [parser.title],
        #     'Keywords': parser.keywords,
        #     'Journal': parser.journal,
        #     'Sections': data
        # }
        return obj#, 'html_txt':parser.raw_html}

NatureSoup = Soup()
NatureSoup.add_ingredient(NatureRemoveTagsSmallSub())
NatureSoup.add_ingredient(NatureRemoveTrash())
NatureSoup.add_ingredient(NatureCollectMetadata())
NatureSoup.add_ingredient(NatureCollect())
