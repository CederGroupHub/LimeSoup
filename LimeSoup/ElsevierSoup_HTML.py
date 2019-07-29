import re

import bs4

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.paragraphs import extract_paragraphs_recursive, get_tag_text

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
        obj = {
            'Journal': None,
            'DOI': None,
            'Title': None,
            'Keywords': None,
            'Sections': None
        }

        h1_tag = soup.find('h1')
        if h1_tag is not None:
            obj['Title'] = get_tag_text(h1_tag)
            h1_tag.extract()

        raw_sections = extract_paragraphs_recursive(soup)

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
                sec_name = re.sub(r'^[0-9.\s]+', '', sec['name'])

                if re.match(r'keywords?', sec_name, re.IGNORECASE) and \
                        all(isinstance(x, str) for x in sec['content']):
                    obj['Keywords'] = [x.strip(';') for x in sec['content']]
                    return False, sec

                if not iterate_status['content_begins']:
                    if re.match(r'.*?abstract.*?', sec_name, re.IGNORECASE) or \
                            (len(sec['content']) > 0 and
                             isinstance(sec['content'][0], str) and  # Typical abstract has more than 100 words
                             sec['content'][0].count(' ') > 100):
                        iterate_status['content_begins'] = True

                if not iterate_status['content_ends']:
                    if re.match(
                            r'.*?(?:acknowledge?ment|reference).*?',
                            sec_name, re.IGNORECASE):
                        iterate_status['content_ends'] = True

                should_include, sub_sections = iterate_sections(sec['content'])
                sec['content'] = sub_sections
                sec['name'] = sec_name
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

        success, sections = iterate_sections(raw_sections)
        obj['Sections'] = sections

        return obj


ElsevierHTMLSoup = Soup(parser_version=__version__)
ElsevierHTMLSoup.add_ingredient(ElsevierRemoveTrash())
ElsevierHTMLSoup.add_ingredient(ElsevierCollect())
