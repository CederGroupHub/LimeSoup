from LimeSoup.NatureSoup import NatureSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = NatureSoup

    def test_paper_1(self):
        parsed = self.get_parsed('style_1/10.1038-nature10258.html', __file__)

        self.assertDOIEqual(parsed, '10.1038/nature10258')
        self.assertJournalEqual(parsed, 'Nature')
        self.assertTitleEqual(
            parsed,
            'Crystal structure of the human centromeric nucleosome containing CENP-A')
        self.assertKeywordsEqual(
            parsed, [
                # Fixme: change here in the future.
                "Structural biology, Cell biology, Biochemistry, Molecular biology"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Main', 8),
                ('$$Methods$$Overexpression of human histones', 2),
                ('$$Methods$$Purification of human histones', 1),
                ('$$Methods$$Preparation of DNAs', 3),
                ('$$Methods$$Preparation of the CENP-A nucleosome', 1),
                ('$$Methods$$Crystallization and structure determination', 2),
                ('$$Methods$$Supercoiling assay', 3),
                ('$$Methods'
                 '$$Nucleosome reconstitution by the salt-dialysis method for biochemical analyses', 1),
                ('$$Methods$$Competitive nucleosome assembly assay', 1),
                ('$$Methods$$Nucleosome disruption assay', 1),
                ('$$Methods$$Exonuclease assay', 1),
                ('$$Methods$$Small-angle X-ray scattering (SAXS)', 1),
                ('$$Methods$$Centromere localization of CENP-A and CENP-A mutants', 1),
                ('$$Accession codes$$Primary accessions$$Protein Data Bank', 2),
            ]
        )
