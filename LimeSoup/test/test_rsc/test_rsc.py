from LimeSoup.RSCSoup import RSCSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = RSCSoup

    def test_paper_CrystEngComm_highlight(self):
        parsed = self.get_parsed('10.1039-B201206E.html', __file__)

        print(parsed)
        self.assertDOIEqual(parsed, '10.1039/B201206E')
        self.assertTitleEqual(
            parsed,
            'Database research in crystal engineering')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 7),
                ('$$Methods', 3),
            ]
        )
