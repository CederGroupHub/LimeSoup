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
import re

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
        # self.error_message = ''
        # self.DOI, self.journal, self.type = None, None, None

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

    # Most Nature articles don't have keywords, default to []
    def set_keywords(self):
        keywords = self.soup.find('meta', {'name':'keywords'})
        self.keywords = keywords['content'].split(', ') if keywords else []

    def set_title(self):
        self.title = self.get([{'itemprop':'name headline'}])

    @staticmethod
    def get_section_title(section_div):
        return section_div.find('h2').get_text(strip=True).replace('\n', ' ')

    @staticmethod
    def deal_with_section(section_div, article_flag=0):
        """
        :param section_div: current section from which to extract subheadings and text
        :param article_flag: boolean (set during DOI extraction) - There are different
                                                    extraction method for older articles.
        return: (Example format below)

        Without section_sub_title:
        {
            "type": "section_h2"
            "name": "Section Title"
            "content": [
                "Paragraph 1 Content",
                "Paragraph 2 Content"
            ]
        }

        With section_sub_title (nested):
        {
            "type": 'section_h2'
            "name": "Section Title"
            "content": [
                {
                    "type": "section_h3"
                    "name": "Sub-Section 1"
                    "content": [
                        "Paragraph 1 Content",
                        "Paragraph 2 Content"
                    ]
                },
                {
                    "type": "section_h3"
                    "name": "Sub-Section 1"
                    "content": [
                        "Paragraph 1 Content",
                        "Paragraph 2 Content"
                    ]
                }
            ]
        }
        """

        content_div = section_div.div
        content = []

        section_sub_title = content_div.h3
        pattern = re.compile(r' \( .*? \)| \(ref\..*? \)')

        # If there are no section_sub_tiles, convert all <p> in section to text
        if section_sub_title is None:
            for paragraph in content_div.find_all(['p']):
                string = paragraph.get_text(' ', strip=True).replace('\n', ' ')
                string = re.sub(pattern, '', string) # Remove references: ( Fig. 4 )

                content.append(string)

        else: # Otherwise iterate through both <h3> and <p> and parse by subsection
            nested = []
            text = []

            for item in content_div.find_all(['p', 'h3'])[1:]:
                if text != [] and item.name == 'h3':
                    nested += [{"type": "section_h3",
                                "name": section_sub_title.get_text(strip=True).replace('\n', ' '),
                                "content": text}]

                    section_sub_title = item
                    text = []

                else:
                    string = item.get_text(' ', strip=True).replace('\n', ' ')
                    string = re.sub(pattern, '', string) # Remove references: ( Fig. 4 )


                    text.append(string)

            content.append(nested)

        return content


        # # These are now both taken care of in the NatureCollectMetadata Ingredient
    # def is_letter_or_article(self):
    #     '''
    #     Scrape the article type and check if it is a Letter or Article. All other
    #     types (ie Books and Art, News and Views, Correspondence, etc.) seem to
    #     be useless. Return whether the file is Article/Letter.
    #     '''
    #     try:
    #         type = self.soup.find('p', {'data-test':'article-identifier'})
    #
    #         if type is None:    # Different years have different type specifications
    #             type = self.soup.find('h1', {'class':'page-header'})
    #
    #         if type is None:    # These three options seem to cover > 90% of articles
    #             type = self.soup.find('p', {'class':'article-type'}).string
    #         else:
    #             type = type.get_text(strip=True)
    #             type = type.split('|', 1)[0].strip()
    #
    #         # print(f'Article:{article}\nType:{type}\n')
    #         return type in ['Letter', 'Article']
    #
    #     except Exception as e:
    #         print(e)
    #         return False
    #
    #
    # def collect_metadata(self, valid_article):
    #     '''
    #     Collect metadata from file. Set parser.DOI and parser.journal_name
    #     for use outside of the function. Return False if there were errors.
    #
    #     :param valid_article: (boolean) Is the article valid (so far)?
    #
    #     return valid_article: False if there was DOI/journal collection error
    #     '''
    #
    #     self.DOI = self.soup.find('meta', {'name':'dc.identifier'})
    #     self.journal = self.soup.find('meta', {'name':'WT.cg_n'})
    #
    #     if self.DOI is None:
    #         self.DOI = self.soup.find('meta', {'name':'citation_doi'})
    #
    #     if self.journal is None:
    #         print("There was a journal error.\n")
    #         valid_article = False
    #
    #     elif self.DOI is None:
    #         print("There was a DOI error.\n")
    #         self.journal = self.journal['content']
    #         valid_article = False
    #
    #     else:
    #         self.DOI, self.journal = self.DOI['content'][4:], self.journal['content']
    #
    #     return valid_article

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        filename = 'debug_Nature/{}'.format(filename)
        ParserPaper.save_soup_to_file(self,
                                      filename=filename,
                                      prettify=prettify
                                      )
