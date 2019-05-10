from LimeSoup.RSCSoup import RSCSoup

from LimeSoup.test.soup_tester import SoupTester


class TestParsing(SoupTester):
    Soup = RSCSoup

    def test_paper_CrystEngComm_highlight(self):
        parsed = self.get_parsed('10.1039-B201206E.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B201206E')
        self.assertTitleEqual(
            parsed,
            'Database research in crystal engineering')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Historical', 2),
                ('$$Intermolecular interactions', 5),
                ('$$Interaction patterns', 6),
                ('$$Crystal packing', 3),
                ('$$Polymorphism and pseudopolymorphism', 4),
                ('$$Structure-based drug design', 5),
                ('$$Conclusions', 2),
            ]
        )

    def test_paper_CrystEngComm_article(self):
        # Paper 1
        parsed = self.get_parsed('10.1039-B210215C.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B210215C')
        self.assertTitleEqual(
            parsed,
            'Preparation of solvent-free clathrand structures '
            'by the exclusion of an unwelcome guest')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 6),
                ('$$Results and discussion', 5),
                ('$$Results and discussion$$Crystal structure of solvent-free 4', 1),
                ('$$Results and discussion$$Crystal structure of (4)3·(toluene)2', 4),
                ('$$Results and discussion$$The dual-role of the solvent', 4),
                ('$$Conclusions', 1),
                ('$$Experimental$$Structure determinations', 3),
            ]
        )

    def test_paper_CrystEngComm_article_2(self):
        # Paper 2

        parsed = self.get_parsed('10.1039-B210346J.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B210346J')
        self.assertTitleEqual(
            parsed,
            'Influence of alcohol on the morphology of BaSO4 crystals '
            'grown at the air–water interface')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 3),
                ('$$Experimental', 3),
                ('$$Results and discussion', 8),
                ('$$Conclusions', 1),
            ]
        )

    def test_paper_CrystEngComm_article_3(self):
        # Paper 3

        parsed = self.get_parsed('10.1039-B304427K.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B304427K')
        self.assertTitleEqual(
            parsed,
            'Unusual ladder-like supramolecular arrangement by cooperative '
            'effect of bifurcated O–H⋯O hydrogen bonding in crystals of '
            'racemic 4-ferrocenylbutan-1,2-diol')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 6),
                ('$$Results and discussion', 15),
                ('$$Experimental$$Synthesis', 2),
                ('$$Experimental$$X-Ray crystallography', 5),
            ]
        )

    def test_paper_CrystEngComm_article_4(self):
        # Paper 4

        parsed = self.get_parsed('10.1039-B718995H.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/B718995H')
        self.assertTitleEqual(
            parsed,
            'Control of the topologies and packing modes of three 2D '
            'coordination polymers through variation of the solvent '
            'ratio of a binary solvent mixture')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 1),
                ('$$Experimental procedure$$Materials and methods', 1),
                ('$$Experimental procedure$$Syntheses', 3),
                ('$$Experimental procedure$$X-Ray crystallography', 1),
                ('$$Results and discussion$$Description of the crystal structures', 5),
                ('$$Discussion', 3),
                ('$$Conclusion', 2),
            ]
        )

    def test_paper_CrystEngComm_article_5(self):
        parsed = self.get_parsed('10.1039-C000028K.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C000028K')
        self.assertTitleEqual(
            parsed,
            'Diverse structural assemblies and variable conductivities '
            'of silver-hexamethylenetetramine coordination polymers with '
            '2-, 3-, and 4-sulfobenzoate ligands')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$Introduction', 4),
                ('$$Experimental$$Materials and physical measurements', 2),
                ('$$Experimental$$Synthesis of {[Ag4(hmt)2(3-sb)2(H2O)2]·2H2O}n (2)', 1),
                ('$$Experimental$$Synthesis of {[Ag3(hmt)2(4-sb)(NO3)(H2O)]·3H2O}n (3)', 1),
                ('$$Experimental$$X-Ray structure determination', 1),
                ('$$Results and discussion$$Synthesis chemistry', 1),
                ('$$Results and discussion$$Crystal structures', 3),
                ('$$Results and discussion$$Coordination modes of sb2− in complexes 1–3', 2),
                ('$$Results and discussion$$Thermal stability behaviour', 1),
                ('$$Results and discussion$$Fluorescent emission', 1),
                ('$$Results and discussion$$Conductivity studies', 2),
                ('$$Conclusion', 1),
            ]
        )

    def test_paper_JMCA(self):
        parsed = self.get_parsed('10.1039-C4TA04073B.html', __file__)

        self.assertDOIEqual(parsed, '10.1039/C4TA04073B')
        self.assertTitleEqual(
            parsed,
            'A fast route for synthesizing nano-sized ZSM-5 aggregates')
        self.assertKeywordsEqual(
            parsed, []
        )
        self.assertSectionPathsEqual(
            parsed, [
                ('$$Abstract', 1),
                ('$$1. Introduction', 4),
                ('$$2. Experimental$$2.1. Synthesis of nano-sized ZSM-5 aggregates', 2),
                ('$$2. Experimental$$2.2. Characterization', 1),
                ('$$2. Experimental$$2.3. Catalytic performance', 2),
                ('$$3. Results and discussion'
                 '$$3.1. Factors affecting the synthesis of nano-sized ZSM-5 aggregates', 8),
                ('$$3. Results and discussion'
                 '$$3.2. Crystallization process of nano-sized ZSM-5 aggregates', 3),
                ('$$3. Results and discussion'
                 '$$3.3. Scheme for the formation of nano-sized ZSM-5 aggregates', 6),
                ('$$3. Results and discussion$$3.4. Catalytic performance', 3),
                ('$$4. Conclusions', 1),
            ]
        )
