import unittest

from bs4 import BeautifulSoup

from LimeSoup.parser.paragraphs import get_tag_text


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
