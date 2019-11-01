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
with open('data/Elsevier/101016jssi201802031.xml', 'r', encoding = 'utf-8') as f:
=======
with open('data/101021acslangmuir7b03411.xml', 'r', encoding = 'utf-8') as f:
>>>>>>> a023f7557a8444a0ad2f4adc864eaf13145ef169
    html_str = f.read()

data = ACSSoup.parse(html_str)

<<<<<<< HEAD
with open('Elsevier_Parsed/new/101016jssi201802031.json', 'w', encoding = 'utf-8') as f:
=======
with open('file_test.json', 'w', encoding = 'utf-8') as f:
>>>>>>> a023f7557a8444a0ad2f4adc864eaf13145ef169
    json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)