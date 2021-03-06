#coding=utf-8
from __future__ import division
from pymongo import *
import json

'''建立链接'''
client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_head_words

def count_res_info(res):
    '''
    注册域名数量统计
    '''
    total = 0
    reg_count = 0
    unreg_count = 0
    except_count = 0
    for domain_info in res:
        reg_info = domain_info["domains_reg"]
        total += len(reg_info)
        reg_count += reg_info.count(1)
        unreg_count += reg_info.count(0)
        except_count += reg_info.count(-1)
    print "新域名总量：" + str(total) + '\n'
    print "已注册新域名总量：" + str(reg_count) + '   占比：' + str(round(reg_count/total, 3) * 100) + '%\n'
    print "未注册新域名总量：" + str(unreg_count) + '   占比：' + str(round(unreg_count/total, 3) * 100) + '%\n'
    print "检测出现异常新域名总量：" + str(except_count) + '   占比：' + str(round(except_count/total, 3) * 100) + '%\n'


def create_new_file():
    '''
    把数据库内未运行的域名导出，生成new_file.json（运行中断时处理）
    '''
    print '获取域名...'
    finish_domains = []
    domain_info = []
    res = collection.find({'flag':1},{'domain': True, '_id':False})
    for domain in list(res):
        print domain["domain"]
        finish_domains.append(domain["domain"])
    print 'finish domains get ...\n'
    with open('domains_data.json', 'r') as json_file:
        data = json.load(json_file)
    print 'file open ...\n'
    for domain in data:
        if domain["domain"] not in finish_domains:
                domain_info.append(domain)
                print 'get one domain_info ...'
    print 'write files ...'
    with open('new_file.json', 'w') as json_file:
        json_file.write(json.dumps(domain_info))
    print '获取域名结束...'


def read_file():
    with open('new_file.json', 'r') as json_file:
        data = json.load(json_file)
    for domain in data:
        print domain["domain"]
    print len(data)







if __name__ == '__main__':
    with open('domain_dga_headwords_data.json', 'r') as json_file:
        data = json.load(json_file)
    for i in data:
        print i['new_domains']
