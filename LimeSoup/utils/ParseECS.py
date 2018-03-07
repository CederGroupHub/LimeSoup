#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import pymongo as pm
import json

from LimeSoup.ECSSoup import ECSSoup

__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


if __name__ == '__main__':

    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parser_papers = db["Parsered_Paper"]

    with open('data/example_ECS_paper.html', 'r') as fd:
        html_str = fd.read()
    # Provide input interface to the html str, associated with the paper DOI index
    data = ECSSoup.parse(html_str)
    with open('data/data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    new_data_id = coll_parser_papers.insert_one(data).inserted_id
