import os

from unittest import TestCase


class SoupTester(TestCase):
    Soup = None

    @staticmethod
    def load_paper(filename, source_file):
        full_path = os.path.join(
            os.path.dirname(os.path.realpath(source_file)),
            filename)
        with open(full_path, encoding='utf8') as f:
            return f.read()

    def get_parsed(self, filename, source_file=__file__):
        """
        Read HTML string from paper file.

        :param filename: The filename of the paper file.
        :param source_file: The filename of the script of the caller.
        :return:
        """
        parse_obj = self.Soup.parse(self.load_paper(filename, source_file))
        return parse_obj['obj']

    def assertDOIEqual(self, parsed, doi):
        self.assertEqual(
            parsed['DOI'], doi,
            'Expected DOI %s, got %s' % (doi, parsed['DOI'])
        )

    def assertTitleEqual(self, parsed, title):
        self.assertEqual(
            parsed['Title'], title,
            'Expected title "%s", got "%s"' % (title, parsed['Title'])
        )

    def assertJournalEqual(self, parsed, journal):
        self.assertEqual(
            parsed['Journal'], journal,
            'Expected journal %s, got %s' % (journal, parsed['Journal'])
        )

    def assertKeywordsEqual(self, parsed, keywords):
        self.assertSetEqual(
            set(parsed['Keywords']), set(keywords),
            'Expected keywords %r, got %r' % (keywords, parsed['Keywords'])
        )

    def assertSectionPathsEqual(self, parsed, sections):
        """
        Test if the parser generates desired contents.
        :param parsed: Parsed object.
        :param sections: List of section heading name paths and number of
            paragraphs. For example, ('section1$$section2$$section3', 3)
        :return:
        """
        section_names = []
        for path, n_paragraphs in sections:
            section_names.append([path, n_paragraphs])

        def test_section(section, current_path):
            if isinstance(section, dict):
                test_section(section['content'], current_path + '$$' + section['name'])
            elif isinstance(section, list):
                for content in section:
                    test_section(content, current_path)
            elif isinstance(section, str):
                self.assertTrue(
                    len(section_names) > 0 and section_names[0][1] > 0,
                    'Unexpected paragraph with path %s: %s' % (current_path, section)
                )
                self.assertEqual(
                    current_path, section_names[0][0],
                    'Expected path %s, got %s' % (section_names[0][0], current_path))

                section_names[0][1] -= 1
                if section_names[0][1] == 0:
                    section_names.pop(0)

        test_section(parsed['Sections'], '')
        self.assertTrue(len(section_names) == 0, 'Missing sections: %r.' % section_names)
