#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper import ParserPaper


__author__ = 'Jason Madeano'
__maintainer__ = 'Jason Madeano'
__email__ = 'Jason.Madeano@shell.com'

# TODO: If there is an equation image splitting a paragraph,
       #it is registered as 2 distict paragraphs

def get_text_and_subheadings(section_div):
    '''
    This helper will likely be implemented as a static method for the parser class but I
    am currently working on getting a fully functional product before refactoring
    '''

    content_div = section_div.div
    content = []

    section_sub_title = content_div.h3

    # If there are no section_sub_tiles, convert all <p> in section to text
    if section_sub_title is None:
        for item in content_div.find_all(['p']):
            content.append(item.get_text(strip=True))

    else: # Otherwise iterate through both <h3> and <p> and parse by subsection
        nested = []
        text = []

        for item in content_div.find_all(['p', 'h3'])[1:]:
            if text != [] and item.name == 'h3':
                nested += [{"name": section_sub_title.get_text(strip=True), "content": text}]
                section_sub_title = item
                text = []

            else:
                text.append(item.get_text(strip=True))

        content.append(nested)

    return content


## TODO: Implement NatureParser Class that has more relevant helper methods

# class ParserNature(ParserPaper):
#
#     def __init__(self, raw_html, debugging=False):
#         self.debugging = debugging
#         # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
#         self.soup = self.create_soup(
#             html_xlm=raw_html,
#             parser_type='html.parser'
#         )
#         # Tags to be removed from the HTML paper ECS
#         list_remove = [
#             {'name': 'p', 'class_': 'header_text'},  # Authors
#             {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
#             {'name': 'div', 'class_': 'image_table'},  # Figures
#             {'name': 'a', 'class_': 'simple'},  # Logo
#             {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
#             {'name': 'code'},  # Codes inside the HTML
#         ]
#         self._remove_tags(rules=list_remove)
#         # Save the soup after cleaning, to test and check
#         if debugging:
#             self.save_soup_to_file(
#                 filename='after_cleaning.html',
#                 prettify=True
#             )
#         # This create a standard of sections tag name
#         self._create_tag_sections()
#         self._create_tag_from_selection(
#             rule={'name': 'p', 'class': 'abstract'},
#             name_new_tag='h2'
#         )
#         self.save_soup_to_file(filename='new_sections.html', prettify=True)
#
#         self._get_keywords(rules=[{'name': 'li', 'class_': 'kwd'}])
#         self._get_title(rules=[
#             {'name': 'h1', 'recursive': True},
#             {'name': 'h2', 'class_': 'subtitle', 'recursive': True}
#         ]
#         )
#         # Create a copy of the soup to obtain some information after parser
#         if debugging:
#             self.soup_orig = self.create_soup(
#                 html_xlm=raw_html,
#                 parser_type='html.parser'
#             )
#         # Parameters of sections parameters from standard
#         # parameters = {'name': self.compile('^section_h[1-6]'), 'recursive': False}
#         # parse_section = self.create_parser_setion(self.soup, parameters)
#         # self.data_sections = parse_section.data
#         # self.headings_sections = parse_section.heading
#         # self.number_paragraphs_sections = parse_section.number_paragraphs
#         # self.soup = parse_section.soup
#         if debugging:
#             self.save_soup_to_file(
#                 filename='file_after_parseHTML.html',
#                 prettify=True
#             )
#         # del parse_section



class NatureRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 # {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'a', 'data-track-action':'figure anchor'},
                 {'name': 'a', 'data-track-action':'supplementary material anchor'}]

        # First manually delete all 'sup's that include reference numbers
        [s.extract() for s in parser.soup.find_all('sup') if s.find('a', {'data-track-action':'reference anchor'})]

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
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.soup = parser.soup.find('div', role = 'main')
        parser.remove_tags(rules=list_remove)

        return parser.raw_html

class NatureCollect(RuleIngredient):

    @staticmethod
    def parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect DOI, Jounal Name and Title from the paper using ParserPaper


        DOI_link = parser.get([{'name':'a', 'data-track-action':'view doi'}])[0] #https://doi.org/10.1038/srep30829
        DOI = "/".join(DOI_link.split('/')[-2:]) #converts link to DOI:           above => 10.1038/srep30829

        journal_name = parser.get([{'name':'i'}])[0]

        parser.get_title([{'itemprop':'name headline'}])

        data = list()

        # Navigate to the actual article body
        article_body = parser.soup.find('div', class_ = 'article-body clear')

        for section in article_body.find_all("section"):

            section_title = section.div.h2.get_text(strip=True)
            # print(f'TITLE:{section_title}')

            # Stop collecting data once any of these sections are reached
            if section_title.lower() in ['references', 'additional information', 'change history']:
                break

            try:
                section_content = get_text_and_subheadings(section.div)

            except AttributeError:
                print(section_title)
                content = "ERROR"
                break

            data += [{"name": section_title, "content": section_content}]

        obj = {
            'DOI': DOI,
            'Title': parser.title,
            'Keywords': 'NA',
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj}#, 'html_txt':parser.raw_html}
        # return parser.raw_html

NatureSoup = Soup()
NatureSoup.add_ingredient(NatureRemoveTagsSmallSub())
NatureSoup.add_ingredient(NatureRemoveTrash())
NatureSoup.add_ingredient(NatureCollect())
