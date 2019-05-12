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

    def test_paper_Analyst_paper_2(self):
        parsed = self.get_parsed('10.1039-C5AN00530B.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C5AN00530B')
        self.assertTitleEqual(
            parsed,
            'Nanopore analysis of amyloid fibrils formed by lysozyme aggregation')
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
                ('$$Introduction', 4),
                ('$$Methods', 3),
                ('$$Results', 7),
                ('$$Conclusion', 1),
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

    def test_paper_PCCP_paper(self):
        parsed = self.get_parsed('10.1039-B400730A.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B400730A')
        self.assertTitleEqual(
            parsed,
            'Allyl type radical formation in X-irradiated glutarimide '
            'crystals studied by ENDOR and ENDOR-induced EPR')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Phys. Chem. Chem. Phys.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1. Introduction', 3),
                ('$$2. Experimental details', 7),
                ('$$3. ENDOR results', 3),
                ('$$4. EIE results', 4),
                ('$$5. Radical identification', 8),
                ('$$6. DFT calculations', 1),
                ('$$6. DFT calculations$$α–CH2 structures IV', 3),
                ('$$6. DFT calculations$$Allyl-type radical III', 1),
                ('$$7. Radical formation', 1),
                ('$$8. Conclusion', 1),
            ]
        )

    def test_paper_DT_communication(self):
        parsed = self.get_parsed('10.1039-B513345A.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B513345A')
        self.assertTitleEqual(
            parsed,
            'Group 4 complexes of amine bis(phenolate)s and their application '
            'for the ring opening polymerisation of cyclic esters')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Dalton Trans.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction(guess)', 5),
            ]
        )

    def test_paper_MolBioSyst_review(self):
        parsed = self.get_parsed('10.1039-B515632G.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B515632G')
        self.assertTitleEqual(
            parsed,
            'Microfluidics-based systems biology')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Mol. BioSyst.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1. Introduction', 6),
                ('$$2. Micro-scale biophysics', 5),
                ('$$3. Considerations for studying biological systems', 5),
                ('$$4. Microfluidic components and devices for biological experimentation'
                 '$$4.1. Exploiting microfluidic flow for unique opportunities in experimentation', 10),
                ('$$4. Microfluidic components and devices for biological experimentation'
                 '$$4.2. Experimental platforms for cellular analysis and cellular systems biology', 9),
                ('$$4. Microfluidic components and devices for biological experimentation'
                 '$$4.3. Detection systems and devices for molecular systems biology', 14),
                ('$$4. Microfluidic components and devices for biological experimentation'
                 '$$4.4 Integration of microfluidic components', 3),
                ('$$5. Developing an integrated microfluidic platform for systems biology', 3),
                ('$$6. Concluding remarks', 3),
            ]
        )

    def test_paper_PhotochemPhotobiolSci_paper_many_equations(self):
        parsed = self.get_parsed('10.1039-B517610G.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B517610G')
        self.assertTitleEqual(
            parsed,
            'Re-absorption of chlorophyll fluorescence in leaves revisited. '
            'A comparison of correction models')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Photochem. Photobiol. Sci.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 6),
                ('$$Materials and methods', 14),
                ('$$Results and discussion', 16),
                ('$$Results and discussion'
                 '$$Analysis of the influence of fluorescence emission on reflectance '
                 'and transmittance data used to correct the fluorescence ratio F685/F737', 2),
                ('$$Conclusion', 2),
            ]
        )

    def test_paper_ChemCommun_communication(self):
        parsed = self.get_parsed('10.1039-B710450B.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B710450B')
        self.assertTitleEqual(
            parsed,
            'An i-motif-containing DNA device that breaks certain forms of Watson–Crick interactions')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Chem. Commun.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction(guess)', 8),
            ]
        )

    def test_paper_ChemCommun_communication_2(self):
        parsed = self.get_parsed('10.1039-C0CC04086J.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C0CC04086J')
        self.assertTitleEqual(
            parsed,
            'Rhodium/diene-catalyzed asymmetric arylation of N-sulfonyl indolylimines:'
            ' a new access to highly optically active α-aryl 3-indolyl-methanamines'
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Chem. Commun.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction(guess)', 8),
            ]
        )

    def test_paper_LabChip_communication(self):
        parsed = self.get_parsed('10.1039-C0LC00068J.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C0LC00068J')
        self.assertTitleEqual(
            parsed,
            'Surface-modified microprojection arrays for intradermal biomarker '
            'capture, with low non-specific protein binding'
        )
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Lab Chip'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction(guess)', 14),
            ]
        )

    def test_paper_AnalMethods_paper(self):
        parsed = self.get_parsed('10.1039-C2AY05686K.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C2AY05686K')
        self.assertTitleEqual(
            parsed,
            'Rapid morphological characterization of isolated mitochondria using Brownian motion')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'Anal. Methods'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 3),
                ('$$Methods$$Reagents and buffers', 1),
                ('$$Methods$$Yeast', 1),
                ('$$Methods$$Animals', 1),
                ('$$Methods$$Yeast mitochondrial preparation', 1),
                ('$$Methods$$Mouse mitochondrial preparation', 1),
                ('$$Methods$$Brownian motion measurement', 1),
                ('$$Methods$$Data analysis', 1),
                ('$$Theory', 3),
                ('$$Results and discussion$$Bead calibration', 1),
                ('$$Results and discussion$$Spherical vs. non-spherical particles', 4),
                ('$$Results and discussion$$Yeast mitochondria', 3),
                ('$$Results and discussion$$Comparison of yeast and mouse mitochondria', 1),
                ('$$Results and discussion$$Effect of exercise on mouse mitochondria', 3),
                ('$$Results and discussion$$Assay caveats', 6),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_JMCA_application(self):
        parsed = self.get_parsed('10.1039-C2TA00126H.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C2TA00126H')
        self.assertTitleEqual(
            parsed,
            'Ionic liquid polymer electrolytes')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'J. Mater. Chem. A'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1 Introduction', 3),
                ('$$2 Physical and chemical properties of ILs', 5),
                ('$$3 Applications and requirements of IL-based polymer electrolytes'
                 '$$3.1 High-temperature proton exchange membrane fuel cells (PEMFCs)', 1),
                ('$$3 Applications and requirements of IL-based polymer electrolytes'
                 '$$3.2 Lithium ion batteries', 1),
                ('$$3 Applications and requirements of IL-based polymer electrolytes'
                 '$$3.3 Dye-sensitized solar cells (DSSCs)', 1),
                ('$$3 Applications and requirements of IL-based polymer electrolytes'
                 '$$3.4 Critical requirements for IL-based polymer electrolytes', 4),
                ('$$4 Synthesis routes to prepare IL-based polymer electrolytes', 2),
                ('$$4 Synthesis routes to prepare IL-based polymer electrolytes'
                 '$$4.1 Approaches to polymer doping with ILs', 2),
                ('$$4 Synthesis routes to prepare IL-based polymer electrolytes'
                 '$$4.2 Polymerization/crosslinking of monomers in ILs', 3),
                ('$$4 Synthesis routes to prepare IL-based polymer electrolytes'
                 '$$4.3 Synthesis of polymeric ionic liquids (PILs)', 2),
                ('$$5 Linear polymer containing ionic liquid for use of polymer electrolyte'
                 '$$5.1 Perfluorinated polymer', 8),
                ('$$5 Linear polymer containing ionic liquid for use of polymer electrolyte'
                 '$$5.2 Aromatic polymer', 5),
                ('$$5 Linear polymer containing ionic liquid for use of polymer electrolyte'
                 '$$5.3 Conventional hydrocarbon polymer', 5),
                ('$$5 Linear polymer containing ionic liquid for use of polymer electrolyte'
                 '$$5.4 Block copolymer', 4),
                ('$$5 Linear polymer containing ionic liquid for use of polymer electrolyte'
                 '$$5.5 Polymeric ionic liquids (PILs)', 3),
                ('$$6 Network polymer containing ionic liquid for use in polymer electrolytes', 1),
                ('$$6 Network polymer containing ionic liquid for use in polymer electrolytes'
                 '$$6.1 Preparation of crosslinked ion gels by in situ radical '
                 'polymerization of vinyl monomers in an IL', 3),
                ('$$6 Network polymer containing ionic liquid for use in polymer electrolytes'
                 '$$6.2 Preparation of crosslinked IL-gels by polyaddition reaction '
                 'of monomers/macro-monomers having multifunctional reactive groups', 2),
                ('$$7 Polymer–ionic liquid composite electrolytes', 2),
                ('$$7 Polymer–ionic liquid composite electrolytes'
                 '$$Non-covalently bonded organic–inorganic polymer–ionic liquid composite electrolytes', 3),
                ('$$7 Polymer–ionic liquid composite electrolytes'
                 '$$Covalently bonded organic–inorganic polymer–ionic liquid composite electrolytes', 1),
                ('$$7 Polymer–ionic liquid composite electrolytes'
                 '$$Carbon material-based polymer–ionic liquid composite electrolytes', 3),
                ('$$8 Conclusions', 2),
            ]
        )

    def test_paper_RSCAdv_paper(self):
        parsed = self.get_parsed('10.1039-C3RA22740E.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C3RA22740E')
        self.assertTitleEqual(
            parsed,
            'Enhanced Li adsorption and diffusion in silicon nanosheets based on first principles calculations')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'RSC Adv.'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 5),
                ('$$Methods', 2),
                ('$$Results and discussion$$Model of energetically stable (111) SiNS', 1),
                ('$$Results and discussion$$Lithium insertion sites and binding energies in SiNS', 5),
                ('$$Results and discussion$$Lithium diffusion in SiNS: penetration vs. surface pathways', 7),
                ('$$Results and discussion$$Surface functionalization of SiNS on Li diffusion', 3),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_JMCC_paper_many_equations(self):
        parsed = self.get_parsed('10.1039-C5TC02373D.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C5TC02373D')
        self.assertTitleEqual(
            parsed,
            'Superconductivity in CaSn3 single crystals with a AuCu3-type structure')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'J. Mater. Chem. C'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$I. Introduction', 2),
                ('$$II. Experimental details', 1),
                ('$$III. Results and discussion', 17),
                ('$$IV. Conclusion', 1),
            ]
        )
        self.assertMaterialMentioned(
            parsed,
            [
                'CaPb3', 'LnM3', 'MgCNi3', 'AX3'
            ],
            [
                'CaSn3'
            ]
        )

    def test_paper_CrystEngComm_highlight(self):
        parsed = self.get_parsed('10.1039-C7CE00022G.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C7CE00022G')
        self.assertTitleEqual(
            parsed,
            'Enzyme encapsulation in metal–organic frameworks for applications in catalysis')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'CrystEngComm'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1. Introduction', 2),
                ('$$2. Enzyme immobilization in MOFs', 2),
                ('$$2. Enzyme immobilization in MOFs$$2.1 Enzyme incorporation de novo', 9),
                ('$$2. Enzyme immobilization in MOFs$$2.2 Post-synthetic enzyme incorporation', 9),
                ('$$3. Summary and outlook', 3),
            ]
        )

    def test_paper_CrystEngComm_paper(self):
        parsed = self.get_parsed('10.1039-C003791P.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C003791P')
        self.assertTitleEqual(
            parsed,
            'Enhanced electrochemical catalytic activity of '
            'new nickel hydroxide nanostructures with (100) facet')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertJournalEqual(
            parsed,
            'CrystEngComm'
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experimental details', 1),
                ('$$Experimental details$$Synthesis of various Ni(OH)2 nanostructures', 1),
                ('$$Experimental details$$Electrochemical measurements', 2),
                ('$$Experimental details$$Characterization', 1),
                ('$$Results and discussion', 10),
                ('$$Conclusion', 1),
            ]
        )
