#coding=utf-8

'''
注册域名数量统计与比例
'''

from __future__ import division
from pymongo import *


'''建立链接'''
client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_word_pinyin

def count_res_info(res):
    '''
    注册域名数量统计与比例
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







if __name__ == '__main__':
    res = collection.find({},{'domain': True, '_id':False, 'domains_reg':True})
    count_res_info(list(res))
