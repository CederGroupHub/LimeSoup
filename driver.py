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

<<<<<<< HEAD
with open('data/springer/101007s10853-006-0223-4.html', 'r', encoding = 'utf-8') as f:
=======
with open('data/ECS/10114911543949.html', 'r', encoding = 'utf-8') as f:
>>>>>>> 04551d98746789ec2a7e10c224526924143bc168
    html_str = f.read()

data = SpringerSoup.parse(html_str)

with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)