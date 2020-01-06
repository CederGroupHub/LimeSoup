import re

from bs4 import BeautifulSoup

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_wiley import ParserPaper

__author__ = 'Zach Jensen'
__maintainer__ = ''
__email__ = 'zjensen@mit.edu'
__version__ = '0.3.0'

class WileyRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=True)
        rules = [{'name':'i'},
                 {'name':'sub'},
                 {'name':'sup'},
                 {'name':'b'}, 
                 {'name':'em'}]

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

class WileyRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        print('Here')
        list_remove = [
            {'name': 'div', 'class': 'loa-wrappers loa_authors hidden-xs'},
            {'name':'div', 'class':'article-header__authors-container'},  # Authors X
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept. 
            {'name': 'div', 'class': 'article-section__inline-figure'},
            {'name': 'section', 'class':'article-section article-section--inline-figure'},
            {'name':'figure'},  # Figures X
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class': 'article-table-content'},  # Remove table X
            {'name': 'header', 'class': 'page-header'}, # Navigation links X 
            {'name': 'div', 'class':'page-footer'},
            {'name':'div', 'class':'js-module notification'},
            {'name':'img'}, 
            {'name':'aside'},
            {'name':'div', 'class':'issue-header js-module'}, 
            {'name':'span', 'class':'article-header__category article-category'},
            {'name':'article-header__meta-info-container'},
            {'name':'a', 'class':'figZoom'},
            {'name':'ul', 'class':'meta-navigation u-list-plain'},
            {'name':'div', 'id':'js-article-nav'},
            {'name':'section', 'id':'pdf-section'},
            {'name':'section', 'class':'article-footer__section article-section'}, 
            {'name':'div', 'class':'l-article-support'}, 
            {'name':'footer', 'role':'contentinfo'}, 
            {'name':'div', 'data-module':'infoplane'},
            {'name':'header', 'role':'banner'},
            {'name':'header', 'class':'journal-header'},
            {'name':'div', 'class':'article-header__meta-info-container'},
            {'name':'div', 'class':'article-header__references-container'},
            {'name':'section', 'id':'footer-article-info'},
            {'name':'section', 'id':'related-content'},
            {'name':'section', 'id':'footer-citing'},
            {'name':'section', 'id':'footer-support-info'},
            {'name':'ul', 'class':'article-section__references-list-additional u-horizontal-list'}, # Remove Footnote X
            {'name':'a', 'class':'bibLink tab-link'}, # remove references
            {'name':'a', 'class':'link__reference js-link__reference'},
            {'name':'div', 'class':'loa-wrapper loa-authors hidden-xs'},
            {'name':'div', 'class':'rlist--inline loa comma visible-xs mobile-authors loa-authors-trunc'},
            {'name':'div', 'class':'readCube-sharing hidden'},
            {'name':'div', 'class':'modal__header'},
            {'name':'div', 'class':'modal__body'},
            {'name':'div', 'class':'readCube-sharing hidden'},
            {'name':'div', 'class':'ux-modal-container readCube-sharing__modal'},
            {'name':'div', 'class':'share__block dropBlock__holder fixed'},
            {'name':'div', 'class':'article-citation'},
            {'name':'span', 'class':'inline-equation__label'},
            {'name':'div', 'class':'accordion article-accordion'},
            {'name':'div', 'class':'table__overflow js-module'},

        ]
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}]
        )
        return parser.raw_html

class WileyCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_sections()
        return parser.raw_html

class WileyCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Create tag from selection function in ParserPaper
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_from_selection(
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        # Guess introductions
        #parser.create_tag_to_paragraphs_inside_tag(
        #  #   rule={'name': 'section_h1'},
        #     name_new_tag='h2',
        #     name_section='Introduction(guess)'
        # )
        return parser.raw_html

class WileyReplaceDivTag(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'div'}]
        parser.strip_tags(rules)
        rules = [{'name': 'span', 'id': parser.compile('^sect[0-9]+$')}]  # some span are heading
        _ = parser.strip_tags(rules)
        return parser.raw_html


class WileyCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        soup = BeautifulSoup(html_str, 'html.parser')
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        keywords = soup.find_all(attrs={'name':'citation_keywords'})
        keys = []
        for key in keywords:
            keys.append(parser.format_text(key.get('content')))
        journal_name = soup.find(attrs={'name':'citation_journal_title'})
        journal_name = parser.format_text(journal_name.get('content'))
        doi = soup.find(attrs={'name':'citation_doi'})
        doi = doi.get('content')
        title = soup.find(attrs={'name':'citation_title'})
        title = parser.format_text(title.get('content'))
        # Create tag from selection function in ParserPaper
        data = list()
        """
        Can deal with multiple Titles in the same paper
        """
        parser.deal_with_sections()
        data = parser.data_sections
        index2 = max(len(data)-1,1)
        check = ['Abstract', 'Acknowledgements', 'Experimental Section', 'Supporting Information']
        no_sections = True
        for d in data:
            if d['name'] not in check:
                no_sections = False
        if no_sections:
            section = soup.find_all('section')
            for sect in section:
                if (sect.get('class') is not None and ('article-section__full' in sect.get('class') or 
                    (isinstance(sect.get('class'), list) and len(sect.get('class'))>1 and 'article-body-section' in sect.get('class')[1]))):
                    paragraphs = sect.find_all('p')
                    for p in paragraphs:
                        skip = False
                        ul = p.find('ul')
                        if ul is not None and ul.get('class') is not None and 'rlist' in ul.get('class'):
                            skip = True
                        pars = p.parents
                        for par in pars:
                            if (par.get('class') is not None and ('supporting' in par.get('class') or 'references' in par.get('class') or 
                                    'citedby' in par.get('class'))):
                                skip = True
                        for d in data:
                            for c in d['content']:
                                if isinstance(c, str):
                                    if c == parser.format_text(p.text):
                                        skip = True
                                elif isinstance(c, dict):
                                    d2 = c['content']
                                    for c2 in d2:
                                        if isinstance(c2, str):
                                            if c2 == parser.format_text(p.text):
                                                skip = True
                                        elif isinstance(c2, dict):
                                            d3 = c2['content']
                                            for c3 in d3:
                                                if c3 == parser.format_text(p.text):
                                                    skip = True
                        if not skip:
                            text = parser.format_text(p.text)
                            # text = ''.join(filter(lambda x: x in string.printable, text)) Can be useful for formating but can remove characters
                            if text[-1] != '.':
                                index = text.rfind('.')
                                text = text[:index+1]
                            if text == data[-1]['content'][0]:
                                continue
                            obj = {
                                'type':'section_h2',
                                'name':'',
                                'content':[text]
                            }
                            data.insert(-1*index2, obj)
        obj = {
            'DOI': doi,
            'Title': title,
            'Keywords': keys,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


WileySoup = Soup(parser_version=__version__)
WileySoup.add_ingredient(WileyRemoveTagsSmallSub())
WileySoup.add_ingredient(WileyRemoveTrash())
WileySoup.add_ingredient(WileyCreateTags())
# WileySoup.add_ingredient(WileyCreateTagAbstract())
WileySoup.add_ingredient(WileyReplaceDivTag())
WileySoup.add_ingredient(WileyCollect())