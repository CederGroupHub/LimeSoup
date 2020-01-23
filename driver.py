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
)
import json

with open('data/springer/101007s11223-016-9732-9.html', 'r', encoding = 'utf-8') as f:
    html_str = f.read()

data = SpringerSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)