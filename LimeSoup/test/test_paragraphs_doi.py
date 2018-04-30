import pickle
import pymongo as pm
from pprint import pprint


def random_paragraph(datas):
    for data in datas:
        data = db.Paragraphs_tmp.aggregate([{"$sample": {"size": 1}}]).next()


def print_paragraph(data_paragraph):
    print('##########################################')
    print('ID:', data_paragraph['_id'])
    print('PATH:', data_paragraph['path'])
    print('DOI:', data_paragraph['DOI'])
    doi_link = 'doi.org/{:}'.format(data_paragraph['DOI'])
    print("http://{:} ".format(doi_link))
    print('-----------------------------------------')
    pprint(data_paragraph['text'])
    input_ = input()
    return input_


def search_doi_from_picke():
    with open('doi_diffs.pickle', 'rb') as fd:
        data = pickle.load(fd)

    for doi_data in data:
        print('############################')
        print('############################')
        print('DOI:', doi_data, '   Number of paragraphs:', data[doi_data])
        data_db = db.Paragraphs_tmp.find({"DOI": doi_data})
        for paragraphs_i in data_db:
            input_ = print_paragraph(paragraphs_i)
            if input_ == 'e':
                break


if __name__ == '__main__':
    host = '***REMOVED***'
    user = '***REMOVED***'
    password = '***REMOVED***'
    client = pm.MongoClient(host, 27017) #, user=user, password=password)
    # client.SynPro.authentication()
    db = client.the_database.authenticate(user, password, source='SynPro')
    db = client['SynPro']
    doi_list = db.Meta_data

    paragraphs = db["Paragraphs_tmp"]
    datas = list(paragraphs_tmp.find()).limit(2000)) #{"Publisher": "RSC"})

    # {'ancestors': 'Results and '}


    # db.Paragraphs.find({"ancestors": "Experimental"})
    # db.Paragraphs.find({"path": /^_root\$\$Experiment/})


    import os
    #
    #
    # for d in data:
    #     pprint(d)
    #
    # exit()



    for doi in data:
        print(doi)
