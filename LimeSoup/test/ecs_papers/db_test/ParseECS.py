#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

__author__ = 'Tiago Botari'
__maintainer__ = 'Tiago Botari'
__email__ = 'tiagobotari@gmail.com'


import pymongo as pm
from pprint import pprint

from LimeSoup.ECSSoup import ECSSoup
from LimeSoup.parser import parser_paper as parser
import LimeSoup.parser.tools as tl

# qrsh

if __name__ == '__main__':

    query_mdb = {
        "$and": [
            {"Publisher": "ECS"},
            {
                "$or": [
                        {"Lock": {"$exists": False}},
                        {"Lock": False}
                ]
            },
            {
                "$or":[
                        {"Parser": {"$exists": False}},
                        {"Parser": False}
                        ]
            }
        ]
    }
    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parser_papers = db["Parsered_Paper"]
    data_list = list(coll_paper_raw_html.find({"Publisher": "ECS"}).limit(5000))
    fd = open('problems.txt', 'w')
    # for i_data, data in enumerate(coll_paper_raw_html.find()):
    #     print('##############################')
    #     print('Number : ', i_data)
    #     doi_v = data['DOI']
    #     print('DOI: ', doi_v)
    #     number_parser = list(coll_parser_papers.find({'DOI': doi_v}))
    #     print('Number Parser: ', number_parser)
    #     if number_parser != 1:
    #         input('problem?')
    # exit()
    # data = coll_paper_raw_html.find(query_mdb).limit(1)
    # print(list(data))
    # exit()
    #for i_paper, data in enumerate(coll_paper_raw_html.find(query_mdb)):
    print('here')
    i_paper = 0
    query_mdb = {"Publisher": "ECS"}
    '10.1149/1.3492151, 10.1149/1.3492174, 10.1149/1.3492188'
    query_mdb = {'DOI': '10.1149/1.3492188'}
    data_list = list(coll_paper_raw_html.find(query_mdb).limit(1))
    print(data_list)
    print('fim')
    exit()
    for data in data_list:

    # while True:
    #     data = list(coll_paper_raw_html.find(query_mdb).limit(1))
        if len(data) == 0:
            break
        i_paper += 1
        # data = data[0]
        data['Lock'] = True
        id_paper = data["_id"]
        coll_paper_raw_html.update_one(
            {"_id": id_paper},
            {
                "$set": {
                        "Lock": True,
                        "Parser": False
                    }
            }
        )
        print("Dealing with paper number: {}".format(i_paper))
        print("DOI: ", data["DOI"])
        doi_i_paper = data["DOI"]
        print("Publisher: ", data["Publisher"])
        # Provide input interface to the html str, associated with the paper DOI index
        html_str = data["Paper_Raw_HTML"]
        data_complete = ECSSoup.parse(html_str)
        data_new = data_complete['obj']
        data_new['DOI'] = doi_i_paper
        #data_plan = tl.flatten_json(data_new)
        #pprint(data_plan)
        #exit()
        plan_data = tl.n_paragraphs_sections(data_new)
        #pprint(plan_data)


        parser_tb = parser.ParserPaper(html_str, debugging=True)
        #parser_tb.save_soup_to_file('original.html')
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
        rules = [
            {'name': 'span', 'class': 'highwire-journal-article-marker-start'},
            {'name': 'ul', 'class': 'epreprint-list'}
        ]
        parser_tb.strip_tags(rules)

        #parser_tb.save_soup_to_file('clean_paper.html')
        #print(' Create from parser_tb!!!!')
        parser_tb.create_tag_to_paragraphs_inside_tag(
            rule={'name': 'div', 'class': 'article fulltext-view'},
            name_new_tag='h2',
            name_section='Introduction(guess)'
        )
        #parser_tb.save_soup_to_file('test.html')
        """
        for para, para_plan in zip(parser_tb.paragraphs, plan_data['paragraphs']):
            print('######################################################################')
            print(para)
            print('----------------------------------------------------------------------')
            print(para_plan)
        """

        if len(parser_tb.paragraphs) > len(plan_data['paragraphs']):
            data_new['problem'] = True
            data_new['problem_p'] = True
            print(len(parser_tb.paragraphs), len(plan_data['paragraphs']))
            fd.write('problem paragraphs paper i: {}\n'.format(i_paper))
            # input('problem paragraphs')
            with open('error_paragraphs_paper_{}'.format(i_paper), 'w') as fd1:
                for i, heading_i in enumerate(parser_tb.paragraphs):
                    try:
                        fd1.write('from test: {} {}\n'.format(i, parser_tb.paragraphs[i]))
                        fd1.write('from Soup: {} {}\n'.format(i, plan_data['paragraphs'][i]))
                        fd1.write(" ###### \n")
                    except:
                        continue

        if len(parser_tb.headings) > len(plan_data['headings']):
            data_new['problem'] = True
            data_new['problem_h'] = True
            print(len(parser_tb.headings), len(plan_data['headings']))
            fd.write('problem headings paper i: {}\n'.format(i_paper))
            with open('error_headings_paper_{}'.format(i_paper), 'w') as fd1:
                for i, heading_i in enumerate(parser_tb.headings):
                    try:
                        fd1.write('{} {}\n'.format(i, parser_tb.paragraphs[i]))
                        fd1.write('{} {}\n'.format(i, plan_data['paragraphs'][i]))
                        fd1.write("###### \n")
                    except:
                        continue
            # input('problem headings')
        # saving data_new to the database
        new_data_id = coll_parser_papers.insert_one(data_new).inserted_id
        coll_paper_raw_html.update_one(
            {"_id": id_paper},
            {
                "$set": {
                    "Lock": False,
                    "Parser": True
                }
            }
        )
        print('Save!!!')
        #       lost_paragraphs = list()
            #       for i, heading_i in enumerate(parser_tb.paragraphs):
            #           if heading_i not in plan_data['paragraphs']:
            #               lost_paragraphs.append(heading_i)
        """
            try:
                print('from test: {} {}\n'.format(i, parser_tb.paragraphs[i]))
                print('from Soup: {} {}\n'.format(i, plan_data['paragraphs'][i]))
                print(" ###### \n")
            except:
                continue
            """
#        print('----->', len(parser_tb.paragraphs), len(plan_data['paragraphs']))
        #if 'problem' iFalseFalsen data.keys():
        #    input('continue...')
    fd.close()