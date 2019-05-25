from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_IOP import ParserPaper1, ParserPaper2


__author__ = 'Zheren Wang'
__maintainer__ = ''
__email__ = ''
__version__ = '0.1.1'

class IOPSoup(Soup):

    def parse(html_str):
        parsed_paper = IOPSoup1.parse(html_str)
        if parsed_paper['DOI']:
            return parsed_paper
        return IOPSoup2.parse(html_str)
"""
The reason why there are two different soup and parsers is that papers from IOP have two different formats, so two parsers are made. Here the way to classify two formats is using different parsers to parse IOP xml, if the xml can be successfully parsed, then we accept the parsed result, otherwise we use another parser. 

"""


class IOPRemoveTrash1(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper
        list_remove = [
            {'name': 'ref-list'},
            {'name': 'xref', 'ref-type': 'bibr'},
            {'name': 'table-wrap'},
            {'name': 'fig'},
        ]
        parser = ParserPaper1(xml_str, parser_type='lxml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml

class IOPCreateTags1(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper1(xml_str, parser_type='lxml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class IOPReplaceSectionTag1(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper1(xml_str, parser_type='lxml', debugging=False)
        parser.change_name_tag_sections()
        return parser.raw_xml

class IOPReformat1(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper1(new_xml, parser_type='lxml',debugging=False)
        return parser.raw_xml

class IOPCollect1(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper1(xml_str, parser_type='lxml', debugging=False)
        # Collect information from the paper using ParserPaper
        try:
            journal_name = next(x for x in parser.get(rules=[{"name": "jnl-fullname"}]))
        except StopIteration:
            journal_name = None

        parser.get_title(rules=[
            {'name': 'title'}
        ]
        )
        doi = parser.get(rules=[
            {'name': 'doi'}
        ])
        parser.deal_with_sections()
        data = parser.data_sections
        parser.create_abstract(rule={'name': 'abstract'})

        obj = {
            'DOI': "".join(doi),
            'Keywords': [],
            'Title': parser.title,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


IOPSoup1 = Soup(parser_version=__version__)
IOPSoup1.add_ingredient(IOPReformat1())
IOPSoup1.add_ingredient(IOPRemoveTrash1())
IOPSoup1.add_ingredient(IOPCreateTags1())
IOPSoup1.add_ingredient(IOPReplaceSectionTag1())
IOPSoup1.add_ingredient(IOPCollect1())

class IOPRemoveTrash2(RuleIngredient):
    @staticmethod
    def _parse(xml_str):
        # Tags to be removed from the xml paper
        list_remove = [
            {'name': 'ref-list'},
            {'name': 'xref', 'ref-type': 'bibr'},
            {'name': 'table-wrap'},
            {'name': 'fig'},
        ]
        parser = ParserPaper2(xml_str, parser_type='lxml', debugging=False)
        parser.remove_tags(rules=list_remove)
        return parser.raw_xml

class IOPCreateTags2(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper2(xml_str, parser_type='lxml', debugging=False)
        try:
            # This create a standard of sections tag name
            parser.create_tag_sections()
        except:
            pass
        return parser.raw_xml

class IOPReplaceSectionTag2(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper2(xml_str, parser_type='lxml', debugging=False)
        parser.change_name_tag_sections()
        return parser.raw_xml

class IOPReformat2(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        new_xml = xml_str.replace('>/','>')
        parser = ParserPaper2(new_xml, parser_type='lxml',debugging=False)
        return parser.raw_xml

class IOPCollect2(RuleIngredient):

    @staticmethod
    def _parse(xml_str):
        parser = ParserPaper2(xml_str, parser_type='lxml', debugging=False)
        # Collect information from the paper using ParserPaper
        try:
            journal_name = next(x for x in parser.get(rules=[{"name": "journal-title"}]))
        except StopIteration:
            journal_name = None

        parser.get_title(rules=[
            {'name': 'article-title'}
        ]
        )
        doi = parser.get(rules=[
            {'name': 'article-id',
            'pub-id-type': 'doi'}
        ])
        parser.deal_with_sections()
        data = parser.data_sections
        parser.create_abstract(rule={'name': 'abstract'})

        obj = {
            'DOI': "".join(doi),
            'Keywords': [],
            'Title': parser.title,
            'Journal': journal_name,
            'Sections': data
        }
        return obj


IOPSoup2 = Soup(parser_version=__version__)
IOPSoup2.add_ingredient(IOPReformat2())
IOPSoup2.add_ingredient(IOPRemoveTrash2())
IOPSoup2.add_ingredient(IOPCreateTags2())
IOPSoup2.add_ingredient(IOPReplaceSectionTag2())
IOPSoup2.add_ingredient(IOPCollect2())


# if __name__ == '__main__':
#     filename = "cm10_4_045302.xml"
#     with open(filename, "r", encoding="utf-8") as f:
#         paper = f.read()

#     parsed_paper = IOPSoup.parse(paper)
#     print(parsed_paper )
    # if parsed_paper['DOI']:
    #     print(parsed_paper)
    # data = parsed_paper["obj"] 
