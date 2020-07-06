from LimeSoup import (
    ACSSoup, 
    APSSoup, 
    ECSSoup, 
    ElsevierSoup, 
    IOPSoup, 
    NatureSoup, 
    RSCSoup, 
    SpringerSoup, 
    WileySoup,
    AIPSoup
)
import json

with open('data/Elsevier/101016jcarbon201111044.xml', 'r', encoding = 'utf-8') as f:
    html_str = f.read()

data = ElsevierSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)