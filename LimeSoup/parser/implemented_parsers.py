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
        if debugging:
            self.save_soup_to_file(
                filename='after_cleaning.html',
                prettify=True
            )
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
        parameters = {'name': self.compile('^section_h[1-6]'), 'recursive': False}
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
            {'name': 'p', 'class_': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class_': 'image_table'},  # Figures
            {'name': 'a', 'class_': 'simple'},  # Logo
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
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
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        self.save_soup_to_file(filename='new_sections.html', prettify=True)

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
        parameters = {'name': self.compile('^section_h[1-6]'), 'recursive': False}
        parse_section = self.create_parser_setion(self.soup, parameters)
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

class ParserNature(ParserPaper):

    def __init__(self, raw_html, debugging=False):
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = self.create_soup(
            html_xlm=raw_html,
            parser_type='html.parser'
        )

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

        return: (Example format below)

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
                string = paragraph.get_text(' ', strip=True)

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
                    string = item.get_text(' ', strip=True)

                    if article_flag:
                        string = string.replace('\n', ' ')

                    text.append(string)

            content.append(nested)

        return content

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        filename = 'debug_Nature/{}'.format(filename)
        ParserPaper.save_soup_to_file(self,
                                      filename=filename,
                                      prettify=prettify
                                      )
