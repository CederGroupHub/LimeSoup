"""
ParseSection part of ParserPaper is a class to parse HTML, XML papers from different publishers into
simples text. It can be used to feed a database.
This is the first version, I tried to separate things
related to a specific publisher in the ParsePaper in order to help
to think how to reuse code in new publishers.
This class is not yet finished, just a security copy in GitHub.
"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Mar 12 2018"

import itertools
import warnings
import re

import bs4

import LimeSoup.parser.tools as tl


class ParserSections(object):
    number_paragraphs = 0
    number_heading = 0
    list_heading = []

    def __init__(self, soup, parameters, debugging=False, parser_type='lxml-xml'):
        # parser_types = ['html.parser', 'lxml', 'html5lib', 'lxml-xml']
        self.parser_type = parser_type
        self.soup = bs4.BeautifulSoup(repr(soup), parser_type)
        self.soup1 = list(self.soup.children)
        if len(self.soup1) != 1:
            #self.save_soup_to_file('some_thing_wrong_chieldren.html')
            warnings.warn(' Some think is wrong in children!=1')
            exit()
        self.soup1 = self.soup1[0]
        self.parameters = parameters
        if debugging:
            self.save_soup_to_file('ParseHTML_initial.html', prettify=True)
        self.sub_section_name = 'section_h'
        self.paragraphs = list()
        self.content_section = None
        self.data = list()

        for item in self.soup1.find_all(**parameters):
            for content in item.contents:
                self.content = content
                if self.content.name is not None:  # deal with empty content
                    if self.sub_section_name in self.content.name:  # standard sections <section_h#>
                        self._create_sub_division()
                    else:
                        self._deal()
        self.data.append(self.content_section)
        lost_section = {
            'type': 'lost_content'
            , 'name': 'lost_content'
            , 'content': []
        }
        save_lost = False
        tags_lost = self.soup1.find_all()
        for tag in tags_lost:
            text1 = tl.convert_to_text(tag.get_text())
            if len(text1) > 0:
                save_lost = True
                lost_section['content'].append(text1)
            tag.extract()
        text1 = tl.convert_to_text(self.soup1.get_text())
        if len(text1) > 0:
            save_lost = True
            lost_section['content'].append(text1)
        if save_lost:
            self.data.append(lost_section)

    def _deal(self):
        method_name = '_deal_' + str(self.content.name)
        method_name_default = '_deal_default'
        method = getattr(
            self,
            method_name,
            getattr(self, method_name_default)
        )
        return method()

    def _deal_p(self):
        if self.content_section is None:
            self._create_section()
            warnings.warn(
                " Section with no name - deal_p "
                + "the name was defined as no_name_section"
            )
        ParserSections.number_paragraphs += 1
        txt_paragraph = tl.convert_to_text(self.content.get_text())
        if txt_paragraph != '' or txt_paragraph is None:
            self.content_section['content'].append(txt_paragraph)
        self.content.extract()

    def _deal_ul(self):
        self._deal_ol()

    def _deal_ol(self):
        list_ol = self.content.find_all('li')
        for item in list_ol:
            self.content = item
            self._deal_p()

    def _deal_h1(self):
        self._deal_h()

    def _deal_h2(self):
        self._deal_h()

    def _deal_h3(self):
        self._deal_h()

    def _deal_h4(self):
        self._deal_h()

    def _deal_h5(self):
        self._deal_h()

    def _deal_h(self):
        name_section = tl.convert_to_text(self.content.get_text())
        if self.content_section is not None:
            self.data.append(self.content_section)
        self._create_section(
            name=name_section,
            type_section=self.content.parent.name
        )
        # ParserSections.list_heading.append(name_section)
        # ParserSections.number_heading += 1
        self.content.extract()

    @staticmethod
    def _wrap_bs(to_wrap, wrap_in):
        contents = to_wrap.replace_with(wrap_in)
        wrap_in.append(contents)

    def _create_sub_division(self):
        if self.content_section is None:
            self._create_section()
            warnings.warn(
                " Section with no name - _deal_div "
                + "the name was defined as no_name_section"
            )
        # create a parent aux-tag
        self._wrap_bs(self.content, self.soup.new_tag('aux-tag'))
        parse_intern = ParserSections(self.content.parent, self.parameters, parser_type=self.parser_type)
        self.content_section['content'].append(parse_intern.data[0])
        del parse_intern
        self.content.extract()

    def _deal_default(self):
        ParserSections.number_paragraphs += len(list(self.content.find_all('p')))
        txt_paragraph = tl.convert_to_text(self.content.get_text())
        if self.content_section is None:
            self._create_section()
            warnings.warn(
                " Section with no name - _deal_default "
                + "the name was defined as no_name_section"
            )
        if txt_paragraph != '':
            self.content_section['content'].append(txt_paragraph)
        self.content.extract()

    @property
    def heading(self):
        lista = ParserSections.list_heading
        ParserSections.list_heading = []
        return lista

    @property
    def get_number_paragraphs(self):
        number_paragraphs = ParserSections.number_paragraphs
        ParserSections.number_paragraphs = 0
        return number_paragraphs

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        with open(filename, 'w', encoding='utf-8') as fd_div:
            if prettify:
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                for item in self.soup:
                    fd_div.write(item)
                    fd_div.write('\n')

    def _create_section(self, name='no_name_section', type_section='no_type'):
        self.content_section = {
            'type': type_section
            , 'name': name
            , 'content': []
        }

