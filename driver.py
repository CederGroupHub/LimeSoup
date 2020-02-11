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
'data\springer\101007s10853-006-0223-4.html'
with open('data/springer/101007s10853-006-0223-4.html', 'r', encoding = 'utf-8') as f:

    html_str = f.read()

data = SpringerSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)