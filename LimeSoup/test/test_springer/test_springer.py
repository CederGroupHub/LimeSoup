from LimeSoup.SpringerSoup import SpringerSoup

from LimeSoup.test.soup_tester import SoupTester

from pprint import pprint


# TODO: WHAT is the section type for the paper missing abstract? h2 or h3
# TODO: do we need to parse DOI
# TODO: discuss what it the format of journal/title output

class TestParsing(SoupTester):
    Soup = SpringerSoup

    def test_paper_applied_physics_a(self):
        parsed = self.get_parsed('10.1007_s00339-013-8138-9.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s00339-013-8138-9')
        self.assertJournalEqual(parsed, ['Applied Physics A'])
        self.assertTitleEqual(
            parsed,
            ['Surface nanostructure effects on optical properties of Pb(ZrxTi1−x)O3 thin films']
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1 Introduction', 2),
                ('$$2 Model for diffuse light scattering calculations', 3),
                ('$$3 Experimental details', 3),
                ('$$4 Results and discussion$$4.1 Microstructures', 4),
                ('$$4 Results and discussion$$4.2 Diffuse transmission measurements', 1),
                ('$$4 Results and discussion$$4.3 Diffuse light scattering calculations', 1),
                ('$$5 Conclusions', 2),
                ('$$Acknowledgments', 1),
            ]
        )

    def test_paper_catalysis_letters(self):
        parsed = self.get_parsed('10.1007_s10562-010-0490-1.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s10562-010-0490-1')
        self.assertJournalEqual(parsed, ['Catalysis Letters'])
        self.assertTitleEqual(
            parsed,
            ['One-Pot Synthesis and Characterization of Cu-SBA-16 Mesoporous '
             'Molecular Sieves as an Excellent Catalyst for Phenol Hydroxylation']
        )
        self.assertKeywordsEqual(
            parsed, ['Copper species', 'Cu-SBA-16', 'Phenol hydroxylation']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract$$Abstact', 1),
                ('$$Abstract$$Graphical Abstract', 1),
                ('$$1 Introduction', 3),
                ('$$2 Experimental$$2.1 Synthesis of Cu-SBA-16', 1),
                ('$$2 Experimental$$2.2 Characterization', 2),
                ('$$2 Experimental$$2.3 Catalytic Testing', 1),
                ('$$3 Results and discussion$$3.1 Texture Characterization of Cu-SBA-16$$'
                 '3.1.1 Small-Angle XRD', 1),
                ('$$3 Results and discussion$$3.1 Texture Characterization of Cu-SBA-16$$'
                 '3.1.2 IR spctra', 1),
                ('$$3 Results and discussion$$3.1 Texture Characterization of Cu-SBA-16$$'
                 '3.1.3 N2 Adsorption–Desorption Isotherms', 1),
                ('$$3 Results and discussion$$3.1 Texture Characterization of Cu-SBA-16$$'
                 '3.1.4 TEM', 1),
                ('$$3 Results and discussion$$3.2 Study of Cu Species$$3.2.1 Wide-Angle XRD', 2),
                ('$$3 Results and discussion$$3.2 Study of Cu Species$$3.2.2 H2-TPR', 1),
                ('$$3 Results and discussion$$3.2 Study of Cu Species$$3.2.3 DRUV-Vis Spectra', 1),
                ('$$3 Results and discussion$$3.2 Study of Cu Species$$3.2.4 XPS', 2),
                ('$$3 Results and discussion$$3.3 Hydroxylation of Phenol', 4),
                ('$$4 Conclusion', 1),
                ('$$Notes$$Acknowledgments', 1),
            ]
        )

    def test_paper_european_physical_journal_b(self):
        parsed = self.get_parsed('101140epjbe2017-80152-2.html', __file__)
        # self.assertDOIEqual(parsed, '10.1140/epjb/e2017-80152-2')
        self.assertJournalEqual(parsed, ['The European Physical Journal B'])
        self.assertTitleEqual(
            parsed,
            ['Ab initio study of new sp3 silicon and germanium allotropes '
             'predicted from the zeolite topologies']
        )
        self.assertKeywordsEqual(
            parsed, ['Solid State and Materials']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),

            ]
        )

    def test_paper_old_paper(self):
        parsed = self.get_parsed('10.1007_bf00353117.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/BF00353117')
        self.assertJournalEqual(parsed, ['Journal of Materials Science'])
        self.assertTitleEqual(
            parsed,
            ['Fracture and fracture toughness of stoichiometric '
             'MgAl2O4 crystals at room temperature']
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
            ]
        )

    def test_paper_multi_para_abstract(self):
        parsed = self.get_parsed('10.1007_bf00701095.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/BF00701095')
        self.assertJournalEqual(parsed, ['Journal of Materials Science: Materials in Electronics']
                                )
        self.assertTitleEqual(
            parsed,
            ['TEM studies of RF magnetron-sputtered thin films'])
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 2),
            ]
        )

    def test_paper_empty_paper(self):
        parsed = self.get_parsed('10.1007_bf03378691.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/BF03378691')
        self.assertJournalEqual(parsed, ['JOM'])
        self.assertTitleEqual(
            parsed,
            ['Engineers and the military service']
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, []
        )

    def test_paper_with_table(self):
        parsed = self.get_parsed('10.1007_s10853-011-5258-5.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s10853-011-5258-5')
        self.assertJournalEqual(parsed, ['Journal of Materials Science'])
        self.assertTitleEqual(
            parsed,
            ['Properties of In-N doped ZnO films synthesized by ion beam assisted deposition']
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Introduction', 2),
                ('$$Experiment', 2),
                ('$$Results and discussion', 4),
                ('$$Conclusions', 1),
                ('$$Acknowledgements', 1),

            ]
        )

    def test_paper_many_paras(self):
        parsed = self.get_parsed('10.1007_s10853-015-9171-1.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s10853-015-9171-1')
        self.assertJournalEqual(parsed, ['Journal of Materials Science'])
        self.assertTitleEqual(
            parsed,
            ['A study of the dynamic recrystallization kinetics '
             'of V-microalloyed medium carbon steel']
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experiments', 4),
                ('$$Results', 20),
                ('$$Discussion', 12),
                ('$$Conclusions', 1),
                ('$$Acknowledgements', 1),
            ]
        )

    def test_paper_subsection(self):
        parsed = self.get_parsed('101007s40964-017-0023-1.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s40964-017-0023-1')
        self.assertJournalEqual(parsed, ['Progress in Additive Manufacturing'])
        self.assertTitleEqual(
            parsed,
            ['The manufacture of 3D printing of medical grade TPU']
        )
        self.assertKeywordsEqual(
            parsed, ['Medical grade TPU', '3D printing',
                     'Tensile test', 'Dumbbell specimen', 'FDM']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1 Introduction', 3),
                ('$$2 Experimental section$$2.1 Materials', 1),
                ('$$2 Experimental section$$2.2 Processing$$2.2.1 Extrusion TPU filament', 3),
                ('$$2 Experimental section$$2.2 Processing$$2.2.2 TPU 3D printing', 2),
                ('$$2 Experimental section$$2.3 Characterization methods', 2),
                ('$$3 Fabrication of TPU filament', 3),
                ('$$4 TPU 3D printing', 1),
                ('$$4 TPU 3D printing$$4.1 Tensile test result', 2),
                ('$$4 TPU 3D printing$$4.2 Orientation angle', 4),
                ('$$4 TPU 3D printing$$4.3 Printing temperature', 4),
                ('$$5 Conclusion', 1),
                ('$$Notes$$Acknowledgements', 1),
            ]
        )

    def test_paper_many_subsections(self):
        parsed = self.get_parsed('101007s11671-009-9393-8.html', __file__)
        # self.assertDOIEqual(parsed, '10.1007/s11671-009-9393-8')
        self.assertJournalEqual(parsed, ['Nanoscale Research Letters'])
        self.assertTitleEqual(
            parsed,
            ['The Acute Liver Injury in Mice Caused by Nano-Anatase TiO2']
        )
        self.assertKeywordsEqual(
            parsed, ['Mice', 'Nano-anatase TiO2', 'Liver',
                     'Inflammatory cytokines', 'Histopathological changes']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 5),
                ('$$Materials and Methods$$Chemicals and Preparation', 2),
                ('$$Materials and Methods$$Animals and Treatment', 1),
                ('$$Materials and Methods$$Coefficients of Liver', 1),
                ('$$Materials and Methods$$Preparation of DNA Samples '
                 'from Mouse Liver', 1),
                ('$$Materials and Methods$$Titanium Content Analysis of '
                 'Liver and Liver DNA', 1),
                ('$$Materials and Methods$$Biochemical Analysis of Liver '
                 'Function', 1),
                ('$$Materials and Methods$$Histopathological Examination', 1),
                ('$$Materials and Methods$$Observation of Hepatocyte '
                 'Ultrastructure by TEM', 1),
                ('$$Materials and Methods$$Expression Amount and '
                 'Concentration Assay of Inflammatory Cytokines', 6),
                ('$$Materials and Methods$$Statistical Analysis', 1),
                ('$$Results$$The Enhancement of Body Weight and the '
                 'Coefficients of Liver', 1),
                ('$$Results$$Titanium Contents in Liver and Liver DNA', 1),
                ('$$Results$$Assay of Liver Function', 1),
                ('$$Results$$Liver Histopathological Evaluation', 1),
                ('$$Results$$Hepatocyte Evaluation', 1),
                ('$$Results$$Inflammatory Cytokines in Nano-Anatase '
                 'TiO2-Treated Mice Liver Tissues', 4),
                ('$$Discussion', 5),
                ('$$Conclusion', 1),
                ('$$Misc', 1),
                ('$$Acknowledgements', 1),
            ]
        )

    def test_paper_key_material_0(self):
        parsed = self.get_parsed('10.1007_s00339-013-8138-9.html', __file__)
        self.assertMaterialMentioned(
            parsed,
            materials=[
                'Pb0.97Nd0.02(Zr0.55Ti0.45)O3',
                'MgO',
            ],
            key_materials=[
                'Pb(ZrxTi1−x)O3',
            ]
        )

    def test_paper_key_material_1(self):
        parsed = self.get_parsed('10.1007_bf02663182.html', __file__)
        self.assertMaterialMentioned(
            parsed,
            materials=[
                'YF3',
                'LiF',
            ],
            key_materials=[
                'Y2O3',
            ]
        )

    def test_paper_key_material_2(self):
        parsed = self.get_parsed('10.1007_s10853-011-5258-5.html', __file__)
        self.assertMaterialMentioned(
            parsed,
            materials=[
                'N2',
                'O2',
            ],
            key_materials=[
                'ZnO',
            ]
        )

    def test_paper_key_material_2(self):
        parsed = self.get_parsed('10.1007_bf01142064.html', __file__)
        self.assertMaterialMentioned(
            parsed,
            materials=[],
            key_materials=[
                'Mg2Ni',
            ]
        )

    def test_paper_key_material_2(self):
        parsed = self.get_parsed('10.1007_bf00701095.html', __file__)
        self.assertMaterialMentioned(
            parsed,
            materials=[
                'ScTaO4',
                'PbO',
            ],
            key_materials=[]
        )


