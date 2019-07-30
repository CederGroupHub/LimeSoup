import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.paragraphs import extract_paragraphs_recursive, get_tag_text
from LimeSoup.parser.parser_paper import ParserPaper

__author__ = 'Jason Madeano, Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'Jason.Madeano@shell.com,haoyan.huo@lbl.gov'
__version__ = '0.3.0'


class NatureRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'small'},
                 {'name': 'sub'},
                 {'name': 'span', 'class': 'small_caps'},
                 {'name': 'b'},
                 {'name': 'i'},
                 {'name': 'sup'},
                 {'name': 'span', 'class': 'italic'},
                 {'name': 'span', 'class': 'bold'},
                 {'name': 'strong'},
                 {'name': 'span', 'class': 'small_caps'}]

        parser.operation_tag_remove_space(rules)
        # Remove some specific all span that are inside of a paragraph 'p'
        parser.strip_tags(rules)
        return parser


class NatureRemoveTrash(RuleIngredient):
    """
    Selects the article div and removes all of the excess (ie. the sidebar,
    Nature contact info, etc). Also strips the items listed below.
    """

    @staticmethod
    def _parse(parser):
        # Tags to be removed from the HTML paper ECS
        list_remove = [
            {'name': 'li', 'itemprop': 'citation'},  # Citations/References
            {'name': 'div', 'id': 'article-comments-section'},  # Comments
            {'name': 'figure'},  # Figures
            {'name': 'code'},  # Code inside the HTML
            {'name': 'div', 'class': 'figure-at-a-glance'},  # Copy of all figures

            # # Still deciding how to deal with removing all references,
            # # Currently all superscript references are removed.
            # {'name': 'a'}
            {'name': 'a', 'data-track-action': 'figure anchor'},  # Figure Link
            {'name': 'a', 'data-track-action': 'supplementary material anchor'}  # Supplementary Link
        ]
        parser.remove_tags(rules=list_remove)

        return parser


class NatureCollectMetadata(RuleIngredient):
    """
    Collect metadata such as Title, Journal Name, DOI and Content Type.
    """

    @staticmethod
    def _parse(parser):
        # This dictionary structure should match other parsers,
        # "Valid Article" and "Content Type" are specific to Nature Parser
        doi = parser.extract_first_meta('citation_doi')
        if doi is None:
            doi = parser.extract_first_meta('prism.doi')
        if doi is not None:
            doi = re.sub(r'^doi:\s*', '', doi)
            doi = re.sub(r'\s+', '', doi)

        # TODO: We can actually use heuristics to get the title as <h1>.
        # this can be implemented later.
        title = parser.extract_first_meta('citation_title')
        if title is None:
            title = parser.extract_first_meta('twitter:title')
        if title is not None:
            title = re.sub(r'\s+', ' ', title)

        journal = parser.extract_first_meta('citation_journal_title')

        # FIXME: separate keywords into single words by comma
        keywords = parser.extract_meta('keywords')
        article_type = parser.extract_first_meta('WT.cg_s')
        obj = {
            'Content Type': article_type,
            'DOI': doi,
            'Title': title,
            'Keywords': keywords,
            'Journal': journal,
        }

        return [obj, parser]


class NatureExtractArticleBody(RuleIngredient):
    """
    Take the body section out of the HTML DOM.
    """

    @staticmethod
    def _parse(parser_obj):
        obj, parser = parser_obj

        # style 1
        article_body = parser.soup.find(attrs={'data-article-body': 'true'})

        if article_body is None:
            # style 2
            article_body = parser.soup.find('article')
            rules_to_remove = [
                {'name': 'header'},
                {'name': 'nav'},
                {'class': 'article-keywords'},
                {'class': 'figures-at-a-glance'},
            ]
            if article_body:
                for rule in rules_to_remove:
                    for tag in article_body.find_all(**rule):
                        tag.extract()

        if article_body is None:
            raise ValueError('Cannot find article body. You '
                             'should inspect this HTML file carefully.')

        parser = ParserPaper(str(article_body), parser_type='html.parser')

        return [obj, parser]


class NatureCollect(RuleIngredient):
    @staticmethod
    def _parse(parser_obj):
        obj, parser = parser_obj

        ending_sections = [
            re.compile(r'.*?acknowledge?ment.*?', re.IGNORECASE),
            re.compile(r'.*?reference.*?', re.IGNORECASE),
            re.compile(r'.*?author\s*information.*?', re.IGNORECASE),
            re.compile(r'.*?related\s*links.*?', re.IGNORECASE),
            re.compile(r'.*?about\s*this\s*article.*?', re.IGNORECASE),
        ]

        section_status = {
            'should_trim': False
        }

        def trim_sections(sections):
            """
            Remove anything after "ending_sections"
            """
            if isinstance(sections, dict):
                for rule in ending_sections:
                    if not section_status['should_trim']:
                        if rule.match(sections['name']):
                            section_status['should_trim'] = True
                            break

                should_include, secs = trim_sections(sections['content'])
                sections['content'] = secs

                return should_include, sections
            elif isinstance(sections, list):
                final_secs = []
                for sub_sec in sections:
                    should_include, sub_sec = trim_sections(sub_sec)
                    if should_include:
                        final_secs.append(sub_sec)

                return len(final_secs) > 0, final_secs
            else:
                return not section_status['should_trim'], sections

        raw_sections = extract_paragraphs_recursive(parser.soup)

        should_include, trimmed_sections = trim_sections(raw_sections)

        # Fix abstract, if the first element is just a plain text.
        if len(trimmed_sections) > 1 and \
                isinstance(trimmed_sections[0], str) and \
                isinstance(trimmed_sections[1], dict):
            trimmed_sections[0] = {
                'type': 'section_abstract_heuristics',
                'name': 'Abstract',
                'content': [trimmed_sections[0]],
            }
        obj['Sections'] = trimmed_sections

        return obj


NatureSoup = Soup(parser_version=__version__)
NatureSoup.add_ingredient(NatureRemoveTagsSmallSub())
NatureSoup.add_ingredient(NatureRemoveTrash())
NatureSoup.add_ingredient(NatureCollectMetadata())
NatureSoup.add_ingredient(NatureExtractArticleBody())
NatureSoup.add_ingredient(NatureCollect())
