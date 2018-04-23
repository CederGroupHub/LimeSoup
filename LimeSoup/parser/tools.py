"""
tools has some general functions that help during the parser process.
"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Mar 12 2018"


def convert_to_text(text_input):
    # import unicodedata
    text = text_input.rstrip()
    # text =  unicodedata.normalize('NFKD', text_input).encode('ascii','ignore')
    text = ' '.join(str(text).split())
    # input()
    # input()
    return text


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def n_paragraphs_sections(data):
    pd = flatten_json(data)
    paragraphs = list()
    headings = list()
    n_keywords = 0
    for item in pd:
        content = item.split('_')[-1]
        initial = item.split('_')[0]
        if content == 'name' or initial == 'Title':
            headings.append(convert_to_text(pd[item]))
        elif initial == 'Keywords':
            n_keywords += 1
        elif content.replace('.', '', 1).isdigit():
            paragraphs.append(pd[item])
    return {
        'headings': headings,
        'paragraphs': paragraphs,
        'keywords': n_keywords
    }
