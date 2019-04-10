from LimeSoup.SpringerSoup import SpringerSoup
import json

html_files = [#'101007bf02663182.html',
'101007s00339-013-8138-9.html',
'101007s10853-011-5258-5.html',
'101007s10853-015-9171-1.html',
'101007s11671-009-9393-8.html',
'101007s40964-017-0023-1.html',
'101140epjbe2017-80152-2.html']

for filename in html_files[2:3]:
    with open(filename, 'r', encoding = 'utf-8') as f:
        html_str = f.readlines()

    data = SpringerSoup.parse(html_str)
    print(filename)
    with open(f'output_files/{filename[:-5]}.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)