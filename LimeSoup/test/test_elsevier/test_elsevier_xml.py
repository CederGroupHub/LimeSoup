import unittest

from LimeSoup.ElsevierSoup import extract_ce_text, resolve_elsevier_entities
from bs4 import BeautifulSoup


class TestExtractCEText(unittest.TestCase):
    def test_simple_text(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
        <ce:text>Example</ce:text>
        </root>"""

        tag = BeautifulSoup(xml_string, 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, 'Example')

    def test_named_entity(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
            <ce:text>é &eacute; &#x000E9;</ce:text>
        </root>"""

        tag = BeautifulSoup(resolve_elsevier_entities(xml_string), 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, 'é é é')

    def test_space(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
            <ce:text>Sub-2<ce:hsp sp="0.25"/>μm core–shell particles</ce:text>
        </root>"""

        tag = BeautifulSoup(xml_string, 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, 'Sub-2 μm core–shell particles')
