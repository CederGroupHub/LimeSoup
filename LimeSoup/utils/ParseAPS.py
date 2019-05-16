import sys
sys.path.append('.')
from LimeSoup.APSSoup import APSSoup
import json

xml_files = ['LimeSoup/test/test_aps/101103PhysRevMaterials1043801.xml'

]

for filename in xml_files:
    with open(filename, 'r', encoding = 'utf-8') as f:
        xml_str = f.read()

    data = APSSoup.parse(xml_str)
    print(filename)
    with open('out.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)