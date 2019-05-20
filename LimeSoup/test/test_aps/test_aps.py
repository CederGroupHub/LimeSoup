from LimeSoup.APSSoup import APSSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = APSSoup

    def test_paper_physical_review_letters(self):
        parsed = self.get_parsed('101103PhysRevLett93196101.xml', __file__)

        self.assertDOIEqual(parsed, '10.1103/PhysRevLett.93.196101')
        self.assertJournalEqual(parsed, 'Physical Review Letters')
        self.assertTitleEqual(
            parsed,
            'Water Dissociation on Ru(001): An Activated Process')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 15),
            ]
        )

    def test_paper_physical_review_x(self):
        parsed = self.get_parsed('101103PhysRevX4031047.xml', __file__)

        self.assertDOIEqual(parsed, '10.1103/PhysRevX.4.031047')
        self.assertJournalEqual(parsed, 'Physical Review X')
        self.assertTitleEqual(
            parsed,
            "Penetration of Action Potentials During Collision in the Median and Lateral Giant Axons of Invertebrates"
            )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$INTRODUCTION', 6),
                ('$$MATERIALS AND METHODS', 9),
                ('$$RESULTS', 1),
                ('$$RESULTS$$Theory', 5),
                ('$$RESULTS$$Experimental results$$Earthworm experiments', 6),
                ('$$RESULTS$$Experimental results$$Experiments on giant axons from the abdominal part of the ventral cord of a lobster', 1),
                ('$$DISCUSSION', 6)
            ]
        )

    def test_paper_physical_review_materials(self):
        parsed = self.get_parsed('101103PhysRevMaterials1043801.xml', __file__)

        self.assertDOIEqual(parsed, '10.1103/PhysRevMaterials.1.043801')
        self.assertJournalEqual(parsed, 'Physical Review Materials')
        self.assertTitleEqual(
            parsed,
            'Fermionic correlations as metric distances: A useful tool for materials science')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$INTRODUCTION', 2),
                ('$$METRIC SPACE DESCRIPTION OF EXCHANGE HOLES', 4),
                ('$$NUMERICAL RESULTS', 7),
                ('$$SUMMARY AND CONCLUSIONS', 1),
            ]
        )

    def test_paper_physical_review_B(self):
        parsed = self.get_parsed('101103PhysRevB80233405.xml', __file__)

        self.assertDOIEqual(parsed, '10.1103/PhysRevB.80.233405')
        self.assertJournalEqual(parsed, 'Physical Review B')
        self.assertTitleEqual(
            parsed,
            'Band-gap scaling of graphene nanohole superlattices')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 12),
            ]
        )

    def test_paper_physical_review_applied(self):
        parsed = self.get_parsed('101103PhysRevApplied8021001.xml', __file__)

        self.assertDOIEqual(parsed, '10.1103/PhysRevApplied.8.021001')
        self.assertJournalEqual(parsed, 'Physical Review Applied')
        self.assertTitleEqual(
            parsed,
            'Controlling the Spectral Characteristics of a Spin-Current Auto-Oscillator with an Electric Field')
        self.assertKeywordsEqual(
            parsed,  []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 14),
            ]
        )
