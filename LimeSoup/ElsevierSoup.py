import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.elsevier_xml import (
    resolve_elsevier_entities, extract_ce_text, find_non_empty_children,
    node_named, extract_ce_para, extract_ce_section, extract_ce_abstract
)

__author__ = 'Haoyan Huo, Nicolas Mingione'
__maintainer__ = 'Nicolas Mingione'
__version__ = '0.3.1-dev'


class ElsevierParseXML(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        xml_str = resolve_elsevier_entities(xml_str)
        return bs4.BeautifulSoup(xml_str, 'lxml-xml')


class ElsevierReadMetaData(RuleIngredient):
    @staticmethod
    def get_text_or_none(soup, name):
        node = soup.find(name=name)
        if node is None:
            return None
        else:
            return node.get_text().strip()

    @staticmethod
    def _parse(soup):
        # journal
        journal_name = ElsevierReadMetaData.get_text_or_none(soup, 'xocs:srctitle')
        doi = ElsevierReadMetaData.get_text_or_none(soup, 'xocs:doi')
        title = ElsevierReadMetaData.get_text_or_none(soup, 'ce:title')

        # https://www.elsevier.com/__data/assets/pdf_file/0003/58872/ja5_tagbytag5_v1.9.5.pdf
        # Elsevier XML definition pp. 46
        head_node = soup.find('head')
        keywords = []
        if head_node is not None:
            # Elsevier XML definition pp. 366
            for node in head_node.find_all('ce:keyword'):
                text_node = node.find('ce:text')
                if text_node is not None:
                    keywords.append(extract_ce_text(text_node))

        return soup, {
            'Journal': journal_name,
            'DOI': doi,
            'Title': title,
            'Keywords': keywords
        }


class ElsevierRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(args):
        soup, obj = args

        rules_to_remove = [{'name': 'xocs:meta'},
                           {'name': 'tail'},
                           {'name': 'ce:cross-refs'},
                           {'name': 'ce:cross-ref'}]
        for rule in rules_to_remove:
            for node in soup.find_all(**rule):
                node.extract()

        with open('output.xml', 'w', encoding='utf8') as f:
            f.write(str(soup))
        return soup, obj


class ElsevierCollect(RuleIngredient):

    @staticmethod
    def _parse(args):
        soup, obj = args

        paragraphs = []

        # find all sections
        for node in soup.find_all('ce:abstract'):
            paragraphs.append(extract_ce_abstract(node))

        for node in find_non_empty_children(soup.find('ce:sections')):
            if node_named(node, 'ce:para'):
                paragraphs.extend(extract_ce_para(node).split('\n'))
            elif node_named(node, 'ce:section'):
                paragraphs.append(extract_ce_section(node))

        obj['Sections'] = paragraphs
        return obj


ElsevierSoup = Soup(parser_version=__version__)
ElsevierSoup.add_ingredient(ElsevierParseXML())
ElsevierSoup.add_ingredient(ElsevierReadMetaData())
ElsevierSoup.add_ingredient(ElsevierRemoveTrash())
ElsevierSoup.add_ingredient(ElsevierCollect())

# with open('test/test_elsevier/10.1016-j.chroma.2013.12.003.xml', encoding='utf8') as f:
#     import json
#     print(json.dumps(ElsevierSoup.parse(f.read())))
