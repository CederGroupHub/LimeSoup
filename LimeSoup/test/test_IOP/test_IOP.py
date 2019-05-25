from LimeSoup.IOPSoup import IOPSoup
from LimeSoup.test.soup_tester import SoupTester



class TestParsing(SoupTester):
    Soup = IOPSoup

    def test_paper_JPCM(self):
        parsed = self.get_parsed('cm_28_9_094014.xml', __file__)

        self.assertDOIEqual(parsed, '10.1088/0953-8984/28/9/094014')
        self.assertJournalEqual(parsed, 'Journal of Physics: Condensed Matter')
        self.assertTitleEqual(
            parsed,
            'Surface etching, chemical modification and characterization of silicon nitride and silicon oxide—selective functionalization of Si3N4 and SiO2')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Materials', 1),
                ('$$Surface cleaning and etching',1 ),
                ('$$Alkylsiloxane reaction conditions', 1),
                ('$$SC-1 treatment on alkylsiloxane-terminated surfaces', 1),
                ('$$Aldehyde reaction conditions',1 ),
                ('$$Surface characterization techniques: IRAS, XPS, GCIB, LEIS, contact angle, and AFM',5 ),
                ('$$Results and discussions',1 ),
                ('$$Chemical composition and stability of HF-etched Si3N4 films', 2),
                ('$$Characterization of HF-etched Si3N4 samples.',2),
                ('$$Chemical bonding of fluorine and oxygen on HF-etched Si3N4 surfaces.', 6),
                ('$$Quantification of fluorine surface coverage on HF-etched Si3N4.', 1),
                ('$$Detection of surficial Si–NH2 bonds on HF-etched Si3N4 surfaces.', 4),
                ('$$Stability of the HF(aq)-etched Si3N4 surface in water.', 10),
                ('$$Chemical functionalization of HF(aq)-etched Si3N4 films', 2),
                ('$$Reaction of etched surfaces of Si3N4 or SiO2 surfaces with CDMODS.', 2),
                ('$$Characterization of surfaces after surface modification with alkylsiloxanes.', 3),
                ('$$Examining selectivity with organosilanes: reaction of HF(aq)-etched surfaces of Si3N4 or SiO2 with other organosilanes.',1 ),
                ('$$Schiff-base-style reaction with surficial –NH2 modes of the HF(aq)-etched Si3N4 surface and quantification of the surficial –NH2 concentration.',2 ),
                ('$$Procedure for selective functionalization.',3 ),
                ('$$Discussion of the etching mechanism and surface chemical composition of Si3N4 in HF(aq)', 9),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_Materials_Research_Express(self):
        parsed = self.get_parsed('mrx_3_9_095008.xml', __file__)

        self.assertDOIEqual(parsed, '10.1088/2053-1591/3/9/095008')
        self.assertJournalEqual(parsed, 'Materials Research Express')
        self.assertTitleEqual(
            parsed,
            "Implication of potassium trimolybdate nanowires as highly sensitive and selective ammonia sensor at room temperature"
            )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Synthesis of K2Mo3O10.4H2O nanowires', 1),
                ('$$Preparation of microspaced electrodes', 1),
                ('$$Gas sensing studies', 1),
                ('$$Results and discussion', 13),
                ('$$Conclusions', 5),
            ]
        )

    def test_paper_Smart_Materials_and_Structures(self):
        parsed = self.get_parsed('sms_25_12_125015.xml', __file__)

        self.assertDOIEqual(parsed, '10.1088/0964-1726/25/12/125015')
        self.assertJournalEqual(parsed, 'Smart Materials and Structures')
        self.assertTitleEqual(
            parsed,
            'High performance of macro-flexible piezoelectric energy harvester using a 0.3PIN-0.4Pb(Mg1/3Nb2/3)O3-0.3PbTiO3 flake array')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Device fabrication', 1),
                ('$$Experiment methods', 4),
                ('$$Theoretical analysis', 1),
                ('$$Results and discussion', 3),
                ('$$Conclusion', 1),
            ]
        )

    def test_paper_2D_Materials(self):
        parsed = self.get_parsed('2dm_3_1_011003.xml', __file__)

        self.assertDOIEqual(parsed, '10.1088/2053-1583/3/1/011003')
        self.assertJournalEqual(parsed, '2D Materials')
        self.assertTitleEqual(
            parsed,
            'Low tension graphene drums for electromechanical pressure sensing')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 2),
                ('$$Fabrication', 5),
                ('$$Resonance measurements', 4),
                ('$$Pressure sensing', 2),
                ('$$Conclusion', 1),
            ]
        )

    def test_paper_Nanotechnology(self):
        parsed = self.get_parsed('nano11_13_135302.xml', __file__)

        self.assertDOIEqual(parsed, '10.1088/0957-4484/22/13/135302')
        self.assertJournalEqual(parsed, 'Nanotechnology')
        self.assertTitleEqual(
            parsed,
            'Wettability control by DLC coated nanowire topography')
        self.assertKeywordsEqual(
            parsed,  []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Materials preparation', 2),
                ('$$Surface characterization', 1),
                ('$$Results and discussion', 9),
                ('$$Conclusions', 1),
            ]
        )
    def test_paper_Russian_Chemical_Reviews(self):
        parsed = self.get_parsed('RCR_83_2_143.xml', __file__)

        self.assertDOIEqual(parsed, '10.1070/RC2014v083n02ABEH004377')
        self.assertJournalEqual(parsed, 'Russian Chemical Reviews')
        self.assertTitleEqual(
            parsed,
            'Prediction of protein post-translational modifications: main trends and methods')
        self.assertKeywordsEqual(
            parsed,  []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 10),
                ('$$Interactions responsible for the specificity of post-translational modifications', 6),
                ('$$Structural features of the neighbouring environment of modification sites', 2),
                ('$$Information resources', 9),
                ('$$General aspects', 5),
                ('$$Prediction of phosphorylation', 34),
                ('$$Prediction of acetylation at lysine residues', 6),
                ('$$Prediction of glycosylation', 4),
                ('$$Conclusion', 6),
            ]
        )
