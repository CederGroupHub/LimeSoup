# LimeSoup

LimeSoup is a package to parse HTML or XML papers from different publishers. It can be
used to feed a database.
The class ECSSoup and RCSSoup are implementations for the ECS and RSC publishers respectively.

Use for ECS Publisher:

    from LimeSoup.ECSSoup import ECSSoup
    data = ECSSoup.parse(html_str)

Use for RCS Publisher:

    from LimeSoup.RCSSoup import RSCSoup
    data = RCSSoup.parse(html_str)

Use for Nature Publisher:

    from LimeSoup.NatureSoup import NatureSoup
    data = NatureSoup.parse(html_str)


parameters:

    :param html_str: raw HTML strings
    :return: Parse JSON object


Full Usage:

    with open(article, 'r', encoding = 'utf-8') as f:
        html_str = f.read()

    ***Choose correct publisher and paste code from above to parse***

    with open('file_test.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
