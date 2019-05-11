from LimeSoup.RSCSoup import RSCSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = RSCSoup

    def test_paper_New_J_Chem_paper(self):
        parsed = self.get_parsed('10.1039-B006835G.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B006835G')
        self.assertTitleEqual(
            parsed,
            'Photoreaction of 2-morpholinoacrylonitrile with substituted 1-acetonaphthones. Part II')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'New J. Chem.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction(guess)', 1),
                ('$$Results and discussion', 5),
                ('$$Experimental', 2),
                ('$$Experimental'
                 '$$Irradiation of 4-chloro-1-acetonaphthone 1f in the presence of 2-morpholinoacrylonitrile 2', 1),
                ('$$Experimental'
                 '$$Irradiation of 4-fluoro-1-acetonaphthone 1g in the presence of 2', 2),
                ('$$Experimental'
                 '$$Irradiation of 4-methyl-1-acetonaphthone 1h in the presence of 2', 2),
                ('$$Experimental'
                 '$$Irradiation of 2-methyl-1-acetonaphthone 1i in the presence of 2', 2),
                ('$$Experimental$$Irradiation of 5b', 1),
                ('$$Experimental$$Hydrolysis of 5b', 2),
            ]
        )

    def test_paper_Analyst_paper(self):
        parsed = self.get_parsed('10.1039-B208577A.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B208577A')
        self.assertTitleEqual(
            parsed,
            'Headspace solid-phase microextraction—comprehensive two-dimensional gas '
            'chromatography of wound induced plant volatile organic compound emissions')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Analyst'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1. Introduction', 3),
                ('$$2. Experimental methods$$2.1 Samples, sampling material and sampling', 4),
                ('$$2. Experimental methods$$2.2 Gas chromatographic analysis', 3),
                ('$$2. Experimental methods$$2.3 Gas chromatographic-mass spectrometry analysis', 1),
                ('$$3. Results and discussion$$3.1 Fibre selection', 4),
                ('$$3. Results and discussion$$3.2 Time profile', 2),
                ('$$3. Results and discussion$$3.3 Identification of components of the plant samples headspace', 2),
                ('$$3. Results and discussion$$3.4 Comprehensive GC×GC vs. GC', 7),
                ('$$Conclusion', 1),
            ]
        )
