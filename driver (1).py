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

<<<<<<< HEAD
with open('data/101016jelectacta201612018.xml', 'r', encoding = 'utf-8') as f:
    html_str = f.read()

data = ElsevierSoup.parse(html_str)

with open('Parsed/101016jelectacta201612018.json', 'w', encoding = 'utf-8') as f:
=======
'data\AIP\Berkeley\The-Journal-of-Chemical-Physics.10.1063-1.5094220.html'
with open('data\AIP\Berkeley\The-Journal-of-Chemical-Physics.10.1063-1.5094220.html', 'r', encoding = 'utf-8') as f:

    html_str = f.read()

data = AIPSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
>>>>>>> 8ab65d6d7c2d59c24337fa83148967362ad52f71
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)