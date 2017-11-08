#coding=utf-8
from __future__ import division
from pymongo import *

'''建立链接'''
client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_word_pinyin

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









if __name__ == '__main__':
    # name = "xin xi chan ye bu zhuan yong cai liao zhi liang jian du jian yan zhong xin"
    name = "xin xi chan ye bu zhuan yong"
    name_list = name.split()
    new_main_domain = ''
    i = 0
    while i < min(len(name_list), 3):
        if len(name_list[i][0]) > 0 and (name_list[i][0].isdigit() or name_list[i][0].isalpha() or name_list[i][0] == '-'):
            new_main_domain += name_list[i][0]
        i += 1
    if i >= len(name_list):# 说明len(name_list)<4,只能生成长度小于4的主域名
        print new_main_domain
        # 直接与顶级域组合
    else: # 可以生成长度大于4的主域名
        while i < min(len(name_list), 6):
            if len(name_list[i][0]) > 0 and (name_list[i][0].isdigit() or name_list[i][0].isalpha() or name_list[i][0] == '-'):
                new_main_domain += name_list[i][0]
                print new_main_domain
                # 直接与顶级域组合
            i += 1
