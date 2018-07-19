#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import pymongo as pm
from pprint import pprint

from LimeSoup.RSCSoup import RSCSoup
from LimeSoup.parser import parser_paper as parser
import LimeSoup.parser.tools as tl


__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


if __name__ == '__main__':
    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parser_papers = db["Parsered_Paper"]

    # for i_paper in range(5000):
    # data = data_list[i_paper]
    i_paper = 0
    data_list = list(coll_paper_raw_html.find({"Publisher": "RSC"}).limit(2000))
    for data in data_list:
        i_paper += 1
        id_paper = data["_id"]
          = data["DOI"]

        # print("Dealing with paper number: {}".format(i_paper))
        # print("DOI: ", doi_i_paper)
        # print("Publisher: ", data["Publisher"])

        # Provide input interface to the html str, associated with the paper DOI index.
        html_str = data["Paper_Raw_HTML"]
        data_complete = RSCSoup.parse(html_str)
        data_new = data_complete['obj']
        # Saving data to the database.
        new_data_id = coll_parser_papers.insert_one(data_new).inserted_id
        # print('Salved data!!!')
