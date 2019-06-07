import os

import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from lxml import etree

__author__ = 'Haoyan Huo, Nicolas Mingione'
__maintainer__ = 'Nicolas Mingione'
__version__ = '0.3.1-dev'


# Elsevier XML format is defined here:
# Book "The Elsevier DTD 5 Family of XML DTDs"
# https://www.elsevier.com/__data/assets/pdf_file/0003/58872/ja5_tagbytag5_v1.9.5.pdf
# https://www.elsevier.com/__data/assets/text_file/0006/275667/ja5_common150_ent.txt


def resolve_elsevier_entities(xml_string):
    """
    Elsevier defined a set of entities that can be found in the corrsponding
    ent (entity) files. However, XML files do not contain definition of such
    entities. Thus, we need to load the entities and patch the XML files, so
    that these entities are converted into unicode chars.
    See also "The Elsevier DTD 5 Family of XML DTDs" pp. 12

    :param xml_string:
    :return:
    """
    if not hasattr(resolve_elsevier_entities, 'dtd_strings'):
        dtd_to_load = [
            'dtd/xhtml-lat1.ent',
            'dtd/ja5_art540/cep140/ESextra.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamsa.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamsb.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamsc.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamsn.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamso.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isoamsr.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isogrk3.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isogrk4.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isomfrk.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isomopf.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isomscr.ent',
            'dtd/ja5_art540/cep140/iso9573-13/isotech.ent'
        ]

        string = []
        for i, file in enumerate(dtd_to_load):
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
            # lxml hates backslashes
            file_path = file_path.replace('\\', '/')

            invocation = """<!ENTITY % {dtdid} PUBLIC "{dtdid}" "{url}" > %{dtdid};""".format(
                dtdid='dtd%d' % i, url=file_path.replace('\\', '/')
            )
            string.append(invocation)
        setattr(resolve_elsevier_entities, 'dtd_invocation', '<!DOCTYPE xml [\n' + '\n'.join(string) + ']>\n')

    parser = etree.XMLParser(load_dtd=True)
    xml_tree = etree.fromstring(
        getattr(resolve_elsevier_entities, 'dtd_invocation') + xml_string,
        parser=parser,
    )
    return etree.tostring(xml_tree)


def process_richstring_data(_node):
    # <!ENTITY % richstring.data  "#PCDATA|ce:glyph|%text-effect;|ce:inline-figure
    #                              %local.richstring.data;" >
    # <!ENTITY % text-effect      "%font-change;|ce:sup|ce:inf|ce:underline|
    #                              ce:cross-out|ce:hsp|ce:vsp" >
    # <!ENTITY % font-change      "ce:bold|ce:italic|ce:monospace|ce:sans-serif|
    #                              ce:small-caps" >
    if _node.name is None:
        # PC data
        return _node.string
    elif _node.prefix == 'ce' and _node.name == 'glyph':
        # FIXME: don't know how to process glyph, produce a whitespace
        return ' '
    elif _node.prefix == 'ce' and _node.name == 'inline-figure':
        return ' '
    elif _node.prefix == 'ce' and _node.name in {
        'bold', 'italic', 'monospace', 'sans-serif', 'small-caps',
        'underline', 'cross-out'
    }:
        children_strings = [process_richstring_data(x) for x in _node.children]
        return ''.join(children_strings)
    elif _node.prefix == 'ce' and _node.name in {'sup', 'inf'}:
        children_strings = [process_richstring_data(x) for x in _node.children]
        return ''.join(children_strings)
    elif _node.prefix == 'ce' and _node.name in {'hsp', 'vsp'}:
        return ' '
    else:
        raise NameError('Unknown tag <%s> in richstring processing' % str(_node.name))


def process_math(_node):
    # FIXME:
    return '<formula>'


def process_text_data(_node):
    # <!ENTITY % text.data        "%richstring.data;|%math; %local.text.data;" >
    try:
        return process_richstring_data(_node)
    except NameError:
        return process_math(_node)


def process_inter_ref(_node):
    # <!ELEMENT   ce:inter-ref        ( %text.data; )* >
    strings = []
    for child in _node.children:
        strings.append(process_text_data(child))
    return ''.join(strings)


def process_textlink_data(_node):
    # <!ENTITY % textlink.data    "%text.data;|ce:inter-ref" >
    try:
        return process_text_data(_node)
    except NameError:
        return process_inter_ref(_node)


def extract_ce_text(node):
    """
    This is the parser for ce:text element defined in Elsevier XML CEP 1.4.0.
    <!ELEMENT   ce:text             ( %textlink.data; )* >

    :param node: A beautiful soup Tag node.
    :return: The text embedded in this node.
    """
    all_strings = []
    for i in node.children:
        all_strings.append(process_textlink_data(i))
    return ''.join(all_strings)


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


class ElsevierSpaceBeforeFormula(RuleIngredient):
    @staticmethod
    def _parse(parser):
        parser.parse_formula(rules=[{'name': 'formula'}])
        return parser


class ElsevierCreateTags(RuleIngredient):
    @staticmethod
    def _parse(parser):
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser


class ElsevierMoveJournalName(RuleIngredient):
    @staticmethod
    def _parse(parser):
        try:
            parser.move_journal_name(rule={'name': 'xocs:srctitle'})
        except:
            pass
        return parser


class ElsevierCreateTagAbstract(RuleIngredient):
    @staticmethod
    def _parse(parser):
        try:
            parser.create_abstract(rule={'name': 'dc:description'})
        except:
            pass
        return parser


class ElsevierReplaceSectionTag(RuleIngredient):
    @staticmethod
    def _parse(parser):
        try:
            parser.strip_tags(rules=[{'name': 'ce:section'}])
        except:
            pass
        return parser


class ElsevierRenameSectionTitleTag(RuleIngredient):
    @staticmethod
    def _parse(parser):
        try:
            parser.rename_tag({'name': 'section-title'}, 'section_title')
        except:
            pass
        return parser.raw_xml


class ElsevierCollect(RuleIngredient):

    @staticmethod
    def _parse(parser):
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'ce:keyword'}])
        journal_name = next(x for x in parser.get([{'name': 'ce:srctitle'}]))
        parser.get_title(rules=[
            {'name': 'ce:title'}
        ])
        try:
            # Create tag from selection function in ParserPaper
            parser.deal_with_sections()
            data = parser.data_sections
        except:  # If Elsevier gives only the abstract OR gives only the raw text
            data = []
            try:
                abstract = parser.get_abstract(rule={'name': 'dc:description'})
                if len(abstract) > 0:
                    data.append(abstract)
            except:
                pass
            try:
                raw_text = parser.raw_text(rule={'name': 'xocs:rawtext'})
                if len(raw_text) > 0:
                    data.append(raw_text)
            except:
                pass
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


ElsevierSoup = Soup(parser_version=__version__)
ElsevierSoup.add_ingredient(ElsevierParseXML())
ElsevierSoup.add_ingredient(ElsevierReadMetaData())
ElsevierSoup.add_ingredient(ElsevierRemoveTrash())
# ElsevierSoup.add_ingredient(ElsevierCreateTagAbstract())
# ElsevierSoup.add_ingredient(ElsevierCreateTags())
# ElsevierSoup.add_ingredient(ElsevierReplaceSectionTag())
# ElsevierSoup.add_ingredient(ElsevierRenameSectionTitleTag())
# ElsevierSoup.add_ingredient(ElsevierCollect())

with open('test/test_elsevier/10.1016-j.chroma.2013.12.003.xml', encoding='utf8') as f:
    print(ElsevierSoup.parse(f.read())[1])
