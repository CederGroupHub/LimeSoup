# -*- coding: utf-8 -*-
"""
Use of the Elsevier parser on some papers
"""

from LimeSoup.ElsevierSoup import ElsevierSoup
import pymongo as pm
import re

client = pm.MongoClient('localhost', 27017, username="test", password="test", authSource="admin")
client_***REMOVED*** = pm.MongoClient('***REMOVED***', 27017, username = '***REMOVED***', password = '***REMOVED***', authSource = 'synthesis',
                       readPreference='nearest',replicaSet='rs0')

db = client['admin']
db_***REMOVED*** = client_***REMOVED***['synthesis']
coll_elsevierpapers = db_***REMOVED***['ElsevierPapers']
coll_parseredpapers = db['ParsedElsevier5']

##
txt = open('Elsevier_journals_upd.json','r')
list_tmp = txt.read().replace('[','').replace(']','').replace('\n','').replace('"','').split(',')
journals = [journal[2:] for journal in list_tmp]
num_papers = 10
print('Trying to parse',str(len(journals)*num_papers),'papers.')
##
nb_errors = 0
for journal in journals:
    print('JOURNAL:',journal)
    query_mdb = {"Crawled":True, "Journal": journal}
    #query_mdb = {"DOI": "10.1016/S0016-2361(00)00007-7"}
    documents = list(coll_elsevierpapers.find(query_mdb).limit(num_papers))
    if len(documents) == 0:
        print('No paper in',journal,'satisfies the query:',str(query_mdb))

    for i_paper, data in enumerate(documents):
        if len(data) == 0:
            pass
        id_paper = data["_id"]
        print("Dealing with paper number: {}".format(i_paper))
        print("DOI: ", data["DOI"])
        doi_i_paper = data["DOI"]
        journal_name = data["Journal"]
        print("Journal: ", data["Journal"])
        title = ''
        try:
            title = data["Title"]
        except:
            pass
        xml_str = data["Paper_Content"]
        try:
            data_complete = ElsevierSoup.parse(xml_str)
            data_new = data_complete['obj']
            data_new['DOI'] = doi_i_paper
            if len(data_new['Journal']) == 0:
                data_new['Journal'] = [journal_name]
            if len(data_new['Title']) == 0:
                data_new['Title'] = [title]
            coll_parseredpapers.insert_one(data_new)
            print('Document parsed and saved.')
        except Exception as e:
            nb_errors += 1
            with open('problems','a') as f:
                f.write('Problem with paper DOI:'+str(data["DOI"])+ 'in journal:'+str(data["Journal"])+'\n')
                f.write(str(e))
                f.write('\n')
            print('Problem with paper DOI:', data["DOI"], 'in journal:',data["Journal"])

print('There were',str(nb_errors),'errors. Please check problems file.')
