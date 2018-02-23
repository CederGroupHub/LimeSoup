# LimeSoup

ParserPaper is an abstract class that can be used to create a class that helps
in the process of parse HTML or XML papers from different publishers. It can be
used to feed a database.
This script presents an example of a use of ParserECS and ParserRSC, 
two different implementations for the ECS and RSC publishers respectively 
using the PaerserPaper. 

Use:

    from parser_paper import ParserECS
    parse = ParserECS(<raw_html>, <debugging>)

parameters:

    <raw_html>: paper in html or xml format
    <debugging>: parameter that helps during debugging, value True or False

Example:

    from parser_paper import ParserECS
    parse = ParserECS(raw_html, debugging=True)

