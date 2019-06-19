# LimeSoup

LimeSoup is a package to parse HTML or XML papers from different publishers. It can be
used to feed a database.

[![Build Status](https://semaphoreci.com/api/v1/projects/686509c1-2128-44fd-9532-1a32090bd980/2687086/badge.svg)](https://semaphoreci.com/cedergrouphub/limesoup)

# Usage

Full Usage:

```
with open(article, 'r', encoding = 'utf-8') as f:
    html_str = f.read()

***Choose correct publisher
from LimeSoup.ECSSoup import ECSSoup
data = ECSSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
```    

Currently, we have implemented the following parsers:

- ECS: The Electrochemical Society
- RSC: The Royal Society of Chemistry
- Elsevier
- Nature Publishing Group
- Springer
- Wiley
- ACS: American Chemical Society
- APS: American Physical Society
- IOP Publishing

# Development documentation

Please refer to the [wiki pages](https://github.com/CederGroupHub/LimeSoup/wiki).

# Change logs

Please see [change logs](CHANGES.md).

