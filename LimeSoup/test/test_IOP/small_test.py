from LimeSoup.IOPSoup import IOPSoup1
from LimeSoup.IOPSoup2 import IOPSoup2

import json
from bs4 import BeautifulSoup

from bson import json_util
if __name__ == '__main__':
    filename = "sms_25_12_125015.xml"
    with open(filename, "r", encoding="utf-8") as f:
        paper = f.read()

    if IOPSoup1.parse(paper)['DOI']:

    	parsed_paper = IOPSoup.parse(paper)
    else:
    	parsed_paper=IOPSoup2.parse(paper)
    print(parsed_paper )
    with open('paper_info.json', 'w') as fw:
        json.dump([parsed_paper], fw, indent=2, default=json_util.default)