import re

from bs4 import Tag

__author__ = "Tiago Botari, Haoyan Huo"
__maintainer__ = "Haoyan Huo"
__email__ = "haoyan.huo@gmail.com"

INLINE_TAGS = {
    # https://www.w3schools.com/html/html_blocks.asp
    'a', 'abbr', 'acronym', 'b', 'bdo', 'big', 'button', 'cite', 'code', 'dfn',
    'em', 'i', 'img', 'input', 'kbd', 'label', 'map', 'object', 'output', 'q',
    'samp', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'textarea', 'time',
    'tt', 'var'
}

LINEBREAK_ELEMENTS = ['hr', 'br']

NON_DISPLAY_TAGS = {
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element
    'base', 'head', 'link', 'meta', 'style', 'title',
    'applet', 'embed', 'iframe', 'noembed', 'object', 'param', 'picture', 'source',
    'canvas', 'noscript', 'script'
}


def normalize_text(string):
    return re.sub(r'[ \t]+', ' ', string.strip())


def get_tag_text(cur_tag):
    """
    Extracts the current tag's embedded text. The text will be stripped, and
    whitespaces will be removed, just like in a rendered HTML document in a
    web browser.
    """
    strings = []

    for child in cur_tag.contents:
        if child.name is None:
            # this is a pure text
            strings.append(re.sub(r'\n', ' ', child))
        elif child.name in NON_DISPLAY_TAGS:
            pass
        elif child.name in LINEBREAK_ELEMENTS:
            strings.append('\n')
        elif child.name in INLINE_TAGS:
            strings.append(get_tag_text(child))
        else:
            strings.append('\n')
            strings.append(get_tag_text(child))

    return normalize_text(''.join(strings))


def extract_paragraphs_recursive(tag_or_soup, exclude_section_rules=None):
    """
    This function recursively extracts paragraphs from a HTML DOM.

    Section headings such as <h1>, <h2>, <h3>, <h4>, <h5> will be
    used to determine the document hierarchy.

    TODO: write unit tests for this function

    :param tag_or_soup: the Tag or BeautifulSoup object to analyze.
    :type tag_or_soup: bs4.BeautifulSoup or bs4.element.Tag
    :param exclude_section_rules: regular expressions representing
        sections to exclude.
    """

    text_chunks = []

    def find_paragraphs(cur_tag, cur_heading=None):
        """
        Extracts the current tag's embedded text.

        Note that HTML text are rendered according to rules:
        https://www.w3.org/TR/html4/struct/text.html#h-9.1

        In other words, what you type in HTML markup does not necessarily
        end up as what you see. Rather, further formatting and typesetting
        are automatically done by user-agents (web browsers).

        For example, inline elements (such as a <a>, <span>, etc.) won't
        cause a line-break to be inserted; however, a block level element
        (<div>, <ul>) will force a line-break. To address this issue, similar
        rendering behaviors must be reproduced here.

        In this part, we extract text in HTML DOM recursively. Here are the
        basic rules:

        1. Excessive whitespaces will be removed, unless specified by "&nbsp;"
        2. All strings are joined together, unless a block level element is
            followed.
        3. Heading elements <h1> - <h6> controls the hierarchy of paragraphs.
            Think about writting a latex document.


        """
        # don't override caller's heading info, as we will be jumping outside
        cur_heading = cur_heading or {}

        for child in cur_tag.contents:
            if child.name is None:
                # this is a pure text
                child_text = re.sub(r'\n', ' ', child)
                # .copy(): performance issues?
                text_chunks.append((cur_heading.copy(), child_text))
            elif child.name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
                child_level = int(child.name[1])
                child_heading_name = get_tag_text(child)

                for lower_levels in range(child_level + 1, 7):
                    if lower_levels in cur_heading:
                        del cur_heading[lower_levels]
                # print(child, child_heading_name)
                cur_heading[child_level] = (child_heading_name, 'section_' + child.name)
            elif child.name in NON_DISPLAY_TAGS:
                pass
            elif child.name in LINEBREAK_ELEMENTS:
                text_chunks.append((cur_heading.copy(), '\n'))
            elif child.name in INLINE_TAGS:
                find_paragraphs(child, cur_heading)
            else:
                text_chunks.append((cur_heading.copy(), '\n'))
                find_paragraphs(child, cur_heading)

    if isinstance(tag_or_soup, Tag):
        find_paragraphs(tag_or_soup)
    else:
        for tag in tag_or_soup:
            find_paragraphs(tag)

    # Up to now, we have recursively extracted all strings.
    # Now we must merge strings according to the rules defined above.
    paragraphs = []

    exclude_section_rules = exclude_section_rules or []

    def should_exclude_sec(sec_name):
        for rule in exclude_section_rules:
            if rule.match(sec_name):
                return True
        return False

    while len(text_chunks) > 0:
        strings = []
        current_heading, string = text_chunks.pop(0)
        strings.append(string)

        while len(text_chunks) > 0 and text_chunks[0][0] == current_heading:
            _, string = text_chunks.pop(0)
            strings.append(string)

        if any(should_exclude_sec(x[0]) for x in current_heading.values()):
            continue

        # Construct paragraphs hierarchy!
        cur_level = paragraphs
        for level in sorted(current_heading):
            heading_name, heading_level = current_heading[level]

            if len(cur_level) < 1 or not isinstance(cur_level[-1], dict) or \
                    cur_level[-1]['type'] != heading_level or cur_level[-1]['name'] != heading_name:
                cur_level.append({
                    'type': heading_level,
                    'name': heading_name,
                    'content': [],
                })

            cur_level = cur_level[-1]['content']

        for paragraph in normalize_text(''.join(strings)).split('\n'):
            paragraph = paragraph.strip()
            if len(paragraph) > 0:
                cur_level.append(paragraph)

    return paragraphs
