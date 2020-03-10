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

'data\Berkeley\Berkeley\The-Journal-of-Chemical-Physics.10.1063-1.5094220.html'
with open('data/Berkeley\Berkeley/The-Journal-of-Chemical-Physics.10.1063-1.5094220.html', 'r', encoding = 'utf-8') as f:
    html_str = f.read()

data = AIPSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)