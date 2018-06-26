#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re
import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Jason Madeano'
__maintainer__ = 'Jason Madeano'
__email__ = 'Jason.Madeano@shell.com'


## TODO: Implement NatureParser Class that has more relevant helper methods

class ParserNature(ParserPaper):

    def __init__(self, raw_html, debugging=False):
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = self.create_soup(
            html_xlm=raw_html,
            parser_type='html.parser'
        )

        # # Save the soup after cleaning, to test and check
        # if debugging:
        #     self.save_soup_to_file(
        #         filename='after_cleaning.html',
        #         prettify=True
        #     )

    # Return first matching result
    def get(self, rules):
        for rule in rules:
            find = self.soup.find(**rule)
            return find.get_text(strip=True)

    # Return all matching results
    def get_all(self, rules):
        results = list()
        for rule in rules:
            finds = self.soup.find_all(**rule)
            for item in finds:
                text = item.get_text(strip=True)
                results.append(text)
        return results

    # Nature articles don't have keywords
    def set_keywords(self):
        self.keywords = []

    def set_title(self):
        self.title = self.get([{'itemprop':'name headline'}])

    @staticmethod
    def get_section_title(section_div):
        return section_div.find('h2').get_text(strip=True)

    @staticmethod
    def deal_with_section(section_div, article_flag):
        """
        :param section_div: current section from which to extract subheadings and text
        :article_flag: boolean (set during DOI extraction) - Older articles have excess '\n'

        return (Example format below)

        Without section_sub_title:
        {
            "content": [
                "Paragraph 1 Content",
                "Paragraph 2 Content"
            ],
            "name": "Section Title"
        }

        With section_sub_title (nested):
        {
            "content": [
                {
                    "content": [
                        "Paragraph 1 Content",
                        "Paragraph 2 Content"
                    ],
                    "name": "Sub-Section 1"
                },
                {
                    "content": [
                        "Paragraph 1 Content",
                        "Paragraph 2 Content"
                    ],
                    "name": "Sub-Section 2"
                }
            ],
            "name": "Section Title"
        }


        """

        content_div = section_div.div
        content = []

        section_sub_title = content_div.h3

        # If there are no section_sub_tiles, convert all <p> in section to text
        if section_sub_title is None:
            for paragraph in content_div.find_all(['p']):
                string = paragraph.get_text(strip=True)

                if article_flag:
                    string = string.replace('\n', ' ')

                content.append(string)

        else: # Otherwise iterate through both <h3> and <p> and parse by subsection
            nested = []
            text = []

            for item in content_div.find_all(['p', 'h3'])[1:]:
                if text != [] and item.name == 'h3':
                    nested += [{"name": section_sub_title.get_text(strip=True), "content": text}]
                    section_sub_title = item
                    text = []

                else:
                    string = item.get_text(strip=True)

                    if article_flag:
                        string = string.replace('\n', ' ')

                    text.append(string)

            content.append(nested)

        return content


    # # Create a copy of the soup to obtain some information after parser
    # if debugging:
    #     self.soup_orig = self.create_soup(
    #         html_xlm=raw_html,
    #         parser_type='html.parser'
    #     )
    #
    # if debugging:
    #     self.save_soup_to_file(
    #         filename='file_after_parseHTML.html',
    #         prettify=True
    #     )

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        filename = 'debug_RSC/{}'.format(filename)
        ParserPaper.save_soup_to_file(self,
                                      filename=filename,
                                      prettify=prettify
                                      )

class NatureRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """

        try:
            parser = ParserNature(html_str, debugging=False)
            rules = [{'name': 'small'},
                     {'name': 'sub'},
                     {'name': 'span', 'class': 'small_caps'},
                     {'name': 'b'},
                     # {'name': 'sup'},
                     {'name': 'span', 'class': 'italic'},
                     {'name': 'span', 'class': 'bold'},
                     {'name': 'strong'},
                     {'name': 'span', 'class': 'small_caps'},
                     {'name': 'a', 'data-track-action':'figure anchor'},
                     {'name': 'a', 'data-track-action':'supplementary material anchor'}]

            # First manually delete all 'sup's that include reference numbers
            # [s.extract() for s in parser.soup.find_all('sup') if s.find('a', {'data-track-action':'reference anchor'})]
            [s.extract() for s in parser.soup.find_all('sup') if s.find('a')]

                # Note this has issues for some downloads (ie C:\Users\Jason\Desktop\nature_htmls\10103835081034.html)

        except AttributeError:
            print('WARNING: This is a news article. Parsing will not work.')


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
            # {'name': 'div', 'id': 'additional-information-section'}
        ]
        parser = ParserNature(html_str, debugging=False)
        parser.soup = parser.soup.find('div', role = 'main')
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

        except AttributeError:

            try:    #This is for older articles
                article_flag = 1
                DOI_link = parser.soup.find('ul', {'data-component':'article-info-list'})
                DOI = str(DOI_link.find('abbr').nextSibling).strip()[1:]

            except Exception as e:
                print(f"ERROR: {e}")
                print("This is a news article rather than journal entry. Please input new file.")
                DOI = 'INVALID'


        parser.set_title()
        parser.set_keywords()
        journal_name = parser.get([{'name':'i'}])


        data = list()

        # Navigate to the actual article body
        article_body = parser.soup.find('div', class_ = 'article-body clear')

        for section in article_body.find_all("section"):

            try:
                section_title = parser.get_section_title(section.div)
                # print(f'TITLE:{section_title}')

            # News/Review articles do not have section headers, will not be parsed
            except Exception as e:
                print(f"ERROR: {e}")
                print("This is a news article rather than journal entry. Please input new file.")
                break

            # Stop collecting data once any of these sections are reached
            if section_title.lower() in ['references', 'additional information', 'change history']:
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
        # return parser.raw_html

NatureSoup = Soup()
NatureSoup.add_ingredient(NatureRemoveTagsSmallSub())
NatureSoup.add_ingredient(NatureRemoveTrash())
NatureSoup.add_ingredient(NatureCollect())
