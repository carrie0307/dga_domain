#coding=utf-8
from pymongo import *
import json
'''
将数据库中程序结果导处到json文件
'''


client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_head_words



if __name__ == '__main__':
    dga_res = []
    res = collection.find({},{'domain': True, '_id':False,'new_domains':True, 'domains_reg':True})
    res = list(res)
    for domain_info in res:
        dga_res.append(domain_info)
    with open('domain_dga_headwords_data.json', 'w') as json_file:
        json_file.write(json.dumps(dga_res))
    print 'over ... '
    # with open('domain_ega_all.json') as json_file:
    #     data = json.load(json_file)
    # for domain in data:
    #     print domain["new_domains"][0]
