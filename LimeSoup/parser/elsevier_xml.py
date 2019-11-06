import os
import re
import warnings

from lxml import etree
from lxml.etree import XMLSyntaxError

__author__ = 'Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'haoyan.huo@lbl.gov'


# Helper functions
def extract_text_any(_node, handler):
    # Extract node text in rules:
    # A := (B*)
    result = []
    for child in _node.children:
        result.append(handler(child))
    return ''.join(result)


def extract_text_or(_node, handlers):
    # Extract node text in rules:
    # A := (B|C|D|E)
    last_exception = None
    for h in handlers:
        try:
            return h(_node)
        except NameError as e:
            last_exception = e

    raise NameError('Failed to match node (%r, %r, %r) with all rules specified: %r, last exception was:\n%s' %
                    (_node.prefix, _node.name, str(_node)[:50], handlers, str(last_exception)))


def find_non_empty_children(_node):
    children = []
    for child in _node.children:
        if child.name is not None or child.string.strip() != '':
            children.append(child)

    return children


def assert_node_type(node, name):
    if ':' in name:
        prefix, name = name.split(':')

        # handle wildcards
        if prefix == '*':
            prefix = node.prefix

        if (node.prefix, node.name) != (prefix, name):
            raise NameError('Expecting %s but got %r:%r' %
                            (name, node.prefix, node.name))
    else:
        if node.name != name:
            raise NameError('Expecting %s but got %r' %
                            (name, node.name))


def node_named(node, name):
    if ':' in name:
        prefix, name = name.split(':')
        return (node.prefix, node.name) == (prefix, name)
    else:
        return node.name == name


def remove_consecutive_whitespaces(string, keep_newline=False):
    def sub(m):
        if keep_newline and '\n' in m.group(0):
            return '\n'
        else:
            return ' '

    st= re.sub(r'[ \t\n]+', sub, string)
    reg = re.compile('\[\d+\]')
    st = reg.sub('', st)
    st = st.replace(' .', '.').replace(' \xa0and\xa0.', '.').replace('\xa0', '').replace(' , , , , ', '').replace(' , , , ', '').replace(' , , ', '').replace(' ,', ',').replace('and,', ',').replace(',.', '.').replace(' ,', ',').replace('[]', '').replace(' .', '.')
    return st


# Elsevier XML format is defined here:
# Book "The Elsevier DTD 5 Family of XML DTDs"
# https://www.elsevier.com/__data/assets/pdf_file/0003/58872/ja5_tagbytag5_v1.9.5.pdf
# https://www.elsevier.com/__data/assets/text_file/0006/275667/ja5_common150_ent.txt
# This file defines functions that are capable of extracting text according to
# the rules defined above.

class XMLSyntaxWarning(Warning):
    pass


def resolve_elsevier_entities(xml_string):
    """
    Elsevier defined a set of entities that can be found in the corresponding
    ent (entity) files. However, XML files do not contain definition of such
    entities. Thus, we need to load the entities and patch the XML files, so
    that these entities are converted into unicode chars.
    See also "The Elsevier DTD 5 Family of XML DTDs" pp. 12

    :param xml_string:
    :return:
    """
    if not hasattr(resolve_elsevier_entities, 'dtd_strings'):
        invocation = """<!DOCTYPE xml [
        <!ENTITY % common.ent
            PUBLIC "-//ES//ELEMENTS common element pool version 1.4.0//EN//XML"
            "{file_dir}/dtd/ja5_art540/cep140/common140.ent">
        %common.ent;]>\n"""

        file_path = os.path.dirname(os.path.realpath(__file__))
        # lxml hates backslashes
        file_path = file_path.replace('\\', '/')

        setattr(resolve_elsevier_entities, 'dtd_invocation', invocation.format(file_dir=file_path))

    try:
        parser = etree.XMLParser(load_dtd=True)
        xml_tree = etree.fromstring(
            getattr(resolve_elsevier_entities, 'dtd_invocation') + xml_string,
            parser=parser,
        )
    except XMLSyntaxError:
        if not hasattr(resolve_elsevier_entities, 'recover'):
            warnings.warn('Enabling "recover" in XML parser. '
                          'There might be a problem with XML source.', XMLSyntaxWarning)
            setattr(resolve_elsevier_entities, 'recover', True)
        parser = etree.XMLParser(load_dtd=True, recover=True)
        xml_tree = etree.fromstring(
            getattr(resolve_elsevier_entities, 'dtd_invocation') + xml_string,
            parser=parser,
        )

    return etree.tostring(xml_tree)


def process_richstring_data(_node):
    # <!ENTITY % richstring.data  "#PCDATA|ce:glyph|%text-effect;|ce:inline-figure
    #                              %local.richstring.data;" >
    # <!ENTITY % text-effect      "%font-change;|ce:sup|ce:inf|ce:underline|
    #                              ce:cross-out|ce:hsp|ce:vsp" >
    # <!ENTITY % font-change      "ce:bold|ce:italic|ce:monospace|ce:sans-serif|
    #                              ce:small-caps" >
    if _node.name is None:
        # PC data
        # All consecutive whitespaces should be treated as only one
        return remove_consecutive_whitespaces(_node.string)
    elif node_named(_node, 'ce:glyph'):
        # TODO: don't know how to process glyph, produce a whitespace
        return ' '
    elif node_named(_node, 'ce:inline-figure'):
        return ' '
    elif _node.prefix == 'ce' and _node.name in {
        'bold', 'italic', 'monospace', 'sans-serif', 'small-caps',
        'underline', 'cross-out'
    }:
        # This is an enhancement: we strip the text for them because they usually
        # appear as inline elements.
        return remove_consecutive_whitespaces(
            extract_text_any(_node, process_richstring_data),
            keep_newline=False).strip()
    elif _node.prefix == 'ce' and _node.name in {'sup', 'inf'}:
        # Same as above.
        return remove_consecutive_whitespaces(
            extract_text_any(_node, process_richstring_data),
            keep_newline=False).strip()
    elif _node.prefix == 'ce' and _node.name in {'hsp', 'vsp'}:
        return ' '
    else:
        raise NameError('Unknown tag <%s> in richstring processing' % str(_node.name))


def process_text_data(_node):
    # <!ENTITY % text.data        "%richstring.data;|mml:math; %local.text.data;" >
    return extract_text_or(_node, (
        process_richstring_data,
        extract_mml_math,
    ))


def process_inter_ref(_node):
    # <!ELEMENT   ce:inter-ref        ( %text.data; )* >
    assert_node_type(_node, 'ce:inter-ref')
    return extract_text_any(_node, process_text_data)


def process_textlink_data(_node):
    # <!ENTITY % textlink.data    "%text.data;|ce:inter-ref" >
    return extract_text_or(_node, (
        process_text_data,
        process_inter_ref,
    ))


def process_cross_ref(_node):
    # <!ENTITY % cross-ref        "ce:cross-ref|ce:intra-ref" >
    if node_named(_node, 'ce:intra-ref'):
        return ''
    elif node_named(_node, 'ce:cross-ref'):
        # We take only cross-ref's that are not bib refs. This includes,
        # for example, "Fig. ?", "Table ?"...
        if not re.match(r'bib.*', _node.attrs['refid'], re.IGNORECASE):
            return extract_text_any(_node, process_text_data)
        else:
            return ''
    else:
        raise NameError('Unknown tag name (%r, %r) in processing cross-ref' %
                        (_node.prefix, _node.name))


def process_cross_refs(_node):
    # <!ENTITY % cross-refs       "ce:cross-refs|ce:intra-refs" >
    # Same as process_cross_ref()
    if node_named(_node, 'ce:intra-refs'):
        return ''
    elif node_named(_node, 'ce:cross-refs'):
        # We take only cross-ref's that are not bib refs. This includes,
        # for example, "Fig. ?", "Table ?"...
        if not re.match(r'bib.*', _node.attrs['refid'], re.IGNORECASE):
            return extract_text_any(_node, process_text_data)
        else:
            return ''
    else:
        raise NameError('Unknown tag name (%r, %r) in processing cross-refs' %
                        (_node.prefix, _node.name))


def process_cross_ref_s(_node):
    # <!ENTITY % cross-ref-s      "%cross-ref;|%cross-refs;" >
    return extract_text_or(_node, (
        process_cross_ref,
        process_cross_refs,
    ))


def process_inter_ref_s(_node):
    # <!ENTITY % inter-ref-s      "ce:inter-ref|ce:inter-refs" >
    if node_named(_node, 'ce:inter-ref'):
        return process_inter_ref(_node)
    elif node_named(_node, 'ce:inter-refs'):
        # <!ELEMENT   ce:inter-refs
        #             ( ce:inter-refs-text?, ce:inter-ref-end+, ce:inter-refs-link )>
        children = find_non_empty_children(_node)

        if children and node_named(children[0], 'ce:inter-refs-text'):
            return extract_text_any(children[0], process_text_data)

        # Not checking the correctness of ce:inter-refs
        return ''
    else:
        raise NameError('Unknown tag name (%r, %r) in processing cross-refs' %
                        (_node.prefix, _node.name))


def process_textref_data(_node):
    # <!ENTITY % textref.data
    #            "%text.data;|%cross-ref-s;|%inter-ref-s; %local.textref.data;" >
    return extract_text_or(_node, (
        process_text_data,
        process_cross_ref_s,
        process_inter_ref_s
    ))


def process_lists(_node):
    # <!ENTITY % lists            "ce:def-list|ce:list" >
    # This is a hack: insert a newline before list, so that it won't break the paragraph
    # If there is no paragraph, this does not hurt, as the paragraph will finally strip
    # the string.
    return '\n' + extract_text_or(_node, (
        extract_ce_def_list,
        extract_ce_list,
    ))


def process_nondisplay_data(_node):
    # <!ENTITY % nondisplay.data  "%textref.data;|ce:footnote|
    #                             ce:anchor %local.nondisplay.data;">
    try:
        return process_textref_data(_node)
    except NameError:
        pass

    if node_named(_node, 'ce:footnote'):
        return extract_ce_footnote(_node)

    # TODO: some papers have ce:float-anchor in a nondisplay.data.
    # We make an exception here.
    if node_named(_node, 'ce:float-anchor'):
        return extract_ce_float_anchor(_node)

    if node_named(_node, 'ce:anchor'):
        return extract_text_any(_node, process_richstring_data)

    raise NameError('Unknown tag name (%r, %r) in processing nondisplay.data' %
                    (_node.prefix, _node.name))


def process_text_objects(_node):
    # <!ENTITY % text-objects     "ce:anchor|ce:grant-sponsor|ce:grant-number" >
    return extract_text_or(_node, (
        extract_ce_anchor,
        extract_ce_grant_sponsor,
        extract_ce_grant_number,
    ))


def process_textfn_data(_node):
    # <!ENTITY % textfn.data
    #          "%text.data;|ce:footnote|%cross-ref-s; %local.textfn.data;" >
    return extract_text_or(_node, (
        process_text_data,
        extract_ce_footnote,
        process_cross_ref_s
    ))


def process_spar_data(_node):
    # <!ENTITY % spar.data        "%textref.data;|%display;|%lists;|ce:footnote|%text-objects;
    #                              %local.spar.data;" >
    return extract_text_or(_node, (
        process_textref_data,
        process_display,
        process_lists,
        extract_ce_footnote,
        process_text_objects,
    ))


def process_display(_node):
    # <!ENTITY % display          "ce:display|ce:displayed-quote|ce:enunciation" >
    return extract_text_or(_node, (
        extract_ce_display,
        extract_ce_displayed_quote,
        extract_ce_enunciation,
    ))


def process_par_data(_node):
    # <!ENTITY % par.data         "%textref.data;|ce:float-anchor|%display;|%lists;|ce:footnote|%text-objects;
    #                              %local.par.data;" >
    return extract_text_or(_node, (
        process_textref_data,
        extract_ce_float_anchor,
        process_display,
        process_lists,
        extract_ce_footnote,
        process_text_objects,
    ))


def extract_mml_math(node):
    try:
        assert_node_type(node, 'mml:math')
    except NameError:
        # To catch the error for some specific articles,
        # such as 10.1016/S1388-2481(01)00138-2
        assert_node_type(node, '*:math')

    # TODO: better rendering.
    return re.sub(r'\s', '', ''.join(node.findAll(text=True)))


def extract_ce_footnote(node):
    assert_node_type(node, 'ce:footnote')
    return ''


def extract_ce_text(node):
    """
    This is the parser for ce:text element defined in Elsevier XML CEP 1.4.0.
    <!ELEMENT   ce:text             ( %textlink.data; )* >

    :param node: A beautiful soup Tag node.
    :return: The text embedded in this node.
    """
    assert_node_type(node, 'ce:text')
    return extract_text_any(node, process_textlink_data)


def extract_ce_section_title(node):
    """
    <!ELEMENT ce:section-title  ( %nondisplay.data; )*>

    :param node:
    :return:
    """
    assert_node_type(node, 'ce:section-title')
    # HACK: see function for ce:title
    return remove_consecutive_whitespaces(
        extract_text_any(node, process_nondisplay_data),
        keep_newline=False
    ).strip()


def extract_ce_def_term(node):
    # <!ELEMENT   ce:def-term         ( %text.data; )* >
    assert_node_type(node, 'ce:def-term')
    return extract_text_any(node, process_text_data)


def extract_ce_def_description(node):
    # <!ELEMENT   ce:def-description  ( ce:para+ )>
    assert_node_type(node, 'ce:def-description')

    children = find_non_empty_children(node)
    if len(children) < 1:
        raise ValueError('Expecting 1+ ce:para for ce:def-description')

    paragraphs = [extract_ce_para(x) for x in children]
    return '\n'.join(paragraphs)


def extract_ce_def_list(node):
    assert_node_type(node, 'ce:def-list')
    # <!ELEMENT   ce:def-list         ( ce:label?, ce:section-title?,
    #                                 ( ce:def-term, ce:def-description? )+ )>

    children = find_non_empty_children(node)
    if len(children) and node_named(children[0], 'ce:label'):
        children.pop(0)

    if len(children) and node_named(children[0], 'ce:section-title'):
        children.pop(0)

    term_definitions = []
    while True:
        term = extract_ce_def_term(children.pop(0))

        description = None
        if len(children) > 0:
            try:
                description = extract_ce_def_description(children[0])
                children.pop(0)
            except NameError:
                pass

        if description is not None:
            term_definitions.append('%s : %s' % (term, description))
        else:
            term_definitions.append('%s' % (term,))

        if len(children) == 0:
            break

    return '\n'.join(term_definitions)


def extract_ce_list_item(node):
    # <!ELEMENT   ce:list-item        ( ce:label?, ce:para+ )>
    assert_node_type(node, 'ce:list-item')
    children = find_non_empty_children(node)
    if len(children) and node_named(children[0], 'ce:label'):
        children.pop(0)

    if len(children) < 1:
        raise ValueError('Expecting 1+ ce:para in ce:list-item')

    paragraphs = [extract_ce_para(x) for x in children]
    return '\n'.join(paragraphs)


def extract_ce_list(node):
    # <!ELEMENT   ce:list             ( ce:label?, ce:section-title?, ce:list-item+ )>
    assert_node_type(node, 'ce:list')

    children = find_non_empty_children(node)
    if len(children) and node_named(children[0], 'ce:label'):
        children.pop(0)

    if len(children) and node_named(children[0], 'ce:section-title'):
        children.pop(0)

    if len(children) < 1:
        raise ValueError('Expecting 1+ ce:list-item in ce:list')

    paragraphs = [extract_ce_list_item(x) for x in children]
    return '\n'.join(paragraphs)


def extract_ce_float_anchor(node):
    assert_node_type(node, 'ce:float-anchor')
    return ''


def extract_ce_anchor(node):
    # <!ELEMENT   ce:anchor           ( %richstring.data; )* >
    assert_node_type(node, 'ce:anchor')
    return extract_text_any(node, process_richstring_data)


def extract_ce_grant_sponsor(node):
    # <!ELEMENT   ce:grant-sponsor    ( %text.data; )* >
    assert_node_type(node, 'ce:grant-sponsor')
    return extract_text_any(node, process_text_data)


def extract_ce_grant_number(node):
    # <!ELEMENT   ce:grant-number     ( %text.data; )* >
    assert_node_type(node, 'ce:grant-number')
    return extract_text_any(node, process_text_data)


def extract_ce_figure(node):
    assert_node_type(node, 'ce:figure')
    return ''


def extract_ce_table(node):
    assert_node_type(node, 'ce:table')
    return ''


def extract_ce_textbox(node):
    assert_node_type(node, 'ce:textbox')
    return ''


def extract_ce_e_component(node):
    assert_node_type(node, 'ce:e-component')
    return ''


def extract_ce_chem(node):
    # <!ELEMENT   ce:chem             ( %textfn.data; )* >
    assert_node_type(node, 'ce:chem')
    return extract_text_any(node, process_textfn_data)


def extract_ce_link(node):
    # <!ELEMENT   ce:link             EMPTY>
    assert_node_type(node, 'ce:link')
    return ''


def extract_ce_formula(node):
    # <!ELEMENT   ce:formula
    #             ( ce:label?, ( mml:math | ce:chem | ce:link | ce:formula+ ))>
    try:
        assert_node_type(node, 'ce:formula')
    except NameError:
        # To catch the error for some specific articles,
        # such as 10.1016/S1388-2481(01)00138-2
        assert_node_type(node, '*:formula')

    children = find_non_empty_children(node)

    if len(children) and node_named(children[0], 'ce:label'):
        children.pop(0)

    if len(children) < 1:
        raise ValueError('Expecting 1+ visible element for ce:formula')

    if len(children) > 1 or node_named(children[0], 'ce:formula') or \
            node_named(children[0], '*:formula'):
        formulas = [extract_ce_formula(x) for x in children]
        return ' '.join(formulas)

    # Another hack: we put an additional whitespace to separate formula and text
    return ' %s ' % extract_text_or(children[0], (
        extract_mml_math,
        extract_ce_chem,
        extract_ce_link,
        extract_ce_formula,
    ))


def extract_ce_display(node):
    # <!ELEMENT   ce:display
    #   ( ce:figure | ce:table | ce:textbox | ce:e-component | ce:formula )>
    try:
        assert_node_type(node, 'ce:display')
    except NameError:
        # To catch the error for some specific articles,
        # such as 10.1016/S1388-2481(01)00138-2
        assert_node_type(node, '*:display')

    children = find_non_empty_children(node)

    if len(children) != 1:
        raise ValueError('ce:display must only have one child, got %d', len(children))
    return extract_text_or(children[0], (
        extract_ce_figure,
        extract_ce_table,
        extract_ce_textbox,
        extract_ce_e_component,
        extract_ce_formula,
    ))


def extract_ce_simple_para(node):
    # <!ELEMENT   ce:simple-para      ( %spar.data; )* >
    text = extract_text_any(node, process_spar_data)
    return remove_consecutive_whitespaces(text, keep_newline=True).strip()


def extract_ce_displayed_quote(node):
    # <!ELEMENT   ce:displayed-quote  ( ce:simple-para+, ce:source? )>
    assert_node_type(node, 'ce:displayed-quote')

    children = find_non_empty_children(node)
    paragraphs = []
    while len(children) and node_named(children[0], 'ce:simple-para'):
        simple_para = extract_ce_simple_para(children.pop(0))
        paragraphs.append(simple_para)

    if len(children) > 1 or \
            (len(children) == 1 and node_named(children[0], 'ce:source')):
        remaining_nodes = [(x.prefix, x.name) for x in children]
        assert ValueError('Expecting ce:simple-para+, ce:source?, got tailing %r' % remaining_nodes)

    return '\n'.join(paragraphs)


def extract_ce_enunciation(node):
    # <!ELEMENT   ce:enunciation      ( ce:label, ce:section-title?, ce:para+ )>
    # We ignore label and section title
    assert_node_type(node, 'ce:enunciation')

    children = find_non_empty_children(node)
    if len(children) and node_named(children[0], 'ce:label'):
        children.pop(0)

    if len(children) and node_named(children[0], 'ce:section-title'):
        children.pop(0)

    if len(children) < 1:
        raise ValueError('Expecting at least ce:para for a ce:enunciation')

    paragraphs = [extract_ce_para(x) for x in children]
    return '\n'.join(paragraphs)


def extract_ce_para(node):
    # <!ELEMENT   ce:para             ( %par.data; )* >
    assert_node_type(node, 'ce:para')
    return remove_consecutive_whitespaces(extract_text_any(node, process_par_data), keep_newline=True).strip()


def extract_ce_section(node):
    assert_node_type(node, 'ce:section')

    # <!ELEMENT ce:section ( ( ( ce:section-title | ( ce:label, ce:section-title? ) ),
    #                      %parsec; ) | ce:section+ )>

    children = find_non_empty_children(node)

    if len(children) < 1:
        raise ValueError('ce:section should not be empty')

    def get_parsec(children_array):
        # <!ENTITY % parsec           "( ce:para | ce:section )+" >
        if len(children_array) < 1:
            raise ValueError('Expecting more than 0 parsec')

        for _child in children_array:
            if node_named(_child, 'ce:para'):
                for i in extract_ce_para(_child).split('\n'):
                    yield i
            elif node_named(_child, 'ce:section'):
                yield extract_ce_section(_child)
            else:
                raise NameError('Unknown tag name (%r, %r) in processing parsec' %
                                (_child.prefix, _child.name))

    section_content = {
        'type': 'ce_section',
        'name': '',
        'content': []
    }
    if node_named(children[0], 'ce:section-title'):
        title = extract_ce_section_title(children.pop(0))
        section_content['name'] = title

        section_content['content'].extend(get_parsec(children))
    elif node_named(children[0], 'ce:label'):
        # remove label
        children.pop(0)

        if node_named(children[0], 'ce:section-title'):
            title = extract_ce_section_title(children.pop(0))
            section_content['name'] = title

        section_content['content'].extend(get_parsec(children))
    else:
        for child in children:
            if not node_named(child, 'ce:section'):
                raise NameError('Expecting ce:section, but got (%r, %r)' %
                                (child.prefix, child.name))
            content = extract_ce_section(child)
            section_content['content'].append(content)

    return section_content


def extract_ce_abstract(node):
    assert_node_type(node, 'ce:abstract')

    # <!ELEMENT   ce:abstract
    #             ( ce:section-title?, ce:abstract-sec+, ce:figure? )>

    children = find_non_empty_children(node)

    section_content = {
        'type': 'ce_section',
        'name': '',
        'content': []
    }

    if len(children) > 0 and node_named(children[0], 'ce:section-title'):
        title = extract_ce_section_title(children.pop(0))
        section_content['name'] = title

    def get_abstract_sec(_node):
        # <!ELEMENT   ce:abstract-sec     ( ce:section-title?, ce:simple-para+ )>
        assert_node_type(_node, 'ce:abstract-sec')
        abstract_sec = {
            'type': 'ce_section',
            'name': '',
            'content': []
        }

        _children = find_non_empty_children(_node)

        if len(_children) > 0 and node_named(_children[0], 'ce:section-title'):
            _title = extract_ce_section_title(_children.pop(0))
            abstract_sec['name'] = _title

        while len(_children) > 0 and node_named(_children[0], 'ce:simple-para'):
            abstract_sec['content'].extend(extract_ce_simple_para(_children.pop(0)).split('\n'))

        if abstract_sec['name']:
            return abstract_sec,
        else:
            return abstract_sec['content']

    while len(children) and node_named(children[0], 'ce:abstract-sec'):
        section_content['content'].extend(get_abstract_sec(children.pop(0)))

    return section_content


def extract_ce_title(node):
    # <!ELEMENT   ce:title            ( %textfn.data; )* >
    # This is a hack: remove newlines because titles should not contain them.
    return remove_consecutive_whitespaces(
        extract_text_any(node, process_textfn_data),
        keep_newline=False
    ).strip()
