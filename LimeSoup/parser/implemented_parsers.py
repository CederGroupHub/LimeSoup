'''
Implementations of the ParserPaper for ECS, RSC, and Nature!
The ParserPaper is an abstract class that can be used to create specific
publishers parser. ParserECS, PaperRSC, and ParserNature are implementations for ECS, RSC, and Nature.
'''

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Feb 20 2018"

import re

from LimeSoup.parser.parser_paper import ParserPaper


class ParserECS(ParserPaper):
    def __init__(self, raw_html, debugging=False):
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = self.create_soup(
            html_xlm=raw_html,
            parser_type='lxml-xml'
        )
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'div', 'class_': 'section-nav'},  # Navigation bottons
            {'name': 'div', 'class_': 'contributors'},  # Authors
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class_': 'fig pos-float odd'},  # Figures
            {'name': 'div', 'id': 'ref-list-1'},  # References
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'span', 'class_': 'kwd-group-title'},  # Keyword lables
            {'name': 'div', 'class_': 'table-caption'},  # Caption Table
            {'name': 'div', 'class_': 'table-inline'},  # Table in line
            {'name': 'div', 'id': 'fn-group-1'}  # Footnotes
        ]
        self._remove_tags(rules=list_remove)
        # Save the soup after cleaning, to test and check
        # if debugging:
        #     self.save_soup_to_file(
        #         filename='after_cleaning.html',
        #         prettify=True
        #     )
        # This create a standard of sections tag name
        self._change_name_tag_sections()
        self._get_keywords(rules=[{'name': 'li', 'class_': 'kwd'}])
        self._get_title(rules=[
            {'name': 'h1', 'recursive': True},
            {'name': 'h2', 'class_': 'subtitle', 'recursive': True}
        ]
        )
        # Create a copy of the soup to obtain some information after parser
        if debugging:
            self.soup_orig = self.create_soup(
                html_xlm=raw_html,
                parser_type='html.parser'
            )
        # Parameters of sections parameters from standard
        parameters = {'name': re.compile('^section_h[1-6]'), 'recursive': False}
        parse_section = self.create_parser_setion(self.soup, parameters)
        self.data_sections = parse_section.data
        self.headings_sections = parse_section.heading
        self.number_paragraphs_sections = parse_section.number_paragraphs
        self.soup = parse_section.soup
        if debugging:
            parse_section.save_soup_to_file(
                filename='file_after_parseHTML.html',
                prettify=True
            )
        del parse_section
