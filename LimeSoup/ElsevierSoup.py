from LimeSoup.ElsevierSoup_HTML import ElsevierHTMLSoup
from LimeSoup.ElsevierSoup_XML import ElsevierXMLSoup
from LimeSoup.lime_soup import Soup, RuleIngredient

__author__ = 'Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'haoyan.huo@lbl.gov'

# make sure to also update versions of HTML/XML parsers.
__version__ = '0.3.2'
__all__ = ['ElsevierSoup']


def classify_code_type(raw_string):
    """
    A very simple function to detect HTML/XML.
    """
    search_for_words = [
        '</div>',
        '</p>',
    ]
    for word in search_for_words:
        if word not in raw_string:
            return 'XML'
    return 'HTML'


class ElsevierChooseParser(RuleIngredient):
    @staticmethod
    def _parse(raw_string):
        code_type = classify_code_type(raw_string)

        if code_type == 'XML':
            return ElsevierXMLSoup.parse(raw_string)
        elif code_type == 'HTML':
            return ElsevierHTMLSoup.parse(raw_string)


ElsevierSoup = Soup(parser_version=__version__)
ElsevierSoup.add_ingredient(ElsevierChooseParser())
