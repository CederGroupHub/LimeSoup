import re

import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.paragraphs import extract_paragraphs_recursive

__author__ = 'Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'haoyan.huo@lbl.gov'
__version__ = '0.3.2'
__all__ = ['ElsevierHTMLSoup']


class ElsevierRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        soup = bs4.BeautifulSoup(html_str, 'html.parser')

        rules_for_remove = [
            {'class_': re.compile('.*?fig(?:ure)?.*?', re.IGNORECASE)},
            {'class_': re.compile('.*?table.*?', re.IGNORECASE)},
            {'name': 'a', 'href': re.compile(r'#(?:ref|bib).*?', re.IGNORECASE)},
        ]

        for rule in rules_for_remove:
            for s in soup.find_all(**rule):
                s.extract()
        return soup


class ElsevierCollect(RuleIngredient):
    @staticmethod
    def _parse(soup):
        sections = extract_paragraphs_recursive(soup)

        iterate_status = {
            'content_begins': False,
            'content_ends': False
        }

        def iterate_sections(sec):
            """
            Use simple heuristics to remove garbage
            before abstract and after conclusions.
            :param sec:
            :return:
            """
            if isinstance(sec, dict):
                sec_name = sec['name']

                if not iterate_status['content_begins']:
                    if re.match(
                            r'.*?abstract.*?',
                            sec_name, re.IGNORECASE):
                        iterate_status['content_begins'] = True

                if not iterate_status['content_ends']:
                    if re.match(
                            r'.*?(?:acknowledge?ment|reference).*?',
                            sec_name, re.IGNORECASE):
                        iterate_status['content_ends'] = True

                should_include, sub_sections = iterate_sections(sec['content'])
                sec['content'] = sub_sections
                return should_include, sec
            elif isinstance(sec, list):
                final_secs = []
                for sub_sec in sec:
                    should_include, sub_sec = iterate_sections(sub_sec)
                    if should_include:
                        final_secs.append(sub_sec)

                return len(final_secs) > 0, final_secs
            else:
                # This is the key heuristics
                should_include = iterate_status['content_begins'] \
                                 and not iterate_status['content_ends']
                if should_include:
                    return True, sec
                else:
                    return False, sec

        success, sections = iterate_sections(sections)

        return {
            'Journal': None,
            'DOI': None,
            'Title': None,
            'Keywords': None,
            'Sections': sections
        }


ElsevierHTMLSoup = Soup(parser_version=__version__)
ElsevierHTMLSoup.add_ingredient(ElsevierRemoveTrash())
ElsevierHTMLSoup.add_ingredient(ElsevierCollect())
