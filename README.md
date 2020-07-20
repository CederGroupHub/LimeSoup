# LimeSoup

LimeSoup is a package to parse HTML or XML papers from different publishers. It can be
used to feed a database.

[![Build Status](https://semaphoreci.com/api/v1/projects/686509c1-2128-44fd-9532-1a32090bd980/2687086/badge.svg)](https://semaphoreci.com/cedergrouphub/limesoup)

# Usage

Full Usage:

```
from LimeSoup import (
    ACSSoup, 
    AIPSoup,
    APSSoup, 
    ECSSoup, 
    ElsevierSoup, 
    IOPSoup, 
    NatureSoup, 
    RSCSoup, 
    SpringerSoup, 
    WileySoup,
)


with open(article, 'r', encoding = 'utf-8') as f:
    html_str = f.read()

***Choose correct publisher
data = ECSSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
```    

Currently, we have implemented the following parsers:

- [ECS: The Electrochemical Society](http://ecsdl.org)
- [RSC: The Royal Society of Chemistry](https://www.rsc.org)
- [Elsevier](https://www.elsevier.com/catalog)
- [Nature Publishing Group](https://www.nature.com)
- [Springer](https://www.springernature.com/gp/products/journals)
- [Wiley](https://onlinelibrary.wiley.com)
- [ACS: American Chemical Society](https://pubs.acs.org)
- [APS: American Physical Society](https://journals.aps.org)
- [IOP Publishing](https://ioppublishing.org/publications/our-journals/)
- [AIP: American Institute of Physics](https://aip.scitation.org/)

# Development documentation

Please refer to the [wiki pages](https://github.com/CederGroupHub/LimeSoup/wiki).

# Change logs

Please see [change logs](CHANGES.md).

# Credits

LimeSoup was contributed to by these genius people:

- Tiago Botari
- Ziqin Rong
- Vahe Tshitoyan
- Nicolas Mingione
- Jason Madeano
- Haoyan Huo
- Tanjin He
- Zach Jensen
- Alex van Grootel
- Edward Kim
- Haihao Liu
- Zheren Wang


If you are planning to use LimeSoup in your work, please consider citing the following paper:

 * Kononova et. al "Text-mined dataset of inorganic materials synthesis recipes", Scientific Data 6 (1), 1-11 (2019) [10.1038/s41597-019-0224-1](https://www.nature.com/articles/s41597-019-0224-1)
