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
    query_mdb = {
        "$and": [
            {"Publisher": "RSC"},
            {
                "$or": [
                    {"Lock": {"$exists": False}},
                    {"Lock": False}
                ]
            },
            {
                "$or": [
                        {"Parser": {"$exists": False}},
                        {"Parser": True}
                        ]
            }
        ]
    }
    client = pm.MongoClient('localhost', 27017)
    db = client['SynPro']
    coll_paper_raw_html = db["Paper_Raw_HTML"]
    coll_parser_papers = db["Parsered_Paper"]

    #data_list = list(coll_paper_raw_html.find())  # {"Publisher": "RSC"}

    #print(len(data_list))

    #exit()
    fd = open('problems.txt', 'w')

    # for i_paper in range(5000):
    # data = data_list[i_paper]
    i_paper = 0
    datas = list(coll_paper_raw_html.find({"Publisher": "RSC"}).limit(2000))
    for data in datas:
    # while True:
    # if True:

        # data = coll_paper_raw_html.aggregate([
        #     {"$match": {"Publisher": "RSC"}},
        #     {"$sample": {"size": 1}}]
        # ).next()[0]

        # doi_query = '10.1039/C5QI00200A'

        # query_mdb = {'DOI': doi_query}
        #query_mdb = {'DOI': '10.1039/C4QI00128A'}
        #query_mdb = {'DOI': '10.1039/B003394O'}
        # data = list(coll_paper_raw_html.find(query_mdb).limit(1))[0]
        # data = list(coll_paper_raw_html.find({"Publisher": "RSC"}).limit(1))
        if len(data) == 0:
            exit()
        #     break

        i_paper += 1
        #data = data[0]
        # data['Lock'] = True
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

        doi_i_paper = data["DOI"]

        print("Dealing with paper number: {}".format(i_paper))
        print("DOI: ", doi_i_paper)
        print("Publisher: ", data["Publisher"])

        # Provide input interface to the html str, associated with the paper DOI index
        html_str = data["Paper_Raw_HTML"]
        data_complete = RSCSoup.parse(html_str)
        data_new = data_complete['obj']
        data_new['DOI'] = doi_i_paper
        plane_data = tl.n_paragraphs_sections(data_new)
        parser_tb = parser.ParserPaper(html_str, parser_type='html.parser', debugging=True)
        # parser_tb.save_soup_to_file('original.html')

        list_remove = [
            {'name': 'p', 'class': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class': 'image_table'},  # Figures
            {'name': 'div', 'id': 'crossmark-content'},  # Another Logo
            {'name': 'code'},  # Codes inside the HTML
            {'name': 'div', 'class': 'table_caption'},
            {'name': 'div', 'class': 'rtable__wrapper'},
            {'name': 'div', 'class': 'left_head'},
            {'name': 'table'},
            {'name': 'div', 'class': 'right_head'},  # just in the test not in the soup
            {'name': 'div', 'class': 'article_info'} # just in the test not in the soup
        ]
        parser_tb.remove_tags(rules=list_remove)
        parser_tb.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser_tb.compile('First published on')}]
        )
        parser_tb.create_tag_from_selection(
            rule={'name': 'p', 'class': 'abstract'},
            name_new_tag='h2'
        )
        rules = [{'name': 'span', 'id': parser_tb.compile('^sect[0-9]+$')}]
        parser_tb.strip_tags(rules)
        journal_name = parser_tb.get([{'name': 'a', 'title': 'Link to journal home page'}])
        # len(parser_tb.paragraphs)

        paragraphs_tb = ['Journal'] + parser_tb.span

        clean_text_html = parser_tb.soup.prettify()

        if len(paragraphs_tb) > len(plane_data['paragraphs']):
            with open('clean_{:}.html'.format(i_paper), 'w') as f_html:
                f_html.write(clean_text_html)

            data_new['problem'] = True
            data_new['problem_p'] = True
            print('Paragraphs error:')
            print(len(paragraphs_tb),  ' from soup: ', len(plane_data['paragraphs']))
            fd.write('problem paragraphs paper i: {}\n'.format(i_paper))
            # input('problem paragraphs')
            with open('error_paragraphs_paper_{}'.format(i_paper), 'w') as fd1:
                fd1.write('DOI: {}\n'.format(doi_i_paper))
                for i, heading_i in enumerate(paragraphs_tb):
                    try:
                        fd1.write('From cou.: {} {}\n'.format(i, paragraphs_tb[i]))
                        fd1.write('From Soup: {} {}\n'.format(i, plane_data['paragraphs'][i]))
                        fd1.write(" ###### \n")
                        print('From cou.: {} {}\n'.format(i, paragraphs_tb[i]))
                        print('From Soup: {} {}\n'.format(i, plane_data['paragraphs'][i]))
                        print(" ###### \n")
                    except:
                        continue

        if len(parser_tb.headings) > len(plane_data['headings']):
            with open('clean_{:}.html'.format(i_paper), 'w') as f_html:
                f_html.write(clean_text_html)

            data_new['problem'] = True
            data_new['problem_h'] = True
            print('Heading error:')
            print(len(parser_tb.headings), ' from soup: ', len(plane_data['headings']))
            fd.write('problem headings paper i: {}\n'.format(i_paper))
            with open('error_headings_paper_{}'.format(i_paper), 'w') as fd1:
                fd1.write('DOI: {}\n'.format(doi_i_paper))
                for i, heading_i in enumerate(parser_tb.headings):
                    try:
                        fd1.write('from test: {} {}\n'.format(i, parser_tb.headings[i]))
                        fd1.write('from soup: {} {}\n'.format(i, plane_data['headings'][i]))
                        fd1.write(" ###### \n")
                    except:
                        continue
        # saving data to the database
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
        print('Salved os data!!!')
        # exit()
            #except:
            #    print('error!!!')
        #print('----->', len(paragraphs_tb), len(plane_data['paragraphs']))

#        if 'problem' in data.keys():
#            input('continue...')


# def data1():
#     for raw_doc in tqdm(raw_col.find(), total=raw_col.find().count()):
#         if "parsed" in raw_doc and \
#                 raw_doc["parsed"] and \
#                 StrictVersion(raw_doc["parser_version"]) >= StrictVersion(parser_version):
#             pass
#     else:
#         parsed_doc = None
#     try:
#         if raw_doc['Publisher'] == "ECS":
#             parsed_doc = ECSSoup.parse(raw_doc['Paper_Raw_HTML'])['obj']
#     elif raw_doc['Publisher'] == "RSC":
#     parsed_doc = RSCSoup.parse(raw_doc['Paper_Raw_HTML'])['obj']
#     if parsed_doc is not None:
#         parsed_doc['DOI'] = raw_doc['DOI']
#     parsed_doc["parser_version"] = parser_version
#     parsed_col.replace_one({'DOI': raw_doc["DOI"].strip()}, parsed_doc, upsert=True)
#     raw_doc["parsed"] = True
#     except Exception as e:
#     raw_doc["parsed"] = False
#     raw_doc["err_msg"] = str(e)
#     logging.warning("Failed to parse " + raw_doc['DOI'] + ": " + str(e))
#     raw_doc["parser_version"] = parser_version
#     raw_col.replace_one({'DOI': raw_doc["DOI"].strip()}, raw_doc)
#     logging.info("Finished Parsing Raw HTML")