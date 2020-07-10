import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.paragraphs import extract_paragraphs_recursive
from LimeSoup.parser.parser_paper import ParserPaper

__author__ = 'Zheren Wang'
__maintainer__ = ''
__email__ = 'zherenwang@berkeley.edu'
__version__ = '0.1.0'


class AIPRemoveTrash(RuleIngredient):
    """
    Selects the article div and removes all of the excess (ie. the sidebar,
    etc). Also strips the items listed below.
    """

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Tags to be removed from the HTML paper
        list_remove = [
            {'name': 'div', 'class': ['figure', 'figure-image-content']},  # Figures
            {'name': 'code'},  # Code inside the HTML
            {'name': 'div', 'class': 'tableWrapper'},  # Tables
            {'name': 'div', 'class': 'table-article'},  # Tables
            {'name': 'div', 'class': 'NLM_table'},  # Tables
            {'name': 'span', 'class': 'ref-lnk'},  # Ref Link
            {'name': 'div', 'class': 'ack'},  # Acknowledgement
            {'name': 'div', 'class': 'NLM_sec-type_appendix'},  # Appendix
            {'name': 'div', 'class': 'article-paragraphs'},  # References
        ]
        parser.remove_tags(rules=list_remove)

        return parser


class AIPCollectMetadata(RuleIngredient):
    """
    Collect metadata such as Title, Journal Name, DOI.
    """

    @staticmethod
    def _parse(parser):
        trim = lambda tag: re.sub(r'(^[\s\n]+)|([\s\n]+$)', '', tag)
        
        # This dictionary structure should match other parsers,
        # "Valid Article" and "Content Type" are specific to AIP Parser
        title = parser.get_first_title([{'name': 'header', 'class': 'publicationContentTitle'}])
        title = trim(title)

        # meta info includes journal & doi
        meta_info = parser.soup.find(**{'name': 'div', 'class': 'publicationContentCitation'}).strings
        meta_info = map(trim, meta_info)
        journal = next(meta_info)

        doi = None
        
        # search for DOI
        for each in meta_info:
            doi_ = re.search(r'(?<=https://doi.org/).+', each)
            if doi_ is not None:
                doi = doi_.group()
                doi = trim(doi)
                break

        if doi is None:
            raise ValueError("Cannot find doi.")
        
        # keywords
        keywords = parser.get_keywords([{'name': 'li', 'class': 'topicTags'}])
        
        obj = {
            'DOI': doi,
            'Title': title,
            'Journal': journal,
            'Keywords': keywords
        }

        return obj, parser


class AIPCleanArticleBody(RuleIngredient):
    @staticmethod
    def _parse(parser_obj):
        """
        Find the article body, then remove some tags
        """
        obj, parser = parser_obj

        # old style
        article_body = parser.soup.find(**{'name': 'article', 'class': 'article'})
        # new style
        if article_body is None:
            article_body = parser.soup.find(**{'name': 'div', 'class': 'left-article'})
        if article_body is None:
            raise ValueError('Cannot find article body')
        parser = ParserPaper(str(article_body), parser_type='html.parser')

        rules = [
            {'name': 'div', 'class': 'abstractInFull'},
            {'name': 'div', 'class': 'sectionInfo'},
            {'name': 'named-content'},
        ]
        parser.strip_tags(rules)

        # deal with listgroup
        rules = [
            {'name': 'table', 'class': 'listgroup'}
        ]
        parser.flatten_tags(rules)

        # deal with formula
        rules = [
            {'name': 'span', 'class': 'equationTd'},
            {'name': 'table', 'class': 'formula-display'}
        ]
        parser.flatten_tags(rules)

        # sub title
        rules = {'name': 'div', 'class': 'head-b'}
        parser.rename_tag(rules, 'h4')

        # sub sub title
        rules = {'name': 'div', 'class': 'head-c'}
        parser.rename_tag(rules, 'h4')

        # abstract header is not in h4 tag
        rules = {'name': 'div', 'class': 'sectionHeading'}
        parser.rename_tag(rules, 'h4')

        print(parser.raw_html)

        return obj, parser


class AIPCollect(RuleIngredient):
    @staticmethod
    def _parse(parser_obj):
        obj, parser = parser_obj

        # Parse abstract
        abstract_body = parser.soup.find(**{'name': 'div', 'class': 'hlFld-Abstract'})
        abstract = extract_paragraphs_recursive(abstract_body)

        for each in abstract:
            each['type'] = 'abstract'
        
        # Full text
        full_text_body = parser.soup.find(**{'name': 'div', 'class': 'hlFld-Fulltext'})
        if full_text_body is not None:
            full_text = extract_paragraphs_recursive(full_text_body)
        else:
            full_text = []

        # remove indexes
        data = abstract + list(full_text)
        for i, sec in enumerate(data):
            # for sections that have no title
            if isinstance(sec, str):
                data[i] = {
                    'type': '',
                    'name': '',
                    'content': sec
                }

        def remove_indexes(sections):
            """
            remove indexes in section header
            """
            # include number, greek number and capital char
            indexes_pattern = re.compile(r'^([A-z0-9]+)(\.|\s)(\s)+')
            for sec in sections:
                if isinstance(sec, dict):
                    sec['name'] = re.sub(indexes_pattern, '', sec['name'])
                    remove_indexes(sec['content'])

        remove_indexes(data)

        obj.update({'Sections': data})

        return obj


AIPSoup = Soup(parser_version=__version__)
AIPSoup.add_ingredient(AIPRemoveTrash())
AIPSoup.add_ingredient(AIPCollectMetadata())
AIPSoup.add_ingredient(AIPCleanArticleBody())
AIPSoup.add_ingredient(AIPCollect())
