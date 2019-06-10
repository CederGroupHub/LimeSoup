from LimeSoup.ElsevierSoup import ElsevierSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = ElsevierSoup

    def test_paper_regular(self):
        parsed = self.get_parsed('10.1016-j.chroma.2013.12.003.xml', __file__)

        self.assertJournalEqual(parsed, 'Journal of Chromatography A')
        self.assertTitleEqual(
            parsed,
            'Accurate measurements of the true column efficiency and of the instrument '
            'band broadening contributions in the presence of a chromatographic column')
        self.assertKeywordsEqual(
            parsed, [
                'Column efficiency',
                'Intrinsic efficiency',
                'vHPLC systems',
                'Homologous compounds',
                'Extra-column band broadening',
                'Sub-2 μm core–shell particles',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Theory$$Band variance under isocratic and quasi-isocratic conditions', 2),
                ('$$Theory$$Relationship between the apparent and the intrinsic HETP', 4),
                ('$$Experimental$$Chemicals', 1),
                ('$$Experimental$$Instruments', 21),
                ('$$Experimental$$Columns', 1),
                ('$$Experimental$$Total porosities', 1),
                ('$$Experimental$$Peak first and second central moments', 3),
                ('$$Experimental$$HETP measurements', 2),
                ('$$Results and discussion', 1),
                ('$$Results and discussion'
                 '$$Difficulties in estimating the true column and instrument performance', 2),
                ('$$Results and discussion'
                 '$$Validation of a method estimating the true column and instrument performance', 12),
                ('$$Results and discussion'
                 '$$Application of the method to the determination of the intrinsic efficiency '
                 'of 2.1 mm × 100 mm column packed with prototype 1.6 μm core–shell particles', 2),
                ('$$Conclusion', 3),
            ]
        )

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

    def test_paper_no_headings(self):
        parsed = self.get_parsed('10.1016-S0168-9002(01)01806-X.xml', __file__)

        self.assertJournalEqual(parsed, 'Nuclear Instruments and Methods in Physics Research Section A: '
                                        'Accelerators, Spectrometers, Detectors and Associated Equipment')
        self.assertTitleEqual(
            parsed,
            'List of participants')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('', 234),
            ]
        )

    def test_paper_no_full_text(self):
        parsed = self.get_parsed('10.1016-j.phpro.2013.10.018.xml', __file__)

        self.assertJournalEqual(parsed, 'Physics Procedia')
        self.assertTitleEqual(
            parsed,
            'Electrical and Optical Spectroscopic Study of Gd Doped GaN Epitaxial Layers')
        self.assertKeywordsEqual(
            parsed, [
                'Dilute magnetic semiconductors',
                'ferromagnetism',
                'point defects',
                'photoluminescence.']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
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

    def test_paper_desalination(self):
        parsed = self.get_parsed('10.1016-j.desal.2010.05.020.xml', __file__)

        self.assertJournalEqual(parsed, 'Desalination')
        self.assertTitleEqual(
            parsed,
            'Natural radioactivity in various surface waters in Adana, Turkey')
        self.assertKeywordsEqual(
            parsed, [
                'α Activity',
                'β Activity',
                'Drinking water',
                'Surface water',
                'Radioactivity',
                'Effective dose equivalent',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 12),
                ('$$Materials and methods', 2),
                ('$$Materials and methods$$Measurement of gross α and gross-β in surface waters', 3),
                ('$$Materials and methods$$Determination of the effective dose equivalent', 2),
                ('$$Results and discussion', 7),
                ('$$Conclusions', 2),
            ]
        )
        self.assertMaterialMentioned(
            parsed,
            ['U-238', 'K-40'],
        )

    def test_paper_jcat(self):
        parsed = self.get_parsed('10.1016-j.jcat.2009.11.006.xml', __file__)

        self.assertJournalEqual(parsed, 'Journal of Catalysis')
        self.assertTitleEqual(
            parsed,
            'Solar light photocatalytic hydrogen production from water over Pt and Au/TiO2(anatase/rutile) '
            'photocatalysts: Influence of noble metal and porogen promotion')
        self.assertKeywordsEqual(
            parsed, [
                'H2 production',
                'Photocatalysis',
                'Water splitting',
                'Pt/TiO2',
                'Au/TiO2',
                'Template-assisted sol–gel synthesis',
                'Methanol',
                'Sacrificial reagent',
                'Solar light',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experimental$$Material synthesis', 3),
                ('$$Experimental$$Characterization techniques', 7),
                ('$$Experimental$$Experimental device and procedure', 1),
                ('$$Results on Pt/sol–gel TiO2 (anatase/rutile)-porogen modified, Pt/TiO2-P'
                 '$$Characterization results of the sol–gel TiO2-P supports', 8),
                ('$$Results on Pt/sol–gel TiO2 (anatase/rutile)-porogen modified, Pt/TiO2-P'
                 '$$Photocatalytic water splitting results', 4),
                ('$$Results on Au/TiO2-P samples', 1),
                ('$$Results on Au/TiO2-P samples$$Characterization results', 8),
                ('$$Results on Au/TiO2-P samples$$Photocatalytic water splitting results', 3),
                ('$$Discussion', 8),
                ('$$Conclusion', 1),
            ]
        )
        self.assertMaterialMentioned(
            parsed,
            ['TiO2', 'CO2', 'CO'],
        )
