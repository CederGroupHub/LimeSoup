import json
import os
import re
import warnings
from unittest import TestCase


def load_html_character_entities_re():
    # create a regular expression that will capture all HTML character entities
    # https://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
    # https://www.w3.org/TR/html5/syntax.html#named-character-references
    # https://www.w3.org/TR/html5/entities.json
    entity_definition = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'html_entities.json'
    )
    with open(entity_definition) as f:
        char_entities = json.load(f)
    regular_expr = r'&#\d{1,4};|&#x[0-9a-f]{1,4};|' + '|'.join(char_entities.keys())
    return re.compile(regular_expr)


HTML_CHAR_ENTITY_RE = load_html_character_entities_re()


def type_of_element_in_list(meta_list):
    """
    Get the type of all elements in a list
    :param meta_list:  a list
    :return: a set of all types of the elements in the input list
    """
    all_types = []
    for e in meta_list:
        all_types.append(type(e))
    return set(all_types)


def flatten_section(section):
    """
    convert stacked sections (with sub-sections in the content field)
    in parsed result to a list of simple sections (no sub-sections)
    :param section: a list of stacked sections or a stacked section dict
    :return: a list of simple sections
    """
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
    return all_sections


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
            doi, parsed['DOI'],
            'Expected DOI %s, got %s' % (doi, parsed['DOI'])
        )

    def assertTitleEqual(self, parsed, title):
        self.assertEqual(
            title, parsed['Title'],
            'Expected title "%s", got "%s"' % (title, parsed['Title'])
        )

    def assertJournalEqual(self, parsed, journal):
        self.assertEqual(
            journal, parsed['Journal'],
            'Expected journal %s, got %s' % (journal, parsed['Journal'])
        )

    def assertKeywordsEqual(self, parsed, keywords):
        self.assertSetEqual(
            set(keywords), set(parsed['Keywords']),
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
                    section_names[0][0], current_path,
                    'Expected path %s, got %s' % (section_names[0][0], current_path))

                section_names[0][1] -= 1
                if section_names[0][1] == 0:
                    section_names.pop(0)

        test_section(parsed['Sections'], '')
        self.assertTrue(len(section_names) == 0, 'Missing sections: %r.' % section_names)

    def assertMaterialMentioned(self, parsed, materials, key_materials=None):
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
        materials = set(materials)
        key_materials = set(key_materials or ())

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
            for paragraph in content:
                for mat in materials - materials_found:
                    if mat in paragraph:
                        materials_found.add(mat)
            if re.match(r'.*?abstract.*?', name, re.IGNORECASE):
                all_text['abstract'].extend(content)
            elif re.match(r'.*?(conclusion|summary).*?', name, re.IGNORECASE):
                all_text['conclusion'].extend(content)
            else:
                all_text['main_content'].extend(content)

        # clean all_text
        all_text = {k: v for (k, v) in all_text.items() if len(v) > 0}
        if 'main_content' in all_text and len(all_text['main_content']) <= 3:
            # assume main content should have at least 3 (arbitary) paragraphs
            del all_text['main_content']

        # get key_materials_not_found and key_materials_found
        for mat in key_materials:
            for paras in all_text.values():
                text = '\n'.join(paras)
                if mat not in text:
                    key_materials_not_found.add(mat)
        key_materials_found = key_materials - key_materials_not_found

        self.assertEqual(
            materials_found, set(materials),
            'Expected materials %s, got %s' % (sorted(set(materials)), sorted(materials_found))
        )
        self.assertEqual(
            key_materials_found, set(key_materials),
            'Expected key materials %s, got %s' % (sorted(set(key_materials)), sorted(key_materials_found))
        )

    def checkSpecialCharInStr(self, s):
        """
        check the special characters in input string
        1. raise error if html characters are used
        2. raise warning if characters neither ascii nor extended latin are used
        :param s: a string
        :return:
        """
        # check if contain HTML characters such as &nbsp;
        def contain_html(string):
            return HTML_CHAR_ENTITY_RE.search(string) is not None

        # check if only ascii or extended latin characters are contained
        # extended ascii: https://www.ascii-code.com/
        # extended latin: see https://en.wikipedia.org/wiki/Latin_script_in_Unicode
        # greek: https: // en.wikipedia.org / wiki / Greek_alphabet
        def get_non_ascii_latin(s):
            result = []
            for c in s:
                # ascii
                not_ascii = False
                if not (ord(c) < 256):
                    not_ascii = True
                # extended latin
                not_latin = False
                if not (0x00C0 <= ord(c) < 0x017F):
                    not_latin = True
                # greek
                not_greek = False
                if not (0x0370 <= ord(c) <= 0x03FF):
                    not_greek = True
                if all([not_ascii, not_latin, not_greek]):
                    result.append(c)
            if result:
                print(s)
                print(result)
            return result

        # simple text cleaning work here
        def simple_clean(s):
            new_s = s
            new_s = new_s.replace('–', '-')
            new_s = new_s.replace('—', '-')
            new_s = new_s.replace('−', '-')
            new_s = new_s.replace('’', '\'')
            return new_s

        # get check results
        new_s = simple_clean(s)
        non_ascii_latin = get_non_ascii_latin(new_s)

        # error if HTML characters used
        self.assertFalse(
            contain_html(new_s),
            'Expected no HTML characters, got %s' % (s)
        )

        # warning if characters neither ascii nor extended latin are used
        if non_ascii_latin:
            warnings.warn(
                'Not only ascii or latin characters used in %s, found: %s' % (s, non_ascii_latin),
                UnicodeWarning
            )

    def checkSpecialCharacters(self, parsed, field_to_check=['Journal']):
        """
        check the special characters in parsed fields
        1. raise error if html characters are used
        2. raise warning if characters neither ascii nor extended latin are used
        :param parsed: Parsed object.
        :param field_to_check: fields in parsed object to check. Check journal name as default.
        :return:
        """

        def get_str_from_journal(parsed):
            # TODO: to be updated after the type of Journal/Title is changed to str
            parsed_str = []
            if parsed['Journal']:
                self.assertEqual(
                    len(parsed['Journal']), 1,
                    'Expected only 1 journal name, got %s' % (len(parsed['Journal']))
                )
                parsed_str.append({
                    'source': 'Journal',
                    'str': parsed['Journal'][0],
                })
            return parsed_str

        def get_str_from_title(parsed):
            # TODO: to be updated after the type of Journal/Title is changed to str
            parsed_str = []
            if parsed['Title']:
                self.assertEqual(
                    len(parsed['Title']), 1,
                    'Expected only 1 title, got %s' % (len(parsed['Title']))
                )
                parsed_str.append({
                    'source': 'Title',
                    'str': parsed['Title'][0],
                })
            return parsed_str

        def get_str_from_doi(parsed):
            parsed_str = []
            if parsed['DOI']:
                parsed_str.append({
                    'source': 'DOI',
                    'str': parsed['DOI'],
                })
            return parsed_str

        def get_str_from_keywords(parsed):
            parsed_str = []
            for kw in parsed['Keywords']:
                parsed_str.append({
                    'source': 'Keywords',
                    'str': kw,
                })
            return parsed_str

        def get_str_from_sections(parsed):
            parsed_str = []
            all_sections = flatten_section(parsed['Sections'])
            for tmp_section in all_sections:
                parsed_str.append({
                    'source': 'Sections.name',
                    'str': tmp_section['name'],
                })
                parsed_str.append({
                    'source': 'Sections.type',
                    'str': tmp_section['type'],
                })
                for tmp_para in tmp_section['content']:
                    parsed_str.append({
                        'source': 'Sections.content',
                        'str': tmp_para,
                    })
            return parsed_str

        get_str_from = {
            'Journal': get_str_from_journal,
            'Title': get_str_from_title,
            'DOI': get_str_from_doi,
            'Keywords': get_str_from_keywords,
            'Sections': get_str_from_sections,
        }

        # goal
        str_to_check = []

        for k in field_to_check:
            self.assertIn(
                k, get_str_from,
                'Key error! Cannot get str from the field: %s' % (k)
            )
            str_to_check.extend(get_str_from[k](parsed))

        for tmp_str in str_to_check:
            self.checkSpecialCharInStr(tmp_str['str'])
