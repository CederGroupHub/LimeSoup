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

    def assertMaterialMentioned(self, parsed, materials, key_materials=[]):
        """
        Test if the parser extract material in correct format.
        1. Check if materials appear in at least one paragraph
        2. Check if key materials appear in abstract, main content,
        and conclusion if applicable.
        Assume a "key material" should appears in abstract, main content,
        and conclusion. For materials only appearing in one or few paragraphs,
        the string of materials should be assigned into `materials` rather
        than `key_materials`.
        :param parsed: Parsed object.
        :param materials: List of material strings. For example, ['Y2O3']
        :param key_materials: List of key material strings. For example, ['Pb(ZrxTi1−x)O3']
        :return:
        """

        def type_of_element_in_list(meta_list):
            all_types = []
            for e in meta_list:
                all_types.append(type(e))
            return set(all_types)

        def flatten_section(section):
            all_sections = []
            if isinstance(section, list):
                for sub_section in section:
                    all_sections.extend(flatten_section(sub_section))
            elif isinstance(section, dict):
                type_of_list = type_of_element_in_list(section['content'])
                if type_of_list == {dict}:
                    all_sections.extend(flatten_section(section['content']))
                elif type_of_list == {str}:
                    all_sections.append(section)
            return  all_sections

        # goal
        materials_found = set()
        key_materials_not_found = set()
        all_text = {
            'abstract': [],
            'main_content': [],
            'conclusion': [],
        }

        # get materials_found and all_text
        all_sections = flatten_section(parsed['Sections'])
        for section in all_sections:
            name = section['name']
            content = section['content']
            text = '\n'.join(content)
            for mat in materials:
                if mat in text:
                    materials_found.add(mat)
            name_lower = name.lower()
            if 'abstract' in name_lower:
                all_text['abstract'].extend(content)
            elif ('conclusion' in name_lower or
                  'summary' in name_lower):
                all_text['conclusion'].extend(content)
            else:
                all_text['main_content'].extend(content)

        # clean all_text
        all_text = dict(filter(lambda x: len(x[1]) > 0, all_text.items()))
        if 'main_content' in all_text and len(all_text['main_content']) <= 3:
            # assume main content should have at least 3 (arbitary) paragraphs
            del all_text['main_content']

        # get key_materials_not_found and key_materials_found
        for mat in key_materials:
            for paras in all_text.values():
                text = '\n'.join(paras)
                if mat not in text:
                    key_materials_not_found.add(mat)
        key_materials_found = set(key_materials) - key_materials_not_found

        self.assertEqual(
            materials_found, set(materials),
            'Expected materials %s, got %s' % (sorted(set(materials)), sorted(materials_found))
        )
        self.assertEqual(
            key_materials_found, set(key_materials),
            'Expected materials %s, got %s' % (sorted(set(key_materials)), sorted(key_materials_found))
        )

