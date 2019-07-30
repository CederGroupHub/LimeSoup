import unittest

from bs4 import BeautifulSoup

from LimeSoup.parser.paragraphs import get_tag_text, INLINE_TAGS, LINEBREAK_ELEMENTS, NON_DISPLAY_TAGS


class HTMLTagText(unittest.TestCase):
    def no_common_elements(self):
        self.assertSetEqual(INLINE_TAGS & LINEBREAK_ELEMENTS, set())
        self.assertSetEqual(INLINE_TAGS & NON_DISPLAY_TAGS, set())
        self.assertSetEqual(NON_DISPLAY_TAGS & LINEBREAK_ELEMENTS, set())


class TestTagText(unittest.TestCase):
    def test_single_tags(self):
        self.assertEqual(
            get_tag_text(
                BeautifulSoup('<h1>Test</h1>', 'html.parser')
            ),
            'Test'
        )

        self.assertEqual(
            get_tag_text(
                BeautifulSoup('Test', 'html.parser')
            ),
            'Test'
        )

        self.assertEqual(
            get_tag_text(
                BeautifulSoup('<script>Should not be here</script>', 'html.parser')
            ),
            ''
        )

    def test_text_normalization(self):
        self.assertEqual(
            get_tag_text(
                BeautifulSoup('<p>Test <span>Test</span> </p>', 'html.parser')
            ),
            'Test Test'
        )

        self.assertEqual(
            get_tag_text(
                BeautifulSoup('Test1<p>Test2</p><script>something else</script>', 'html.parser')
            ),
            'Test1\nTest2'
        )
