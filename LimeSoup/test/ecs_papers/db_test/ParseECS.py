#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import pymongo as pm
from pprint import pprint

from LimeSoup.ECSSoup import ECSSoup
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

    data_list = list(coll_paper_raw_html.find({"Publisher": "ECS"}).limit(5000))
    fd = open('problems.txt', 'w')
    for i_paper in range(520,  5000, 1):
        data = data_list[i_paper]
        id_paper = data["_id"]
        print("Dealing with paper number: {}".format(i_paper))
        print("DOI: ", data["DOI"])
        print("Publisher: ", data["Publisher"])
        # Provide input interface to the html str, associated with the paper DOI index
        html_str = data["Paper_Raw_HTML"]
        data_complete = ECSSoup.parse(html_str)
        data = data_complete['obj']
        plan_data = tl.n_paragraphs_sections(data)
        parser_tb = parser.ParserPaper(html_str, debugging=True)
        list_remove = [
            {'name': 'div', 'class_': 'section-nav'},  # Navigation buttons
            {'name': 'div', 'class_': 'contributors'},  # Authors
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class_': 'fig pos-float odd'},  # Figures
            {'name': 'div', 'id': 'ref-list-1'},  # References
            {'name': 'span', 'class_': 'disp-formula'},  # Formulas
            {'name': 'span', 'class_': 'kwd-group-title'},  # Keyword labels
            {'name': 'div', 'class_': 'table-caption'},  # Caption Table
            {'name': 'div', 'class_': 'table-inline'},  # Table in line
            {'name': 'div', 'id': 'fn-group-1'},  # Footnotes
            {'name': 'div', 'id': 'license-1'}
        ]
        parser_tb.remove_tags(rules=list_remove)
        parser_tb.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'div', 'class': 'article fulltext-view'},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        parser_tb.save_soup_to_file('test.html')
        """
        for para, para_plan in zip(parser_tb.paragraphs, plan_data['paragraphs']):
            print('######################################################################')
            print(para)
            print('----------------------------------------------------------------------')
            print(para_plan)
        """

        if len(parser_tb.paragraphs) > len(plan_data['paragraphs']):
            data['problem'] = True
            data['problem_p'] = True
            print(len(parser_tb.paragraphs), len(plan_data['paragraphs']))
            fd.write('problem paragraphs paper i: {}\n'.format(i_paper))
            # input('problem paragraphs')
        if len(parser_tb.headings) > len(plan_data['headings']):
            data['problem'] = True
            data['problem_h'] = True
            print(len(parser_tb.headings), len(plan_data['headings']))
            fd.write('problem headings paper i: {}\n'.format(i_paper))
            # input('problem headings')
        # saving data to the database
        new_data_id = coll_parser_papers.insert_one(data).inserted_id
        """
        for i, heading_i in enumerate(plan_data['headings']):
            print(i, heading_i)
        print(" ###### ")
        for i, heading_i in enumerate(parser_tb.headings):
            print(i, heading_i)
        """
        for i, heading_i in enumerate(parser_tb.paragraphs):
            #try:
                print(i, parser_tb.paragraphs[i])
                print(i, plan_data['paragraphs'][i])
                print(" ###### ")
            #except:
            #    print('error!!!')
        if 'problem' in data.keys():
            input('continue...')
