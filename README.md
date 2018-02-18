# parser_paper

ParserPaper is a class to parse html, xml, papers from different publisher into
simples text, it can be used to feed a database.

Use:

    from parser_paper import ParserPaper
    
    parse = ParserPaper(<raw_html>, <debugging>)

parameters:

    <raw_html>: paper in html or xml format
    
    <debugging>: parameter that helps during debugging, value True or False

Example:

    from parser_paper import ParserPaper
    
    parse = ParserPaper(raw_html, debugging=True)

You can run the example in the main.py
