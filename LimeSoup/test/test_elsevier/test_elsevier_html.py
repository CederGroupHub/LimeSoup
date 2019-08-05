import os
from unittest import TestCase

from LimeSoup.ElsevierSoup import classify_code_type
from LimeSoup.ElsevierSoup_HTML import ElsevierHTMLSoup
from LimeSoup.test.soup_tester import SoupTester


class TestCodeClassifier(TestCase):
    def test_all_html(self):
        html_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'html',
        )
        for fn in os.listdir(html_dir):
            with open(os.path.join(html_dir, fn), encoding='utf8') as f:
                raw_string = f.read()
                self.assertEqual(classify_code_type(raw_string), 'HTML')


class TestParsing(SoupTester):
    Soup = ElsevierHTMLSoup

    def test_paper_mit_old(self):
        parsed = self.get_parsed('html/10.1016-j.ceramint.2013.07.151.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Phase formation, microstructure and magnetic properties '
            'of (1−x)BiFeO3–x(0.9Pb(Mg1/3Nb2/3)O3–0.1PbTiO3) system')
        self.assertKeywordsEqual(
            parsed, [
                "B. Composites",
                "C. Magnetic properties",
                "Multiferroic",
                "BiFeO3-based ceramics"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 3),
                ('$$Experimental', 2),
                ('$$Results and discussion', 6),
                ('$$Conclusions', 1),
            ]
        )

        self.assertMaterialMentioned(
            parsed,
            ['PMN–PT', 'PbO', 'MgO', 'Nb2O5', 'TiO2'],
        )

    def test_paper_mit_old_graphical_abs(self):
        parsed = self.get_parsed('html/10.1016-j.molcata.2007.11.002.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Selective oxidation of sulfide catalyzed by peroxotungstate immobilized '
            'on ionic liquid-modified silica with aqueous hydrogen peroxide')
        self.assertKeywordsEqual(
            parsed, [
                "Peroxotungstate",
                "Hydrogen peroxide",
                "Ionic liquid-modified silica"
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Graphical abstract', 1),
                ('$$Introduction', 2),
                ('$$Experimental$$Materials and apparatus', 2),
                ('$$Experimental$$Synthesis of catalysts'
                 '$$Preparation of SiO2-1', 2),
                ('$$Experimental$$Synthesis of catalysts'
                 '$$Preparation of ionic liquid-modified silica SiO2–2-Im', 1),
                ('$$Experimental$$Synthesis of catalysts'
                 '$$Preparation of supported peroxotungstate immobilized on ionic liquid-modified silica SiO2–W2–Im',
                 2),
                ('$$Experimental$$General procedure of catalytic oxidation experiments'
                 '$$A typical procedure for the selective oxidation of sulfides to sulfoxides', 1),
                ('$$Experimental$$General procedure of catalytic oxidation experiments'
                 '$$A typical procedure for the selective oxidation of sulfides to sulfones', 1),
                ('$$The results and discussion$$Catalysts preparation', 1),
                ('$$The results and discussion$$Characterization of the intermediates and catalysts', 1),
                ('$$The results and discussion$$IR spectral study', 1),
                ('$$The results and discussion$$Catalytic abilities of catalysts'
                 '$$Oxidation of sulfides to sulfoxides', 4),
                ('$$The results and discussion$$Catalytic abilities of catalysts'
                 '$$Recycle ability of the catalyst', 1),
                ('$$The results and discussion$$Catalytic abilities of catalysts'
                 '$$Oxidation of sulfides to sulfones', 1),
                ('$$Conclusion', 1),
            ]
        )

    def test_paper_mit_old_empty(self):
        parsed = self.get_parsed('html/10.1016-0040-4039(96)01904-1.html', __file__)

        self.assertTitleEqual(
            parsed,
            'The importance of pyridine complexation on selective '
            'oxidation within the Fe(III)Fe(V) manifold in Gif chemistry')
        self.assertIsNone(
            parsed['Keywords']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 2),
            ]
        )

    def test_paper_mit_formula_embedded(self):
        parsed = self.get_parsed('html/10.1016-j.jeurceramsoc.2007.03.025.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Synthesis, densification and electrical properties of strontium cerate ceramics')
        self.assertListEqual(
            parsed['Keywords'], [
                "SrCeO3",
                "Sintering",
                "Electrical conductivity"
            ])
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 9),
                ('$$Experimental$$Powder synthesis and sample preparation', 2),
                ('$$Experimental$$Characterization of sintered materials', 2),
                ('$$Experimental$$Conductivity measurements', 3),
                ('$$Results$$Characterization of powders', 5),
                ('$$Results$$Densification', 2),
                ('$$Results$$Microstructure and grain growth', 1),
                ('$$Results$$Electrical properties', 2),
                ('$$Discussion$$Powder characteristics', 1),
                ('$$Discussion$$Densification and microstructure', 3),
                ('$$Discussion$$Conductivity', 16),
                ('$$Conclusions', 1),
            ]
        )
