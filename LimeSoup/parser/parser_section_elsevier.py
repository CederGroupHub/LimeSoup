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
__maintainer__ = "Nicolas Mingione"
__email__ = "nicolasmingione@lbl.gov"
__date__ = "Apr 11 2018"

import warnings
import bs4
import re

from LimeSoup.parser import tools as tl


class ParserSections(object):
    number_paragraphs = 0
    number_heading = 0
    list_heading = []

    def __init__(self, soup, parameters, debugging=False, parser_type='lxml-xml', new=False):
        # parser_types = ['xml.parser', 'lxml', 'xml5lib', 'lxml-xml']
        self.parser_type = parser_type
        self.soup = bs4.BeautifulSoup(repr(soup), parser_type)
        self.soup1 = list(self.soup.children)
        self.new = new
        if len(self.soup1) != 1:
            #self.save_soup_to_file('some_thing_wrong_children.xml')
            warnings.warn(' Something is wrong in children!=1')
            exit()
        self.soup1 = self.soup1[0]
        self.parameters = parameters
        if debugging:
            self.save_soup_to_file('ParseXML_initial.xml', prettify=True)
        self.sub_section_name = 'section_h'
        self.paragraphs = list()
        self.content_section = []
        self.data = list()
        #print(self.soup1)
        #print('The find_all returns',len(self.soup1.find_all(**parameters)),'results.')
        self.i = 0
        # for i,item in enumerate(self.soup1.find_all(**parameters)):
        #     print('=== item #',i,'==')
        #     print(item.name)
        #     for child in item:
        #         print('->',child.name)
        for i,item in enumerate(self.soup1.find_all(**parameters)):
            #print('===',i,'====')
            #print(item.name)
            if item.name is not None:
                if self.sub_section_name in item.name:
                    #print('IT\'S A HEADING!')
                    self.content_section.append({
                            'type': item.name,
                            'name': re.sub('(?<!\.)\\n','',item.section_title.get_text()),
                            'content': []
                            })
    
                    #print('Creation of self.content_section:',self.content_section)
            for content in item.contents:
                #print('===')
                #print(content.name)
                self.content = content
                if self.content.name is not None:  # deal with empty content
                    if self.sub_section_name in self.content.name:  # standard sections <section_h#>
                        #print('>>> It\'s a sub-heading. <<<')

                        self._create_sub_division()
                        content.extract()
                    else:
                        #print('>>> It\'s not a sub-heading <<<')
                        self._deal()
                        content.extract()
            self.i += 1
        self.data = self.content_section
        lost_section = {
            'type': 'lost_content'
            , 'name': 'lost_content'
            , 'content': []
        }
        save_lost = False
        tags_lost = self.soup.find_all()
        for tag in tags_lost:
            text1 = tl.convert_to_text(re.sub('(?<!\.)\\n','',tag.get_text()))
            if len(text1) > 0:
                save_lost = True
                lost_section['content'].append(text1)
            tag.extract()
        text1 = tl.convert_to_text(re.sub('(?<!\.)\\n','',self.soup1.get_text()))
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
        #print('Going into',method_name)
        return method()

    def _deal_para(self):
        if self.content_section is None:
            self._create_section()
            warnings.warn(
                " Section with no name - deal_para "
                + "the name was defined as no_name_section"
            )
        ParserSections.number_paragraphs += 1
        txt_paragraph = tl.convert_to_text(re.sub('(?<!\.)\\n','',self.content.get_text()))
        #print('The paragraph is', txt_paragraph)
        if txt_paragraph != '' or txt_paragraph is None:
            #print('We add it to the content_section')
            self.content_section[self.i]['content'].append(txt_paragraph)
        
    def _deal_abstract(self): #tmp

        pass
        
    def _deal_section_title(self): #tmp

        pass
        
    def _deal_label(self):

        pass

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
            print('No content_section yet, so we create one with the no_type')
        # create a parent aux-tag
        #self._wrap_bs(self.content, self.soup.new_tag('aux-tag'))
        aux_tag = self.soup.new_tag('aux-tag')
        self.content = self.content.wrap(aux_tag)
        #print(self.content)
        #print('Recurrence with TYPE:', self.content.name)
        parse_intern = ParserSections(self.content, self.parameters, parser_type=self.parser_type)
        #print('We get the first element of:',parse_intern.data)
        self.content_section[self.i]['content'].append(parse_intern.data[0])
        del parse_intern

    def _deal_default(self):
        #print('DEFAULT')
        ParserSections.number_paragraphs += len(list(self.content.find_all('ce:para')))
        txt_paragraph = tl.convert_to_text(re.sub('(?<!\.)\\n','',self.content.get_text()))
        if self.content_section is None:
            self._create_section()
            warnings.warn(
                " Section with no name - _deal_default "
                + "the name was defined as no_name_section"
            )
        if txt_paragraph != '':
            self.content_section[self.i]['content'].append(txt_paragraph)

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

    def save_soup_to_file(self, filename='soup.xml', prettify=True):
        with open(filename, 'w', encoding='utf-8') as fd_div:
            if prettify:
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                for item in self.soup:
                    fd_div.write(item)
                    fd_div.write('\n')

    def _create_section(self, name='no_name_section', type_section='no_type'):
        self.content_section.append({
            'type': type_section
            , 'name': name
            , 'content': []
        })

