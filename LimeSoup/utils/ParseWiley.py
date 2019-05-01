import sys
sys.path.append('.')
from LimeSoup.WileySoup import WileySoup
import json

html_files = ['LimeSoup/test/test_wiley/10.1002-anie.201508702.html'

]

for filename in html_files:
    with open(filename, 'r', encoding = 'utf-8') as f:
        html_str = f.readlines()

    data = WileySoup.parse(html_str)
    print(filename)
    with open('out.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)