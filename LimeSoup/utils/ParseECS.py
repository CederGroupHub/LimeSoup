#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from LimeSoup.RSCSoup import RSCSoup
from pprint import pprint
import pymongo as pm

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':

    with open('example_RSC_paper.html', 'r') as fd:
        html_str = fd.read()

    # Provide input interface to the html str, associated with the paper DOI index
    with open('before.html', 'w') as fd:
        fd.write(html_str)

    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parsered_paper = db["Parsered_Paper"]
    dados = RSCSoup.parse(html_str)
    new_data_id = coll_parsered_paper.insert_one(dados).inserted_id

    processed_json = RSCSoup.parse(html_str)
    pprint(processed_json)
    with open('after.html', 'w') as fd:
        fd.write(repr(processed_json))
