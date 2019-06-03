from LimeSoup.ElsevierSoup import ElsevierSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = ElsevierSoup

    def test_paper_abs_only(self):
        parsed = self.get_parsed('10.1006-jcis.1997.5095.xml', __file__)

        self.assertJournalEqual(parsed, 'Journal of Colloid and Interface Science')
        self.assertTitleEqual(
            parsed,
            '2-D and 3-D Interactions in Random Sequential Adsorption of Charged Particles')
        self.assertKeywordsEqual(
            parsed, [
                'colloidal electrostatic interactions',
                'superposition approximation',
                'simulation',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
            ]
        )

    def test_paper_paper_with_list(self):
        parsed = self.get_parsed('10.1016-j.apsusc.2009.04.100.xml', __file__)

        self.assertJournalEqual(parsed, 'Applied Surface Science')
        self.assertTitleEqual(
            parsed,
            'Laser-assisted micro-forming process with miniaturised structures in sapphire dies')
        self.assertKeywordsEqual(
            parsed, [
                'Laser treatment',
                'Sapphire dies',
                'Miniaturisation',
                'Micro-forming',
                'Size effects',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 2),
                ('$$Die structures made using rotation masks', 4),
                ('$$Micro-forming', 8),
                ('$$Experimental set-up for laser-assisted micro-forming', 2),
                ('$$Conclusion', 1),
            ]
        )

    def test_paper_with_equations(self):
        parsed = self.get_parsed('10.1016-j.jiec.2013.10.024.xml', __file__)

        self.assertJournalEqual(parsed, 'Journal of Industrial and Engineering Chemistry')
        self.assertTitleEqual(
            parsed,
            'Adsorption of Cu(II) from aqueous solution by micro-structured ZnO thin films')
        self.assertKeywordsEqual(
            parsed, [
                'ZnO',
                'Micro-structure',
                'Thin film',
                'Adsorption',
                'Copper ion',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experimental methods', 8),
                ('$$Results$$Effect of pH on the film structure', 8),
                ('$$Results$$Effect of MW irradiation time on the film structure', 4),
                ('$$Results$$Surface area measurement', 2),
                ('$$Results$$Adsorption studies', 4),
                ('$$Results$$Point of zero charge pH', 1),
                ('$$Results$$The effect of pH on the removal efficiency', 2),
                ('$$Results$$Comparison with other adsorbents', 1),
                ('$$Conclusion', 3),
            ]
        )

    def test_paper_with_chemical_formulas(self):
        parsed = self.get_parsed('10.1016-j.materresbull.2015.04.014.xml', __file__)

        self.assertJournalEqual(parsed, 'Materials Research Bulletin')
        self.assertTitleEqual(
            parsed,
            'Electronic structure, optical and thermal/concentration '
            'quenching properties of Lu2−2xEu2xWO6 (0 ≤ x ≤0.2)')
        self.assertKeywordsEqual(
            parsed, [
                'A. Inorganic compounds',
                'B. Luminescence',
                'B. Optical properties',
                'C. XAFS',
                'D. Electronic structure',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 2),
                ('$$Experimental$$Starting materials', 1),
                ('$$Experimental$$Synthesis of Lu2(1−x)Eu2xWO6 (0 ≤ x ≤ 0.20)', 1),
                ('$$Experimental$$Electronic structure calculation', 1),
                ('$$Experimental$$Characterization', 3),
                ('$$Results and discussion'
                 '$$Electronic structure and optical properties of Lu2(1−x)Eu2xWO6 (x = 0, 0.1)', 3),
                ('$$Results and discussion'
                 '$$Valency state and coordination number of Eu ion in Lu1.8Eu0.2WO6', 1),
                ('$$Results and discussion'
                 '$$Thermal quenching mechanism of Lu1.8Eu0.2WO6', 1),
                ('$$Results and discussion'
                 '$$Concentration mechanism of Lu2−2xEu2xWO6 (0.05 ≤ x ≤0.2)', 1),
                ('$$Conclusions', 1),
            ]
        )
        self.assertMaterialMentioned(
            parsed,
            ['Lu2WO6', 'Lu2(1−x)Eu2xWO6', 'Lu1.8Eu0.2WO6', 'CdWO4'],
            ['Lu2WO6 ']
        )
