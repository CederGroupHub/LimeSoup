'''
ParserPaper is a class to parser html, xml papers from different publisher
into simples text. It can be used to feed a database.
This is a first version, I tried to separate things 
related with a specific publisher in the ParsePaper in order to help
to think how to reuse code in new publishers.
This class is not yet finished, just a securit copy in github..
'''

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Feb 18 2018"


#from abc import ABCMeta  
import itertools
import warnings
import re

import bs4


def convert_to_text(text_input):
    # import unicodedata
    text = text_input.rstrip()
    # text =  unicodedata.normalize('NFKD', text_input).encode('ascii','ignore')
    text = ' '.join(str(text).split())
    return text
        
        
class ParserPaper(object):
    
    def __init__(self, raw_html, debugging=False):
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = bs4.BeautifulSoup('{:}'.format(raw_html), 'lxml-xml')
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
            self.soup_orig = bs4.BeautifulSoup(
                '{:}'.format(str(self.soup)),
                'lxml-xml'
            )
        #Parameters of sections parameters from standard
        parameters = {'name':re.compile('^section_h[1-6]'),'recursive':False}
        parse_section = ParserSections(self.soup, parameters)
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
        
    def save_soup_to_file(self, filename='soup.html', prettify=True):
        with open(filename, 'w', encoding='utf-8') as fd_div:
            if (prettify == True):
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                for item in self.soup:
                    fd_div.write(item)    
                    fd_div.write('\n')
                    
    def _get_title(self, rules):
        self.title = []
        for rule in rules:
            title = self.soup.find_all(**rule)
            for item_title in title:
                text = convert_to_text(item_title.get_text())
                self.title.append(text)      
                item_title.extract()
        
    def _get_keywords(self, rules):
        self.keywords = []
        for rule in rules:
            for keyword in self.soup.find_all(**rule):
                self.keywords.append(convert_to_text(keyword.get_text()))
                keyword.extract() 
      
    def _remove_tags(self, rules): 
        for rule in rules:    
            [s.extract() for s in self.soup.find_all(**rule)]
                
    @property
    def headings(self):
        if (not self.debugging): 
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_heading_soup = self.soup_orig.find_all(name=re.compile('^h[2-6]$'))  
        list_heading = []
        for item in list_heading_soup:
            list_heading.append(item.get_text())
        return list_heading
    
    @property
    def paragraphs(self):
        if (not self.debugging): 
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_paragraphs_soup = self.soup_orig.find_all(name=re.compile('p'))  
        list_paragraphs = []
        for item in list_paragraphs_soup:
            list_paragraphs.append(item.get_text())
        return list_paragraphs
    
    def number_of_parafraphs_inside_paramters(self, parameters):
        if (not self.debugging): 
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        soup_sec = self.soup_orig.find_all(parameters)
        number_of_paragraphs_soup_sec = 0                                
        for it in soup_sec:
            number_of_paragraphs_soup_sec += len(list(
                it.find_all('p',recursive=False)
            ))
        print(' number paragraphs inside div class section and sub: ',
              number_of_paragraphs_soup_sec)
        
    def number_of_paragraphs_children(self): 
        if (not self.debugging): 
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        number_of_paragraphs_children = len(list(list(
            self.soup_orig.children)[0].find_all('p', recursive=True)
            )
        )
        print(' Number of Paragraphs externo : ', number_of_paragraphs_children)
            
    
    def _create_tag_sections(self):
        tag_names = ['h{}'.format(i) for i in range(1,6)] 
        for tag_name in tag_names:
            tags = self.soup.find_all(tag_name)
            for each_tag in tags:
                inside_tags = [item for item in itertools.takewhile(
                          lambda t: t.name not in [each_tag.name, 'script'],
                          each_tag.next_siblings)]
                section = self.soup.new_tag('section_{}'.format(tag_name))
                each_tag.wrap(section)
                for tag in inside_tags:
                    section.append(tag)
        
    def _change_name_tag_sections(self):     
        tags = self.soup.find_all(re.compile('^h[2-6]'))
        for each_tag in tags:
            each_tag.parent.name = 'section_{}'.format(each_tag.name)
     
              
            
class ParserSections(object):
    
    number_paragraphs = 0
    number_heading = 0
    list_heading =[]
    
    def __init__(self, soup, parameters, debugging=False):
        self.var_title = []
        parsertypes = ['html.parser', 'lxml', 'html5lib', 'lxml-xml']
        self.soup = bs4.BeautifulSoup(repr(soup), parsertypes[-1])
        self.soup1 = list(self.soup.children)
        if (len(self.soup1)!=1):
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
                if (self.content.name != None):
                    if (self.sub_section_name in self.content.name): 
                        self._create_sub_division()
                    else:
                        self._deal()
        self.data.append(self.content_section)
                           
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
        if (self.content_section == None):   
            self._create_section()
            warnings.warn(
                " Section with no name - deal_p "
                + "the name was defined as no_name_section"
            )
        ParserSections.number_paragraphs += 1
        txtParagraph = convert_to_text(self.content.get_text())
        if (txtParagraph != '' or txtParagraph == None):
            self.content_section['content'].append(txtParagraph) 
        self.content.extract()
            
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
        name_section = convert_to_text(self.content.get_text())
        if (self.content_section != None):   
            self.data.append(self.content_section)
        self._create_section(name=name_section, 
                             type_section=self.content.parent.name
                             )
        ParserSections.list_heading.append(name_section)
        ParserSections.number_heading += 1
        self.content.extract()  
           
    def _wrap_bs(self, to_wrap, wrap_in):
        contents = to_wrap.replace_with(wrap_in)
        wrap_in.append(contents)
             
    def _create_sub_division(self):
        if (self.content_section == None):   
            self._create_section()
            warnings.warn(
                " Section with no name - _deal_div "
                + "the name was defined as no_name_section"
            )
        # create a parent aux-tag  
        self._wrap_bs(self.content, self.soup.new_tag('aux-tag'))
        parse_intern = ParserSections(self.content.parent, self.parameters)
        self.content_section['content'].append(parse_intern.data)
        del parse_intern
        self.content.extract()
    
    def _deal_default(self):
        ParserSections.number_paragraphs += len(list(self.content.find_all('p')))
        txtParagraph = convert_to_text(self.content.get_text()) 
        if (self.content_section == None):   
            self._create_section()
            warnings.warn(
                " Section with no name - _deal_default "
                + "the name was defined as no_name_section"
            )
        if txtParagraph != '':
            self.content_section['content'].append(txtParagraph)
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
            if (prettify == True):
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                for item in self.soup:
                    fd_div.write(item)    
                    fd_div.write('\n')
            
    def _create_section(self, name='no_name_section', type_section='no_type'):
        self.content_section = {
                                'type': type_section 
                                ,'name': name
                                ,'content': []
                                }
