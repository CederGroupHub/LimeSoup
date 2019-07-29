import os
from unittest import TestCase

from LimeSoup.ElsevierSoup import classify_code_type
from LimeSoup.ElsevierSoup_XML import ElsevierXMLSoup
from LimeSoup.test.soup_tester import SoupTester


class TestCodeClassifier(TestCase):
    def test_all_xml(self):
        xml_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'xml',
        )
        for fn in os.listdir(xml_dir):
            with open(os.path.join(xml_dir, fn), encoding='utf8') as f:
                raw_string = f.read()
                self.assertEqual(classify_code_type(raw_string), 'XML')


class TestParsing(SoupTester):
    Soup = ElsevierXMLSoup

    def test_paper_regular(self):
        parsed = self.get_parsed('xml/10.1016-j.chroma.2013.12.003.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1006-jcis.1997.5095.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.apsusc.2009.04.100.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.jiec.2013.10.024.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-S0168-9002(01)01806-X.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.phpro.2013.10.018.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.materresbull.2015.04.014.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.desal.2010.05.020.xml', __file__)

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
        parsed = self.get_parsed('xml/10.1016-j.jcat.2009.11.006.xml', __file__)

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

    def test_paper_ce_list(self):
        parsed = self.get_parsed('xml/10.1016-j.fluid.2014.06.008.xml', __file__)

        self.assertJournalEqual(parsed, 'Fluid Phase Equilibria')
        self.assertTitleEqual(
            parsed,
            'Aqueous two-phase system of poly ethylene glycol dimethyl ether 2000 and '
            'sodium hydroxide at different temperatures: Experiment and correlation')
        self.assertKeywordsEqual(
            parsed, [
                "Liquid–liquid equilibrium",
                "Poly ethylene glycol dimethyl ether",
                "Sodium hydroxide, Setschenow equation, Local composition model"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 5),
                ('$$Materials and methods$$Materials', 1),
                ('$$Materials and methods$$Apparatus and procedure', 2),
                ('$$Results and discussion$$Experimental results', 2),
                ('$$Results and discussion$$Effect of polymer', 1),
                ('$$Results and discussion$$Effect of anion', 1),
                ('$$Correlation$$Correlation of binodal curve', 4),
                ('$$Correlation$$Tie-line correlation', 1),
                ('$$Correlation$$Tie-line correlation$$Othmer–Tobias and Bancroft equations', 1),
                ('$$Correlation$$Tie-line correlation$$Setschenow-type equation', 2),
                ('$$Correlation$$Tie-line correlation$$Local composition NRTL models', 8),
                ('$$Correlation$$Estimated plait point, slope and the length of tie-lines', 3),
                ('$$Correlation$$The free energies of the cloud point (CP)', 5),
                ('$$Conclusion', 3),
                ('$$List of symbols', 40),
            ]
        )
        self.assertMaterialMentioned(
            parsed,
            ['PEGDME2000'],
        )

    def test_paper_xml_syntax_error(self):
        parsed = self.get_parsed('xml/10.1016-j.fluid.2017.10.031.xml', __file__)

        self.assertJournalEqual(parsed, 'Fluid Phase Equilibria')
        self.assertTitleEqual(
            parsed,
            'On fundamentally-based and thermodynamically-consistent description '
            'of dilute multicomponent solutions: Formal results, microscopic '
            'interpretations, and modeling implications')
        self.assertKeywordsEqual(
            parsed, [
                "Multicomponent solutions",
                "Maxwell relations",
                "Gibbs-Duhem relation",
                "Kirkwood-Buff",
                "Henry's constant",
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 8),
                ('$$Isobaric-isothermal composition truncated perturbation '
                 'expansion of the partial molar properties of species in dilute quaternary solutions', 15),
                ('$$Molecular-based interpretation of the expansion coefficients kij(T,P)', 13),
                ('$$Special types of systems and species\' intermolecular asymmetries', 1),
                ('$$Special types of systems and species\' intermolecular asymmetries'
                 '$$Species partial molar fugacity coefficients for quaternary mixtures '
                 'of imperfect gases: second-order perturbation versus truncated virial EoS approaches', 6),
                ('$$Special types of systems and species\' intermolecular asymmetries'
                 '$$Solvation of mixed gases in mixed solvents', 7),
                ('$$Special types of systems and species\' intermolecular asymmetries'
                 '$$Mixed-solutes in a single solvent', 2),
                ('$$Special types of systems and species\' intermolecular asymmetries'
                 '$$Lewis-Randall ideality between solvents or/and solutes', 22),
                ('$$Discussion and concluding remarks', 15),
                ('$$Dedication', 1),
            ]
        )

    def test_paper_xml_bad_definition(self):
        parsed = self.get_parsed('xml/10.1016-S1388-2481(01)00138-2.xml', __file__)

        self.assertJournalEqual(parsed, 'Electrochemistry Communications')
        self.assertTitleEqual(
            parsed,
            'Voltammetry at a liquid–liquid interface supported on a metallic electrode')
        self.assertKeywordsEqual(
            parsed, [
                "ITIES",
                "Ion transfer",
                "Electron transfer"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experimental$$Chemicals', 2),
                ('$$Experimental$$Electrochemical cell and measurements', 3),
                ('$$Results and discussion$$Study of ion transfer reactions at the supported ITIES', 12),
                ('$$Results and discussion$$Potential window', 8),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_xml_term_no_desc(self):
        parsed = self.get_parsed('xml/10.1016-j.icheatmasstransfer.2004.04.029.xml', __file__)

        self.assertJournalEqual(parsed, 'International Communications in Heat and Mass Transfer')
        self.assertTitleEqual(
            parsed,
            'Mixed convection with heat and mass transfer in horizontal tubes')
        self.assertKeywordsEqual(
            parsed, [
                "Heat and Mass transfer",
                "Mixed convection",
                "Lewis number effect",
                "Horizontal tubes"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 2),
                ('$$Problem formulation and numerical procedure', 4),
                ('$$Results and discussion', 4),
                ('$$Conclusion', 36),
            ]
        )

    def test_paper_formula_in_formula(self):
        parsed = self.get_parsed('xml/10.1016-S0927-0248(00)00408-6.xml', __file__)

        self.assertJournalEqual(parsed, 'Solar Energy Materials and Solar Cells')
        self.assertTitleEqual(
            parsed,
            'Calculation of the PV modules angular losses under '
            'field conditions by means of an analytical model')
        self.assertKeywordsEqual(
            parsed, [
                "PV modules",
                "Optical losses",
                "Angular losses",
                "Reflectance"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 3),
                ('$$The PV module angular losses', 2),
                ('$$Analytical model for the reflectance of a PV module$$The model expression', 1),
                ('$$Analytical model for the reflectance of a PV module'
                 '$$Model-fitting performance with analytical results', 3),
                ('$$Analytical model for the reflectance of a PV module'
                 '$$Validation of the model with experimental results$$Experimental method', 1),
                ('$$Analytical model for the reflectance of a PV module'
                 '$$Validation of the model with experimental results'
                 '$$Regression analysis with the experimental data', 1),
                ('$$Analytical model for the reflectance of a PV module'
                 '$$The effect of superficial dust on the model parameters', 2),
                ('$$Corrected expression of Isc with angular losses', 3),
                ('$$Angular losses calculation at different European sites', 1),
                ('$$Angular losses calculation at different European sites$$Monthly average losses', 1),
                ('$$Angular losses calculation at different European sites'
                 '$$Annual losses: The latitude and tilt angle influence', 3),
                ('$$Angular losses calculation at different European sites'
                 '$$The dust influence in the average angular losses', 1),
                ('$$Conclusions', 1),
            ]
        )

        self.assertMaterialMentioned(
            parsed, [
                'Isc=I\u0304scG\u0304Bcos\u03b11\u2212FB(\u03b2)+D1+'
                'cos\u03b221\u2212FD(\u03b2)+A1\u2212cos\u03b221\u2212FA(\u03b2),'
            ])
