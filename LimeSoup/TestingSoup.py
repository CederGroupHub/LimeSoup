# -*- coding: utf-8 -*-
# from LimeSoup.NatureSoup import NatureSoup
from pprint import pprint
import random, os, glob, re
import requests
import json
from bs4 import BeautifulSoup
from LimeSoup.NatureSoup import NatureSoup

#### TEST PARSER USING HTML FILES ####
# # Select random article from ~65,000
directory = os.path.realpath('C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls')
html_files = glob.glob(os.path.join(directory, '*.html'))
articles = random.sample(html_files, 20) # This number represents size of sample

directory = os.path.realpath('C:\\Users\\Jason\\Desktop\\Shell\\Synthesis Articles')
articles = glob.glob(os.path.join(directory, '*Z.html'))


# # ***Automatically find path of LimeSoup\TestingSoup.py***
# # ***Test the parser using the included test files***
# file_path = os.path.realpath(__file__)
# directory = os.path.dirname(file_path)
# test_file_directory = directory + "\\test\\nature_papers"
#
# articles = [test_file_directory +'\\10103835012032.html',
#             test_file_directory +'\\10103835050110.html',
#             test_file_directory + '\\101038416304a.html',
#             test_file_directory +'\\10103818335.html',
#             test_file_directory +'\\10103826206.html',
#             test_file_directory +'\\10103819734.html']


# TODO: These articles are currently not parsed. They seem to be a very small subset.
    #   If it becomes a noticeable issue in regular usage, I will attempt to fix.

# # These articles have an entirely different format, they do not have 'article-body'
# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature05027.html',
#             'C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature05904.html']

# # Everything parses but methods remains blank, *Methods section has h3 and (mainly) h4 tags for subsection titles*
# articles = ['C:\\Users\\Jason\\Desktop\\nature_htmls\\nature_htmls\\101038nature21420.html']

parsed = []
for article in articles:    # Quickly test using nature links
    print(article)
    with open(article, 'r', encoding = 'utf-8') as f:
        article_text = f.read()
    try:
        parsed.append(NatureSoup.parse(article_text))

    except Exception as e:
        os.startfile(article)
        print(e)


# Export the test results as .json
# Use ensure_ascii = False and encoding = 'utf-8' in order to get rid of \u****
with open('Nature_file_test.json', 'w', encoding = 'utf-8') as f:
    json.dump(parsed, f, indent=4, ensure_ascii=False)
