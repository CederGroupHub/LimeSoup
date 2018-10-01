"""
This ParserPaper is a class to parse XML papers from different publishers into
simples text. It can be used to feed a database.
"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Nicolas Mingione"
__email__ = "nicolasmingione@lbl.gov"
__date__ = "Apr 11 2018"

import warnings
import re

import bs4

# from LimeSoup.parser.parser_section_acs import ParserSections
from LimeSoup.parser import tools as tl


class ParserPaper:

    def __init__(self, raw_xml, parser_type='lxml', debugging=False):
        """
        :param raw_xml:
        :param parser_type: can be 'xml.parser', 'lxml', 'xml5lib', 'lxml-xml'
        :param debugging: True or False
        """
        self.debugging = debugging
        # parsers 'xml.parser', 'lxml', 'xml5lib', 'lxml-xml'
        self.soup = bs4.BeautifulSoup(raw_xml, parser_type)
        self.parser_type = parser_type
        self.title = []
        self.keywords = []
        self.data_sections = []
        self.headings_sections = []
        self.number_paragraphs_sections = []
        if debugging:
            self.soup_orig = self.soup

    def deal_with_sections(self):
        """
        Deal with the sections, parse tags that contains <'section_h#'>
        Ex: <'section_h2'>
        :return:
        """
        self.data_sections = []
        self.create_parser_sections(self.soup)
        # self.data_sections = parse_section.data
        # self.headings_sections = parse_section.heading
        # self.number_paragraphs_sections = parse_section.number_paragraphs
        # self.soup = parse_section.soup
        # del parse_section

    @staticmethod
    def compile(pattern):
        return re.compile(pattern)

    def create_section(self, name='no_name_section', type_section='no_type', content=[]):
       return {
            'type': type_section
            , 'name': name
            , 'content': content
        }


    def create_parser_sections(self, soup):
        search_str = re.compile('section_h[1-6]')
        section_tags = soup.find_all(search_str)
        
        # Get all sections
        for tag in section_tags:
            name = tag.find('title').text
            content = []
            for p in tag.find_all('p'):
                content.append(p.text)

            self.data_sections.append(self.create_section(
                name=name,
                type_section=tag.name,
                content=content
            ))

        # Nest data sections
        for i in range(6, 1, -1):
            did_nest = False
            secname = "section_h{}".format(i)
            supersec_name = "section_h{}".format(i-1)
            curr_sec_set = []
            for j, sec in enumerate(reversed(self.data_sections)):
                if sec['type'] == secname:
                    curr_sec_set.insert(0, sec)
                elif (sec['type'] == supersec_name) and curr_sec_set:
                    sec['content'] = curr_sec_set
                    curr_sec_set = []
                    did_nest = True

            if did_nest:
                self.data_sections = [s for s in self.data_sections if s['type'] != 'section_h{}'.format(i)]

            


    @staticmethod
    def create_soup(xml_xlm, parser_type='lxml'):
        # parser_types = ['xml.parser', 'lxml', 'xml5lib', 'lxml-xml']
        return bs4.BeautifulSoup(xml_xlm, parser_type)

    def save_soup_to_file(self, filename='soup.xml', prettify=True):
        """
        Save the soup to a file to be analysed. This can be used during the
        debugging process.
        :param filename: str that contain the name of the file
        :param prettify: boolean to add spaces on children tags
        :return: None - just save a file on disk
        """
        with open(filename, 'w', encoding='utf-8') as fd_div:
            if prettify:
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                for item in self.soup:
                    fd_div.write(item)
                    fd_div.write('\n')

    def get_title(self, rules):
        self.title = self.get(rules)

    def get(self, rules):
        results = list()
        for rule in rules:
            finds = self.soup.find_all(**rule)
            for item in finds:
                text = self.convert_to_text(item.get_text())
                results.append(text)
                item.extract()
        return results

    def parse_formula(self,rules):
        for rule in rules:
            finds = self.soup.find_all(**rule)
            for item in finds:
                label = item.find('id')
                if label is not None:
                    label.string = ' ' + label.string + ' '
                item.append(', ')

    def get_keywords(self, rules):
        self.keywords = []
        for rule in rules:
            for keyword in self.soup.find_all(**rule):
                self.keywords.append(keyword.get_text().strip('\n'))
                keyword.extract()

    def remove_tags(self, rules):
        """
        Remove tags from bs4 soup object using a list of bs4 rules to find_all()
        :param rules: list() of dict() of rules of bs4 find_all()
        :return: None
        """
        for rule in rules:
            [s.extract() for s in self.soup.find_all(**rule)]

    def remove_tag(self, rules):
        """
        Remove the first found tag from bs4 soup object using
        a list of bs4 rules to find_all() Remove the first tag.
        :param rules: rules: list() of dict() of rules of bs4 find_all()
        :return: None
        """
        for rule in rules:
            [s.extract() for s in self.soup.find_all(limit=1, **rule)]

    @property
    def headings_orig(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_heading_soup = self.soup_orig.find_all('sec')
        list_heading = []
        for item in list_heading_soup:
            list_heading.append(item.get_text())
        return list_heading

    @property
    def headings(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_heading_soup = self.soup.find_all('sec')
        list_heading = []
        for item in list_heading_soup:
            list_heading.append(self.convert_to_text(item.get_text()))
        return list_heading

    @property
    def paragraphs(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_paragraphs_soup = self.soup.find_all(name='p') # re.compile(
        list_paragraphs = []
        for item in list_paragraphs_soup:
            if len(self.convert_to_text(item.get_text())) != 0:
                item.string = self.convert_to_text(item.get_text())
                list_paragraphs.append(item.get_text())
        return list_paragraphs

    @property
    def paragraphs_orig(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_paragraphs_soup = self.soup_orig.find_all(name=re.compile('p'))
        list_paragraphs = []
        for item in list_paragraphs_soup:
            list_paragraphs.append(item.get_text())
        return list_paragraphs

    def number_of_paragraphs_inside_parameters(self, parameters):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        soup_sec = self.soup_orig.find_all(parameters)
        number_of_paragraphs_soup_sec = 0
        for it in soup_sec:
            number_of_paragraphs_soup_sec += len(list(
                it.find_all('p', recursive=False)
            ))
        # print(' number paragraphs inside div class section and sub: ',
        #      number_of_paragraphs_soup_sec)

    def number_of_paragraphs_children(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        number_of_paragraphs_children = len(list(list(
            self.soup_orig.children)[0].find_all('p', recursive=True)
                                                 )
                                            )
        # print(' Number of Paragraphs externo : ', number_of_paragraphs_children)

    def create_tag_from_selection(self, rule, name_new_tag, name_section='Abstract'):
        """
        Create a tag inside a bs4 soup object from a selection using a rule.
        :param rule: a dict() of rules of bs4 find_all()
        :param name_new_tag: new tag's name
        :param name_section: create a <h2> tag with the name_section content
        :return: None
        """
        inside_tags = self.soup.find_all(**rule)
        section = self.soup.new_tag('section_{}'.format(name_new_tag))
        heading = self.soup.new_tag('h2')
        heading.append(name_section)
        section.append(heading)
        for tag in inside_tags:
            tag.wrap(section)
            section.append(tag)
            
    def create_abstract(self, rule):
        """
        Create a section for the abstract
        """
        abstract = self.soup.find(**rule)
        if abstract is not None:
            self.data_sections.insert(0, self.create_section(
                    name='Abstract',
                    type_section='abstract',
                    content= abstract.get_text()
                ))

    def get_abstract(self, rule):
        """
        Get abstract when there is no body article
        """
        abstract = self.soup.find(**rule)
        if abstract is not None:
            abstract_text = re.sub('(?<!\.)\\n','',abstract.get_text())
            abstract_text = abstract_text.replace('Abstract', '')
            abstract_text = abstract_text.replace('\n','')
            abstract_text = abstract_text.replace('  ', '')
            abstract_dict = {
                            'type': 'section_h2',
                            'name': 'Abstract',
                            'content': [abstract_text]
                            }
            return abstract_dict

    def raw_text(self,rule):
        """
        Get the text with no format if ACS does not provide the sections hierarchy.
        """
        raw_text = self.soup.find(**rule)
        if raw_text is not None:
            raw_text_dict = {
                            'type': 'section_h2',
                            'name': 'Raw text',
                            'content': [raw_text.get_text()]
                            }
            return raw_text_dict       

    def create_tag_to_paragraphs_inside_tag(self, rule, name_new_tag, name_section='Abstract'):
        inside_tags_inter = self.soup.find_all(**rule)
        if len(inside_tags_inter) == 0:
            # self.save_soup_to_file('selction_found_nothing.xml')
            # input('Section not created, selection found nothing')
            return 'Section not created, number of paragraphs equal zero.'
        inside_tags = inside_tags_inter[0].find_all(re.compile('para'), recursive=False)
        #inside_tags = inside_tags_inter[0].find_all('p', recursive=False)
        #inside_tags_ol = inside_tags_inter[0].find_all('ol', recursive=False)
        #print(len(inside_tags_ol))
        #inside_tags = inside_tags_p + inside_tags_ol
        if len(inside_tags) == 0:
            # self.save_soup_to_file('selction_found_nothing.xml')
            # input('Section not created, number of paragraphs equal zero.')
            return 'Section not created, number of paragraphs equal zero.'
        section = self.soup.new_tag('section_{}'.format(name_new_tag))
        heading = self.soup.new_tag('h2')
        heading.append(name_section)
        section.append(heading)
        for tag in inside_tags:
            tag_next_sibling = tag
            while True:
                tag_next_sibling = tag_next_sibling.next_sibling
                if tag_next_sibling is None:
                    break
                if tag_next_sibling.name is None:
                    continue
                else:
                    break
            tag.wrap(section)
            section.append(tag)
            if tag_next_sibling is None: break
            if 'section_h' in tag_next_sibling.name:
                break


    def operation_tag_remove_space(self, rules):
        for rule in rules:
            tags = self.soup.find_all(**rule)
            for tag in tags:
                if tag is not None:
                    if tag.name is not None:
                        tag.string = tag.get_text().strip()

    def create_tag_sections(self, rule=None):
        """
        Create the standard tags (<section_h#>) using a rule to bs4 find_all()
        :param rule:
        :return:
        """
        tags = self.soup.find_all('sec')  # Tags corresponded to headings
        for each_tag in tags:
            # try:
            tag_name_tmp = each_tag.find('id').string
            #print('Tag:', each_tag.name, 'Label:', "%r"%tag_name_tmp)
            # To be consistent with the html parser, the notation h1, h2, ..., h6 is kept.
            tag_name = int(tag_name_tmp.count('.'))+2
            section = self.soup.new_tag('section_h{}'.format(tag_name))
            each_tag.wrap(section)
            # except:
            #     section = self.soup.new_tag('section_h0')
            #     each_tag.wrap(section)

    def rename_tag(self, rule, new_name='section_h4'):
        tags = self.soup.find_all(**rule)
        for tag in tags:
            tag.name = new_name

    def strip_tags(self, rules):
        """
        Replace some tag with the children tag.
        :param rules: list of rules for bs4 find_all()
        :return: None
        """
        tags = list()
        for rule in rules:
            for tag in self.soup.find_all(**rule):
                tag.replace_with_children()
                tags.append(tag.name)
        return tags

    def change_name_tag_sections(self):
        tags = self.soup.find_all('sec')
        for each_tag in tags:
            try:
                tag_name_tmp = each_tag['id']
                # To be consistent with the xml parser, the notation h1, h2, ..., h6 is kept.
                tag_name = int(tag_name_tmp.count('.'))+2
                each_tag.name = 'section_h{}'.format(tag_name)
            except:
                 each_tag.name = 'section_h2'

    @staticmethod
    def convert_to_text(text):
        text = text.replace("\n", " ")
        text = ' '.join(str(text).split())
        text = re.sub(r"\&(\w+?)gr;", r"\1", text)
        return text

    @property
    def raw_xml(self):
        return str(self.soup.prettify)

