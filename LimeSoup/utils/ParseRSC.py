#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from LimeSoup.RSCSoup import RSCSoup

import pymongo as pm

__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


if __name__ == '__main__':
    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parser_paper = db["Parsered_Paper"]

    with open('data/example_RSC_paper.html', 'r') as fd:
        html_str = fd.read()
    # Provide input interface to the html str, associated with the paper DOI index
    dados = RSCSoup.parse(html_str)
    new_data_id = coll_parser_paper.insert_one(dados).inserted_id
    processed_json = RSCSoup.parse(html_str)
    pprint(processed_json)
    with open('data/after.html', 'w') as fd:
        fd.write(repr(processed_json))


class TestRSCRemoveTagsSmallSub:
    html_str = """"
                       <html>
                       <body>
                           <p> a<strong>b </strong>c </p>
                           <span> a<strong>b </strong>c </span>
                           <span> a<strong>b </strong>c <span> a<strong>b </strong>c </span> </span>
                       </body>
                       </html>
                       """
