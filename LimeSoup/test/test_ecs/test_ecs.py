from LimeSoup.ECSSoup import ECSSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = ECSSoup

    def test_paper_ecs_detailed_sections(self):
        parsed = self.get_parsed('10.1149-1.1372213.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Gaseous Impurities in Co Silicidation: Impact and Solutions')
        self.assertKeywordsEqual(
            parsed, [
                'cobalt compounds',
                'impurities',
                'integrated circuit manufacture',
                'rapid thermal processing',
                'thermally stimulated desorption',
                'mass spectroscopic chemical analysis',
                'semiconductor-metal boundaries',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('', 3),
                ('$$Experimental$$Sample preparation', 1),
                ('$$Experimental$$Desorption test and APIMS analysis', 4),
                ('$$Experimental$$X-ray photoelectron spectroscopy (XPS) characterization', 1),
                ('$$Results$$Desorption of moisture (H2O)', 5),
                ('$$Results$$Desorption of oxygen (O2)', 2),
                ('$$Results$$Desorption of carbon dioxide (CO2)', 2),
                ('$$Results$$Desorption of NH3 (m/e=17)', 1),
                ('$$Results$$XPS analyses', 2),
                ('$$Discussion$$Main impurities and their sources', 1),
                ('$$Discussion$$Thermodynamic considerations', 4),
                ('$$Discussion$$Detrimental impact of gaseous impurities', 3),
                ('$$Discussion'
                 '$$Impact of thermal desorption from the dielectrics used as field isolation or spacer', 2),
                ('$$Discussion$$Analyses of technical solutions', 6),
                ('$$Conclusions', 5),
            ]
        )

    def test_paper_ecs_flat_sections(self):
        parsed = self.get_parsed('10.1149-1.1887166.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Electrochemical and Spectroscopic Properties of Electrospun PAN-Based Fibrous Polymer Electrolytes')
        self.assertKeywordsEqual(
            parsed, [
                'lithium',
                'polymer electrolytes',
                'polymer fibres',
                'porous materials',
                'membranes',
                'nanostructured materials',
                'ionic conductivity',
                'Raman spectra',
                'Fourier transform spectra',
                'secondary cells',
            ]
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('', 4),
                ('$$Experimental', 8),
                ('$$Results and Discussion', 15),
                ('$$Conclusion', 4),
            ]
        )

    def test_paper_ecs_no_keywords(self):
        parsed = self.get_parsed('10.1149-2.012305jes.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Phase Transition Analysis between LiFePO4 and FePO4 by '
            'In-Situ Time-Resolved X-ray Absorption and X-ray Diffraction')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('', 2),
                ('$$Experimental', 2),
                ('$$Results and Discussion', 6),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_ecs_list(self):
        parsed = self.get_parsed('10.1149-2.033408jes.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Design of Membrane-Encapsulated Wireless Photoelectrochemical Cells for Hydrogen Production')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('', 13),
                ('$$Background', 5),
                ('$$Theory', 1),
                ('$$Theory$$Gas transport', 5),
                ('$$Theory$$Proton transport and potential distribution', 5),
                ('$$Theory$$Heat transport', 7),
                ('$$Theory$$Water transport', 4),
                ('$$Results', 1),
                ('$$Results$$Design space for efficient gas transport', 7),
                ('$$Results$$Design space for efficient gas transport$$Use of gas channels', 5),
                ('$$Results$$Design space for proton transport', 5),
                ('$$Results$$Design space for heat transport', 7),
                ('$$Results$$Design space for water transport', 2),
                ('$$Discussion', 6),
                ('$$Conclusions', 1),
                ('$$Appendix I: Supersaturation Distribution of Gases in Membrane Channels', 1),
                ('$$Appendix II: Potential Distribution in Membrane Encapsulated PECs', 3),
                ('$$Appendix III: Light Absorption Spectrum of Nafion', 1),
            ]
        )

    def test_paper_ecs_content(self):
        parsed = self.get_parsed('10.1149-1.3606475.html', __file__)

        self.assertTitleEqual(
            parsed,
            'Characterizations of LBC-GDC Composite Cathodes for Low Temperature SOFCs')
        self.assertKeywordsEqual(
            parsed, ['barium compounds',
                     'catalysis',
                     'cerium compounds',
                     'composite materials',
                     'electrical resistivity',
                     'electrochemical electrodes',
                     'electrochemical impedance spectroscopy',
                     'gadolinium',
                     'heat treatment',
                     'ionic conductivity',
                     'lanthanum compounds',
                     'materials preparation',
                     'porous materials',
                     'reduction (chemical)',
                     'solid electrolytes',
                     'thermal expansion',
                     'X-ray diffraction']
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('', 3),
                ('$$Experimental$$LBC synthesis and characterization', 1),
                ('$$Experimental$$LBC-GDC composite fabrication', 1),
                ('$$Experimental$$TEC measurements', 1),
                ('$$Experimental$$Electrode fabrication and characterization', 2),
                ('$$Results and Discussion$$XRD measurements', 1),
                ('$$Results and Discussion$$Electrode microstructure', 1),
                ('$$Results and Discussion$$Thermal expansion coefficient (TEC)', 1),
                ('$$Results and Discussion$$Impedance response of symmetrical cell electrodes', 2),
                ('$$Results and Discussion'
                 '$$Comparison of total polarization resistance of different composite electrodes', 3),
                ('$$Results and Discussion'
                 '$$Mechanistic understanding of electrochemical processes', 3),
                ('$$Results and Discussion'
                 '$$Quantification of activation energy of HF and LF resistances', 1),
                ('$$Results and Discussion'
                 '$$pO2 dependency of HF and LF resistances', 3),
                ('$$Conclusions', 1),
            ]
        )

        self.assertNoReference(parsed, 1, ['1', '2', '3', '4'])
        self.assertNoReference(parsed, 2, ['6-9', '12-17'])

        self.assertContainsStrings(parsed, 4, ['153 MPa', '1000°C', '1. 5406 Å'])
