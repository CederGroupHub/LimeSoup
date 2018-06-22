# -*- coding: utf-8 -*-
# from LimeSoup.NatureSoup import NatureSoup
from pprint import pprint
import requests
import json
from NatureSoup import NatureCollect, NatureRemoveTrash, NatureRemoveTagsSmallSub
# from LimeSoup.NatureSoup import NatureSoup


# Links to test multiple parsers for inconsistencies in outut format
Nature_url = 'https://www.nature.com/articles/srep30829'
ECS_url = 'http://jes.ecsdl.org/content/161/10/D484.full?sid=f2018f6f-cfce-495e-a8a1-a057226eb336'
RCS_url = 'http://pubs.rsc.org/en/content/articlehtml/2017/ra/c6ra28478g'


# with open('TEST.html') as f:
#     data = f.read()


# This proxy is required when using a Shell workstation, change request (line 36)
http_proxy  = "proxy-ap.shell.com:8080"                         #if not at Shell
https_proxy = "proxy-ap.shell.com:8080"
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
            }



articles = ['https://www.nature.com/articles/srep30829',
            'https://www.nature.com/articles/lsa201414',
            'https://www.nature.com/articles/srep21496']

parsed = []
for article in articles:    # Quickly test using nature links
    data = requests.get(article, proxies=proxyDict).content.decode('ascii', 'ignore')

    tags_removed = NatureRemoveTagsSmallSub().parse(data)
    trash_removed = NatureRemoveTrash().parse(tags_removed)
    parsed.append(NatureCollect().parse(trash_removed))

# Export the test results as .json
with open('test.json', 'w') as f:
    json.dump(parsed, f, sort_keys=True, indent=4)
