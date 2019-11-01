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

with open('data/Elsevier/101016jssi201802031.xml', 'r', encoding = 'utf-8') as f:
    html_str = f.read()

data = ElsevierSoup.parse(html_str)

with open('Elsevier_Parsed/new/101016jssi201802031.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)