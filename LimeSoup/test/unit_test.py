#!/usr/bin/env python

"""
unit_test script is a script to test the Soup classes.
Implemented for ECSSoup and its ingredients.
Future:
    -> Implemented for RCSSoup and its ingredients.

Use:
    python unit_test.py

"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "May 20 2017"

import unittest
import argparse

import json
import bs4

from LimeSoup.ECSSoup import ECSSoup, ECSRemoveTrash, ECSCreateTags, ECSCollect
from LimeSoup.lime_soup import Soup
from LimeSoup.parser.parser_paper import ParserPaper

# from LimeSoup.lime_soup import RuleIngredient
# from LimeSoup.parser.parser_paper import ParserPaper


class TestFunctions(unittest.TestCase):

    def number_of_section(self):
        parse = ParserPaper()
        soup = bs4.BeautifulSoup("{:}".format(raw_html), "lxml-xml")
        know_value = soup.find_all(parse.compile('^h[1-6]$'))
        result = parse.number_headings
        self.assertEqual(know_value, result)

    def number_of_paragraphs(self):
        parse = ParserPaper()
        soup = bs4.BeautifulSoup("{:}".format(raw_html), "lxml-xml")
        know_value = soup.find_all(parse.compile('^h[1-6]$'))
        result = parse.number_paragraphs
        self.assertEqual(know_value, result)


class TestKnownValuesOffline(unittest.TestCase):
    # Test a list of html files from paper of different publishers, future...
    # Create a instance with a emulated method to create a test set offline
    # This a test for known values, other tests can be included.
    def test_ECSSoup_parser(self):
        """parser should give known result with known input"""
        for k in range(1, 2):
            know_value = json.load(open('ecs_papers/paper{:}.json'.format(k)))
            with open('ecs_papers/paper{:}.html'.format(k), 'r') as fd:
                html_str = fd.read()
            result = ECSSoup.parse(html_str)
            self.assertEqual(know_value, result)


class TestIngredients(unittest.TestCase):

    def test_ECSSoup_ECSRemoveTrash(self):
        test_value = ('<?xml version="1.0" encoding="utf-8"?>\n<html>\n Bla\n'
                      + ' <code>\n Bla\n <code/>\n <html/>\n</html>')
        know_value = '<?xml version="1.0" encoding="utf-8"?>\n<html>\n Bla\n</html>'
        ecs_soup_test = Soup()
        ecs_soup_test.add_ingredient(ECSRemoveTrash())
        result = ecs_soup_test.parse(test_value)
        self.assertEqual(know_value, result)

    def test_ECSSoup_ECSCreateTags(self):
        test_value = '<html>\n <h2> section1 </h2> Bla\n  </html>'
        know_value = ('<?xml version="1.0" encoding="utf-8"?>\n<section_h2>\n <h2>\n  section1\n </h2>'
                      + '\n Bla\n</section_h2>')
        ecs_soup_test = Soup()
        ecs_soup_test.add_ingredient(ECSCreateTags())
        result = ecs_soup_test.parse(test_value)
        self.assertEqual(know_value, result)

    def test_ECSSoup_ECSCollect(self):
        test_value = ('<?xml version="1.0" encoding="utf-8"?>\n<html>\n <h1> title </h1> \n'
                      + ' <code>\n Bla\n <code/>\n <html/>\n</html>')
        know_value = {'Title': ['title'], 'Keywords': [], 'Sections': [None]}
        ecs_soup_test = Soup()
        ecs_soup_test.add_ingredient(ECSCollect())
        result = ecs_soup_test.parse(test_value)
        self.assertEqual(know_value, result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""unit_test is a script that test the ParserPaper class""",
        epilog="""Author: {}
            Version: {}
            Last updated: {}""".format(__author__, __version__, __date__))
    parser.add_argument(
        "-ARG1",
        help="""descriptions of ARG1 .""")
    args = parser.parse_args()
    if args.ARG1 is None:
        ARG1 = args.ARG1
    if ARG1 is not None:
        print("Performing online test!")
    else:
        print("Performing just offline test!")
    print("\nPerforming offline test!")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKnownValuesOffline)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIngredients)
    unittest.TextTestRunner().run(suite)
