from LimeSoup.WileySoup import WileySoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = WileySoup

    def test_paper_organic_chem(self):
        parsed = self.get_parsed('10.1002-jhet.2172.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/jhet.2172')
        self.assertJournalEqual(parsed, 'Journal of Heterocyclic Chemistry')
        self.assertTitleEqual(
            parsed,
            'Applications of Azoalkenes in the Synthesis of Fused Ring Pyridazine Derivatives')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 2),
                ('$$Results and Discussion', 3),
                ('$$Experimental', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '3-Methyl-2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5b)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '2-Phenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline-3-carbonitrile (5c)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '2-Phenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline-3-carboxylic acid ethyl ester (5d)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '2,3-Diphenyl-3,4,4a,5,6,7-hexahydro-2H-cyclopenta[c]pyridazine (9a)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '3-Methyl-2,3-Diphenyl-3,4,4a,5,6,7-hexahydro-2H-cyclopenta[c]pyridazine (9b)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '2-Phenyl-3,4,4a,5,6,7-hexahydro-2H-cyclopenta[c]pyridazine-3-carbonitrile (9c)', 1),
                ('$$Experimental$$Typical procedure for the preparation of 2,3-diphenyl-2,3,4,4a,5,6,7,8-octahydrocinnoline (5a)$$'
                 '2-Phenyl-3,4,4a,5,6,7-hexahydro-2H-cyclopenta[c]pyridazine-3-carboxylic acid ethyl ester (9d)', 1),
            ]
        )

    def test_paper_anie_bullets(self):
        parsed = self.get_parsed('10.1002-anie.201508702.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/anie.201508702')
        self.assertJournalEqual(parsed, 'Angewandte Chemie International Edition')
        self.assertTitleEqual(
            parsed,
            "A [4+1] Cyclative Capture Approach to 3H‐Indole‐N‐oxides at Room Temperature "
            "by Rhodium(III)‐Catalyzed C--H Activation")
        self.assertKeywordsEqual(
            parsed, [
                "C--H activation", 'cyclizations', 'diazo compounds',
                'heterocycles', 'rhodium'
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 17),
                ('$$Acknowledgements', 1),
            ]
        )

    def test_paper_anie_no_headings(self):
        parsed = self.get_parsed('10.1002-anie.201305377.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/anie.201305377')
        self.assertJournalEqual(parsed, 'Angewandte Chemie International Edition')
        self.assertTitleEqual(
            parsed,
            'Controlling Size‐Induced Phase Transformations Using Chemically Designed Nanolaminates')
        self.assertKeywordsEqual(
            parsed, [
                'chalcogenides', 'layered compounds', 'metastable compounds',
                'nanostructures', 'phase transitions'
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 12),
                ('$$Experimental Section', 1),
            ]
        )

    def test_paper_full_with_bullets(self):
        parsed = self.get_parsed('10.1111-jace.12629.html', __file__)

        self.assertDOIEqual(parsed, '10.1111/jace.12629')
        self.assertJournalEqual(parsed, 'Journal of the American Ceramic Society')
        self.assertTitleEqual(
            parsed,
            'Microstructural Evolution and Growth Behavior of In Situ TiB Whisker Array '
            'in ZrB2–SiC/Ti6Al4V Brazing Joints')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$I. Introduction', 5),
                ('$$II. Materials and Experimental Procedures', 2),
                ('$$III. Results and Discussion$$(1) Thermodynamics', 4),
                ('$$III. Results and Discussion$$(2) Microstructural Evolution of ZS/TC4 Joints', 3),
                ('$$III. Results and Discussion$$(3) Growing Behavior of TiB', 4),
                ('$$III. Results and Discussion$$(4) Mechanical Properties of ZS/TC4 Joints', 2),
                ('$$IV. Conclusion', 1),
                ('$$Acknowledgments', 1),
            ]
        )

    def test_paper_full_simple(self):
        parsed = self.get_parsed('10.1002-mop.29251.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/mop.29251')
        self.assertJournalEqual(parsed, 'Microwave and Optical Technology Letters')
        self.assertTitleEqual(
            parsed,
            'Wideband high‐gain low‐profile dual‐polarized stacked patch antenna array with parasitic elements')
        self.assertKeywordsEqual(
            parsed, [
                'dual‐polarized antenna', 'high gain', 'patch antenna', 'parasitic antenna array',
                'wideband antenna',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$ABSTRACT', 1),
                ('$$1. INTRODUCTION', 2),
                ('$$2. THEORY ANALYSIS', 2),
                ('$$2. THEORY ANALYSIS$$2.1. Stacked Patches', 4),
                ('$$2. THEORY ANALYSIS$$2.2. Parasitic Patches', 3),
                ('$$2. THEORY ANALYSIS$$2.3. Feeding Network', 2),
                ('$$3. FABRICATION AND MEASUREMENTS', 4),
                ('$$4. CONCLUSION', 1),
                ('$$ACKNOWLEDGMENTS', 1),
            ]
        )

    def test_paper_full_many_headings(self):
        parsed = self.get_parsed('10.1002-2017JE005343.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/2017JE005343')
        self.assertJournalEqual(parsed, 'Journal of Geophysical Research: Planets')
        self.assertTitleEqual(
            parsed,
            'Dioctahedral Phyllosilicates Versus Zeolites and Carbonates '
            'Versus Zeolites Competitions as Constraints to Understanding '
            'Early Mars Alteration Conditions')
        self.assertKeywordsEqual(
            parsed, [
                'Mars', 'clay minerals', 'carbonates', 'zeolites', 'experiments',
                'geochemical modeling',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1 Introduction', 4),
                ('$$2 Martian Zeolites$$2.1 Remote Sensing Detection of Zeolites', 1),
                ('$$2 Martian Zeolites$$2.2 Absence and Controversial Detection of Zeolites', 1),
                ('$$2 Martian Zeolites$$2.3 Reliable Zeolite Detections', 3),
                ('$$2 Martian Zeolites$$2.4 Possible Process of Formation', 2),
                ('$$3 Materials and Methods$$3.1 Starting Material and Sample Preparation', 1),
                ('$$3 Materials and Methods$$3.2 Experimental Setup and Procedure', 1),
                ('$$3 Materials and Methods$$3.3 Solid Phase Analysis$$3.3.1 X‐Ray Diffraction Analysis', 1),
                ('$$3 Materials and Methods$$3.3 Solid Phase Analysis$$3.3.2 Near‐Infrared Analysis', 1),
                ('$$3 Materials and Methods$$3.4 Geochemical Simulation', 4),
                ('$$4 Results$$4.1 Experimental Results', 6),
                ('$$4 Results$$4.2 Geochemical Model Results', 3),
                ('$$5 Discussion$$5.1 pH, a Key to Understanding Mineral Formation Competition', 6),
                ('$$5 Discussion$$5.2 Martian Implications', 4),
                ('$$6 Conclusion and Remarks', 2),
                ('$$Acknowledgments', 1),
            ]
        )

    def test_paper_old_pdf(self):
        parsed = self.get_parsed('10.1002-jcp.1030030403.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/jcp.1030030403')
        self.assertJournalEqual(parsed, 'Journal of Cellular Physiology')
        self.assertTitleEqual(
            parsed,
            'Studies of the electromotive force in biological systems. II. The surface '
            'activity of homologous carbamate solutions')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, []  # nothing really
        )

    def test_paper_old_pdf_with_abs(self):
        parsed = self.get_parsed('10.1111-j.1151-2916.1999.tb01896.x.html', __file__)

        self.assertDOIEqual(parsed, '10.1111/j.1151-2916.1999.tb01896.x')
        self.assertJournalEqual(parsed, 'Journal of the American Ceramic Society')
        self.assertTitleEqual(
            parsed,
            'Tin Oxide Thin‐Film Sensors for Aromatic Hydrocarbons Detection: '
            'Effect of Aging Time on Film Microstructure')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
            ]
        )

    def test_paper_ancillary(self):
        parsed = self.get_parsed('10.1002-adsc.201190008.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/adsc.201190008')
        # Parser need to convert &amp; symbols to their real characters
        self.assertJournalEqual(parsed, 'Advanced Synthesis & Catalysis')
        self.assertTitleEqual(
            parsed,
            'Graphical Abstract: Adv. Synth. Catal. 5/2011')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, []  # nothing really
        )

    def test_paper_without_section_headings(self):
        parsed = self.get_parsed('10.1002-smll.200800808.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/smll.200800808')
        self.assertJournalEqual(parsed, 'Small')
        self.assertTitleEqual(
            parsed,
            'An Assembly Route to Inorganic Catalytic Nanoreactors Containing '
            'Sub‐10‐nm Gold Nanoparticles with Anti‐Aggregation Properties')
        self.assertKeywordsEqual(
            parsed, [
                'anti‐aggregation', 'catalysts', 'encapsulation', 'gold',
                'nanoparticles'
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 12),
                ('$$Experimental Section$$Gold Nanoparticles', 1),
                ('$$Experimental Section$$Au@SiO2 Core–Shell Particles', 1),
                ('$$Experimental Section$$Au@SiO2@ZrO2 Core–Shell Particles', 1),
                ('$$Experimental Section$$Au@hm-ZrO2 Yolk–Shell Particles', 1),
                ('$$Experimental Section$$Gold Nanoparticles Supported on the Surface of hm-ZrO2', 1),
                ('$$Experimental Section$$Catalytic Reduction of p-Nitrophenol', 1),
            ]
        )

    def test_paper_without_section_headings_2(self):
        parsed = self.get_parsed('10.1002-adma.201103895.html', __file__)

        self.assertDOIEqual(parsed, '10.1002/adma.201103895')
        self.assertJournalEqual(parsed, 'Advanced Materials')
        self.assertTitleEqual(
            parsed,
            'Conjugated Polyelectrolyte‐Antibody Hybrid Materials for '
            'Highly Fluorescent Live Cell‐Imaging')
        self.assertKeywordsEqual(
            parsed, [
                'conjugated polyelectrolytes', 'bioimaging', 'B‐lymphocytes',
                'poly(p‐phenyleneethynylenes)', 'antibody labeling'
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$', 9),
                ('$$Supporting Information', 1),
                ('$$Acknowledgements', 1),
            ]
        )
