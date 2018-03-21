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

    data_list = list(coll_paper_raw_html.find({"Publisher": "RSC"}).limit(5000))
    fd = open('problems.txt', 'w')
    for i_paper in range(171,  5000, 1):
        data = data_list[i_paper]
        id_paper = data["_id"]
        doi_value =  data["DOI"]
        print("Dealing with paper number: {}".format(i_paper))
        print("DOI: ", doi_value)
        print("Publisher: ", data["Publisher"])
        # Provide input interface to the html str, associated with the paper DOI index
        html_str = data["Paper_Raw_HTML"]
        data_complete = RSCSoup.parse(html_str)
        data = data_complete['obj']
        plane_data = tl.n_paragraphs_sections(data)
        parser_tb = parser.ParserPaper(html_str, parser_type='html.parser', debugging=True)
        parser_tb.save_soup_to_file('original.html')

        list_remove = [
            {'name': 'p', 'class': 'header_text'},  # Authors
            {'name': 'div', 'id': 'art-admin'},  # Data rec./accept.
            {'name': 'div', 'class': 'image_table'},  # Figures
            {'name': 'a', 'class': 'simple'},  # Logo
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
        parser_tb.save_soup_to_file('clean_paper_tb.html')

        if len(paragraphs_tb) > len(plane_data['paragraphs']):
            data['problem'] = True
            data['problem_p'] = True
            print('Paragraphs error:')
            print(len(paragraphs_tb),  ' from soup: ', len(plane_data['paragraphs']))
            fd.write('problem paragraphs paper i: {}\n'.format(i_paper))
            # input('problem paragraphs')
            with open('error_paragraphs_paper_{}'.format(i_paper), 'w') as fd1:
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
            data['problem'] = True
            data['problem_h'] = True
            print('Heading error:')
            print(len(parser_tb.headings), ' from soup: ', len(plane_data['headings']))
            fd.write('problem headings paper i: {}\n'.format(i_paper))
            with open('error_headings_paper_{}'.format(i_paper), 'w') as fd1:
                for i, heading_i in enumerate(parser_tb.headings):
                    try:
                        fd1.write('from test: {} {}\n'.format(i, parser_tb.headings[i]))
                        fd1.write('from soup: {} {}\n'.format(i, plane_data['headings'][i]))
                        fd1.write(" ###### \n")
                    except:
                        continue

        # saving data to the database
        data['DOI'] = doi_value
        data['i'] = i_paper
        new_data_id = coll_parser_papers.insert_one(data).inserted_id
        print('Salvou os dados!!!')
            #except:
            #    print('error!!!')
        print('----->', len(paragraphs_tb), len(plane_data['paragraphs']))

#        if 'problem' in data.keys():
#            input('continue...')

