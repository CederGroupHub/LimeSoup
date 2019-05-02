import sys, os
sys.path.append("..")
sys.path.append(".")

from LimeSoup.SpringerSoup import SpringerSoup
import json

html_files = ['101007bf02663182.html',
'101007s00339-013-8138-9.html',
'101007s10853-011-5258-5.html',
'101007s10853-015-9171-1.html',
'101007s11671-009-9393-8.html',
'101007s40964-017-0023-1.html',
'101140epjbe2017-80152-2.html',
'101007bf01142064.html',
'10.1007_s10562-010-0490-1.html'
]

path = 'test/springer_papers/'
for filename in html_files:
    html_file = path+filename
    with open(html_file, 'r', encoding = 'utf-8') as f:
        html_str = f.read()
    print('\n')
    print(filename)
    data = SpringerSoup.parse(html_str)
    with open(f'test/springer_papers/parsed_papers/{filename[:-5]}.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)