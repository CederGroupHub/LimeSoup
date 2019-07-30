from LimeSoup.NatureSoup import NatureSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = NatureSoup

    def test_paper_1(self):
        parsed = self.get_parsed('10.1038-19734.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/19734')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            'A nanometre-sized hexahedral coordination capsule assembled from 24 components')
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

    def test_paper_2(self):
        parsed = self.get_parsed('10.1038-26206.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/26206')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            "Plastic deformation of silicate spinel under the transition-zone conditions of the Earth's mantle")
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 10),
            ]
        )

    def test_paper_3(self):
        parsed = self.get_parsed('10.1038-416304a.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/416304a')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            'An ordered mesoporous organosilica hybrid material with a crystal-like wall structure')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 6),
                ('$$Methods$$Preparation of mesoporous benzene–silica material', 1),
                ('$$Methods$$Sulphonation of mesoporous benzene–silica', 1),
            ]
        )

    def test_paper_4(self):
        parsed = self.get_parsed('10.1038-35012032.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/35012032')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            'Relaxation in polymer electrolytes on the nanosecond timescale')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 11),
            ]
        )

    def test_paper_5(self):
        parsed = self.get_parsed('10.1038-35050110.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/35050110')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            "Aβ peptide immunization reduces behavioural impairment and plaques in a model of Alzheimer's disease")
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 8),
                ('$$Methods$$Mice', 1),
                ('$$Methods$$Immunization procedures', 1),
                ('$$Methods$$Behavioural tests and data analysis', 2),
                ('$$Methods$$Analysis of βAPP and amyloid burden in brain', 2),
            ]
        )

    def test_news(self):
        parsed = self.get_parsed('10.1038-440274a.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/440274a')
        self.assertTitleEqual(
            parsed,
            "Political chemistry: Make a strong bond")
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('', 24),
            ]
        )

    def test_no_doi(self):
        parsed = self.get_parsed('10.1038-416525a.html', __file__)

        self.assertDOIEqual(parsed, None)
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 8),
            ]
        )
