# -*- coding: utf-8 -*-
"""
Use of the Elsevier parser on some papers
Some papers only contain metadata but no "body". In order to get rid of these, the tag
"$where": "this.Paper_Content.length > 15000" is added to the query.
"""

from LimeSoup.ElsevierSoup import ElsevierSoup
import os
import pprint
import pymongo as pm

client = pm.MongoClient('localhost', 27017, username="test", password="test", authSource="admin")
client_***REMOVED*** = pm.MongoClient('***REMOVED***', 27017, username = '***REMOVED***', password = '***REMOVED***', authSource = 'synthesis',
                       readPreference='nearest',replicaSet='rs0')

db = client['admin']
db_***REMOVED*** = client_***REMOVED***['synthesis']
coll_elsevierpapers = db_***REMOVED***['ElsevierPapers']
coll_parseredpapers = db['ParsedElsevier']

query_mdb = {"Crawled":True, "Paper_Content": {"$exists": True}, "$where": "this.Paper_Content.length > 15000"}

num_papers = 20
documents = list(coll_elsevierpapers.find(query_mdb).limit(num_papers))
for i_paper, data in enumerate(documents):
    if len(data) == 0:
        pass
    id_paper = data["_id"]
    print("Dealing with paper number: {}".format(i_paper))
    print("DOI: ", data["DOI"])
    doi_i_paper = data["DOI"]
    print("Journal: ", data["Journal"])
    xml_str = data["Paper_Content"]
    try:
        data_complete = ElsevierSoup.parse(xml_str)
        data_new = data_complete['obj']
        data_new['DOI'] = doi_i_paper
        #plan_data = tl.n_paragraphs_sections(data_new)
        #print(data_new)
        coll_parseredpapers.insert_one(data_new)
        filename = 'data/ElsevierPapertest'+str(i_paper)+'.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'w') as f:
            f.write(pprint.pformat(data_new))
        print('Document parsed and saved.')
    except:
        print('Problem with paper DOI:', data["DOI"], 'in journal:',data["Journal"])


