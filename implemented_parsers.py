'''
Implementations of the ParserPaper for ECS and RSC!
'''

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Feb 20 2018"

from parser_paper import ParserPaper

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
            {'name':'div' , 'class_':'section-nav'},     # Navigation bottons
            {'name':'div' , 'class_':'contributors'},    # Authors
            {'name':'span' , 'class_':'disp-formula'},   # Formulas
            {'name':'code'},                             # Codes inside the HTML
            {'name':'div', 'class_':'fig pos-float odd'},# Figures
            {'name':'div', 'id':'ref-list-1'},           # References
            {'name':'span' , 'class_':'disp-formula'},   # Formulas
            {'name':'span', 'class_':'kwd-group-title'}, # Keyword lables
            {'name':'div', 'class_':'table-caption'},    # Caption Table
            {'name':'div', 'class_':'table-inline'},     # Table in line
            {'name':'div', 'id':'fn-group-1'}            # Footnotes   
        ]
        self._remove_tags(rules=list_remove)
        # Save the soup after cleaning, to test and check
        if debugging:
            self.save_soup_to_file(
                filename='after_cleaning.html',
                prettify=True
            )
        # This create a standard of sections tag name  
        self._change_name_tag_sections()
        self._get_keywords(rules=[{'name':'li','class_':'kwd'}])
        self._get_title(rules = [
                            {'name':'h1', 'recursive':True},
                            {'name':'h2', 'class_':'subtitle', 'recursive':True}
                                             ]
        )
        # Create a copy of the soup to obtain some information after parser
        if debugging:
            self.soup_orig = self.create_soup(
                html_xlm=raw_html,
                parser_type='html.parser'
            )
        #Parameters of sections parameters from standard
        parameters = {'name':self.compile('^section_h[1-6]'),'recursive':False}
        parse_section =  self.create_parser_setion(self.soup, parameters)
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


class ParserRSC(ParserPaper):
        
    def __init__(self, raw_html, debugging=False):
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = self.create_soup(
            html_xlm=raw_html,
            parser_type='html.parser'
        )
        # Tags to be removed from the HTML paper ECS 
        list_remove = [
            {'name':'p', 'class_':'header_text'},        # Authors
            {'name':'div', 'id':'art-admin'},            # Data rec./accept.
            {'name':'div', 'class_':'image_table'},      # Figures
            {'name':'a', 'class_':'simple'},             # Logo
            {'name':'div', 'id':'crossmark-content'},    # Another Logo
            {'name':'code'},                             # Codes inside the HTML
        ]
        self._remove_tags(rules=list_remove)
        # Save the soup after cleaning, to test and check
        if debugging:
            self.save_soup_to_file(
                filename='after_cleaning.html',
                prettify=True
            )
        # This create a standard of sections tag name  
        self._create_tag_sections()
        self._create_tag_from_selection(
            rule={'name':'p', 'class':'abstract'},
            name_new_tag='h2'
        )
        self.save_soup_to_file(filename='new_sections.html', prettify=True)
        
        self._get_keywords(rules=[{'name':'li','class_':'kwd'}])
        self._get_title(rules = [
                {'name':'h1', 'recursive':True},
                {'name':'h2', 'class_':'subtitle', 'recursive':True}
            ]
        )
        # Create a copy of the soup to obtain some information after parser
        if debugging:
            self.soup_orig = self.create_soup(
                html_xlm=raw_html,
                parser_type='html.parser'
            )
        # Parameters of sections parameters from standard
        parameters = {'name':self.compile('^section_h[1-6]'),'recursive':False}
        parse_section =  self.create_parser_setion(self.soup, parameters)
        self.data_sections = parse_section.data
        self.headings_sections = parse_section.heading
        self.number_paragraphs_sections = parse_section.number_paragraphs 
        self.soup = parse_section.soup
        if debugging:
            self.save_soup_to_file(
                filename='file_after_parseHTML.html',
                prettify=True
            )
        del parse_section

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        filename = 'debug_RSC/{}'.format(filename)
        ParserPaper.save_soup_to_file(self,
            filename=filename,
            prettify=prettify
        )