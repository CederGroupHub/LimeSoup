'''
ParserPaper is a class to parse html, xml, papers from different publisher into
simples text, it can be used to feed a database.

Use:
    from parser_paper import ParserECS
    parse = ParserECS(<raw_html>, <debugging>)

parameters:
    <raw_html>: paper in html or xml format
    <debugging>: parameter that helps during debugging, value True or False

Example:
    from parser_paper import ParserECS
    parse = ParserECS(raw_html, debugging=True)
'''

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "Feb 18 2018"

from implemented_parsers import ParserECS, ParserRSC
      
if __name__ == '__main__':
    print("read example_RSC_paper.html")
    with open('example_RSC_paper.html', 'r') as fd:
        raw_html = fd.read()
    parse = ParserRSC(raw_html, debugging=True)
    with open('output_RSC_parser_paper.txt', 'w') as fd:
        fd.write('Title: {}\n'.format(parse.title))
        fd.write('Keywords: {}\n'.format(parse.keywords))
        fd.write('Sections: \n')
        for item in parse.data_sections:
            fd.write('    Section type: {}\n'.format(item['type']))
            fd.write('    Section name: {}\n'.format(item['name']))
            fd.write('    Content: \n')
            for item_content in item['content']:
                fd.write('        {}\n'.format(item_content))
        fd.write('----------------------------')         
    del parse
    print("end RSC paper!!!")
    print('-------')
    print("read example_ECS_paper.html")
    with open('example_ECS_paper.html', 'r') as fd:
        raw_html = fd.read()
    print("process file...")
    parse = ParserECS(raw_html, debugging=True)
    print('output file = output_parser_paper.txt')
    with open('output_ECS_parser_paper.txt', 'w') as fd:
        fd.write('Title: {}\n'.format(parse.title))
        fd.write('Keywords: {}\n'.format(parse.keywords))
        fd.write('Sections: \n')
        for item in parse.data_sections:
            fd.write('    Section type: {}\n'.format(item['type']))
            fd.write('    Section name: {}\n'.format(item['name']))
            fd.write('    Content: \n')
            for item_content in item['content']:
                fd.write('        {}\n'.format(item_content))
        fd.write('----------------------------')         
    del parse
    print("end!!!")