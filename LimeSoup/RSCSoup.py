import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.paragraphs import extract_paragraphs_recursive, get_tag_text
from LimeSoup.parser.parser_paper import ParserPaper

__author__ = 'Ziqin (Shaun) Rong, Tiago Botari, Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'haoyan.huo@lbl.gov'
__version__ = '0.2.3'


class RSCRemoveTagsSmallSub(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'}]
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

        return parser


class RSCRemoveTrash(RuleIngredient):
    # TODO: error in two papers: 10.1039/B802997K - 10.1039/B717130G, some heading inside a span tag:
    @staticmethod
    def _parse(parser):
        parser.remove_tags(rules=[
            {'name': 'p', 'class': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class': 'image_table'},  # Figures
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class': 'table_caption'},  # Remove table caption
            {'name': 'div', 'class': 'rtable__wrapper'},  # Remove table itself
            {'name': 'div', 'class': 'left_head'},  # Navigation links
            {'name': 'table'},  # Remove Footnote
            {'name': 'a', 'href': re.compile(r'#cit\d+')},  # Remove citations
            {'name': 'script'},
        ])
        parser.remove_first_tag(rules=[
            {'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}
        ])
        return parser


class RSCCreateTags(RuleIngredient):
    @staticmethod
    def _parse(parser):
        # This create a standard of sections tag name
        parser.create_tag_sections()
        return parser


class RSCCreateTagAbstract(RuleIngredient):
    @staticmethod
    def _parse(parser):
        # Create tag from selection function in ParserPaper
        parser.create_tag_from_selection(
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        # Guess introductions
        parser.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'section_h1'},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        return parser


class RSCCollect(RuleIngredient):
    @staticmethod
    def _parse(parser):
        """
        Collect metadata and sections from cleaned-up Paper structure.

        :type parser: LimeSoup.parser.parser_paper.ParserPaper
        :return:
        """
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'li', 'class': 'kwd'}])

        doi = parser.extract_first_meta('DC.Identifier')
        journal_name = parser.extract_first_meta('citation_journal_title')

        title_element = next(
            x for x in parser.soup.find_all(attrs={'class': 'title_heading'})
        )
        title = get_tag_text(title_element).strip('*†‡§‖¶')
        # title = parser.extract_first_meta('citation_title')

        # Create tag from selection function in ParserPaper
        data = list()

        exclude_sections = [
            re.compile(r'.*?acknowledgements.*?', re.IGNORECASE),
            re.compile(r'.*?references.*?', re.IGNORECASE),
        ]
        for item in parser.soup.find_all('section_h1'):
            for tag in item.find_all(**{'name': re.compile('^section_h[1-6]'), 'recursive': False}):
                data.extend(extract_paragraphs_recursive(
                    tag,
                    exclude_section_rules=exclude_sections
                ))

        obj = {
            'DOI': doi,
            'Title': title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return {'obj': obj, 'html_txt': parser.raw_html}


RSCSoup = Soup(parser_version=__version__)
RSCSoup.add_ingredient(RSCRemoveTagsSmallSub())
RSCSoup.add_ingredient(RSCRemoveTrash())
RSCSoup.add_ingredient(RSCCreateTags())
RSCSoup.add_ingredient(RSCCreateTagAbstract())
RSCSoup.add_ingredient(RSCCollect())
