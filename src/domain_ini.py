# coding=utf-8
from pymongo import *
import json
'''
将原始的domain转移到dga表中
'''


client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_word_pinyin

def json_load():
    domains = []
    with open('domains_data.json') as json_file:
        data = json.load(json_file)
        for domain in data:
            # print domain["domain"]
            domains.append(domain["domain"])
    return domains



def store(data):
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def transfer_domains(domains):
    """
    将域名和document的原始构造插入表中
    :param domains: 原始的域名列表
    :return: 域名列表
    """
    global gollection
    # print domains
    domain_documents = [{'domain':domain, 'new_domains':[], 'domains_reg':[], 'flag':0} for domain in domains]
    collection.insert_many(domain_documents)
    print 'insert over ... '


def strip_fun(string):
    return string.strip()





if __name__ == '__main__':
    # global collection
    # res = collection.find({'flag':0},{'domain': True, '_id':False})
    # string = ''
    # for domain in list(res):
    #     string = string + str(domain["domain"]) + '\n'
    # with open('duplicate_domains.txt','w') as f:
    #     f.write(string)

    domains = json_load()
    transfer_domains(domains)
