# LimeSoup

LimeSoup is a package to parse HTML or XML papers from different publishers. It can be
used to feed a database.
The class ECSSoup and RCSSoup are implementations for the ECS and RSC publishers respectively. 

Use for ECS Publisher:

    from LimeSoup.ECSSoup import ECSSoup
    data = ECSSoup.parse(html_str)

Use for RCS Publisher:

    from LimeSoup.ECSSoup import RSCSoup
    data = RCSSoup.parse(html_str)

parameters:
    
    :param html_str: raw HTML strings
    :return: Parse JSON object
    


