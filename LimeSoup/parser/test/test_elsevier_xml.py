# -*- coding: utf-8 -*-
import unittest

from LimeSoup.parser.elsevier_xml import extract_ce_text, resolve_elsevier_entities, extract_ce_section
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

    def test_named_entities(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
            <ce:text>&z.dshfnc; &EmptySmallSquare; &DoubleRightTee; &rscr; &jsercy;</ce:text>
        </root>"""

        tag = BeautifulSoup(resolve_elsevier_entities(xml_string), 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, '┆ ◻ ⊨ 𝓇 ј')

    def test_space(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
            <ce:text>Sub-2<ce:hsp sp="0.25"/>μm core–shell particles</ce:text>
        </root>"""

        tag = BeautifulSoup(xml_string, 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, 'Sub-2 μm core–shell particles')

    def test_font_change(self):
        xml_string = '<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">' \
                     '<ce:text>Test for <ce:bold>bold</ce:bold> ' \
                     '<ce:italic>italic</ce:italic> <ce:monospace>monospace</ce:monospace> ' \
                     '<ce:sans-serif>sans-serif</ce:sans-serif> <ce:small-caps>small-caps</ce:small-caps> ' \
                     '</ce:text></root>'

        tag = BeautifulSoup(xml_string, 'xml').find('ce:text')
        text = extract_ce_text(tag)
        self.assertEqual(text, 'Test for bold italic monospace sans-serif small-caps ')


class TestExtractSection(unittest.TestCase):
    def test_simple_text(self):
        xml_string = """<root xmlns:ce="http://www.elsevier.com/xml/common/dtd">
        <ce:sections>
            <ce:section id="s1">
                <ce:section-title id="st1">Photodamage</ce:section-title>
                <ce:para id="p1">Sunlight coupled <ce:cross-ref id="cr2"
                 refid="bib05">[1]</ce:cross-ref></ce:para>
            </ce:section>
        </ce:sections>
        </root>"""

        tag = BeautifulSoup(xml_string, 'xml').find('ce:section')
        paragraph = extract_ce_section(tag)
        self.assertEqual(paragraph, {
            'type': 'ce_section',
            'name': 'Photodamage',
            'content': ['Sunlight coupled ']
        })
