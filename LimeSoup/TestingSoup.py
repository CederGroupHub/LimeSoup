# -*- coding: utf-8 -*-
# from LimeSoup.NatureSoup import NatureSoup
from pprint import pprint
import random, os, glob, re
import requests
import json
from bs4 import BeautifulSoup
# from NatureSoup import NatureCollect, NatureRemoveTrash, NatureRemoveTagsSmallSub, InvalidArticleException
from LimeSoup.NatureSoup import NatureSoup, InvalidArticleException

#### TEST PARSER USING URLs ####
# # Links to test multiple parsers for inconsistencies in outut format
# Nature_url = 'https://www.nature.com/articles/srep30829'
# ECS_url = 'http://jes.ecsdl.org/content/161/10/D484.full?sid=f2018f6f-cfce-495e-a8a1-a057226eb336'
# RCS_url = 'http://pubs.rsc.org/en/content/articlehtml/2017/ra/c6ra28478g'
#
# # This proxy is required when using a Shell workstation, change request (line 36)
# http_proxy  = "proxy-ap.shell.com:8080"                         #if not at Shell
# https_proxy = "proxy-ap.shell.com:8080"
# proxyDict = {
#               "http"  : http_proxy,
#               "https" : https_proxy,
#             }
#
#
#
# articles = ['https://www.nature.com/articles/srep30829',
#             'https://www.nature.com/articles/lsa201414',
#             'https://www.nature.com/articles/srep21496']
#
# parsed = []
# for article in articles:    # Quickly test using nature links
#     data = requests.get(article, proxies=proxyDict).content.decode('ascii', 'ignore')
#
#     tags_removed = NatureRemoveTagsSmallSub().parse(data)
#     trash_removed = NatureRemoveTrash().parse(tags_removed)
#     parsed.append(NatureCollect().parse(trash_removed))


#### TEST PARSER USING HTML FILES ####
# Select random article from ~65,000
directory = os.path.realpath('C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls')
html_files = glob.glob(os.path.join(directory, '*.html'))
articles = random.sample(html_files, 10)


# # Automatically find path of LimeSoup\TestingSoup.py
file_path = os.path.realpath(__file__)
directory = os.path.dirname(file_path)
test_file_directory = directory + "\\test\\nature_papers"

# Valid Articles
# articles = [test_file_directory +'\\10103835012032.html',
#             test_file_directory +'\\10103835050110.html',
#             test_file_directory + '\\101038416304a.html',
#             test_file_directory +'\\10103818335.html',
#             test_file_directory +'\\10103826206.html',
#             test_file_directory +'\\10103819734.html']

# # Invalid Articles (*properly dealt with in Article Type Screening)
# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038421478a.html', #news
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038418831a.html', #review
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038380585a0.html', #empty
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038384612a0.html', # ...
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038374671b0.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\10103817740.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038385009a0.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\10103835065225.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\10103835000303.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038531171a.html'] # Book review

# articles =['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038d41586-017-07497-x.html'] # List of links, unclassified?
# print(articles)
# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038ncomms10347.html'] # good ncomms
# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature21420.html'] # ***doesnt extract methods***

# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature05027.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature05904.html'] # no article body!!!

# directory = os.path.realpath('C:\\Users\\Jason\\Desktop\\Shell\\Synthesis Articles')
# articles = glob.glob(os.path.join(directory, '*Z.html'))


parsed = []
for article in articles:    # Quickly test using nature links
    # print(article)
    valid_article = True
    with open(article, 'r', encoding = 'utf-8') as f:
        data = f.read()

    try:
        print(article)
        parsed.append(NatureSoup.parse(data))

    except Exception as e:
        print(e)
        os.startfile(article)


# Export the test results as .json
# Use ensure_ascii = False and encoding = 'utf-8' in order to get rid of \u****
with open('file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(parsed, f, indent=4, ensure_ascii=False)
