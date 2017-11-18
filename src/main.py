#coding=utf-8

import domain_verify
import domain_generate
import threading
import time
import json
import Queue
from pymongo import *

thread_num = 1


'''建立链接'''
client = MongoClient('172.29.152.152', 27017)
db = client.domain_icp_analysis
collection = db.domain_dga_head_words

domain_q = Queue.Queue()
new_domain_q = Queue.Queue()
domain_verify_q = Queue.Queue()
domain_res_q = Queue.Queue()
res_json = []

def json_load():
    global domain_q
    print '获取域名...'
    finish_domains = []
    res = collection.find({'flag':1},{'domain': True, '_id':False})
    for domain in list(res):
        finish_domains.append(str(domain["domain"]))
    with open('domains_data2.json') as json_file:
        data = json.load(json_file)
        for domain in data:
            if domain["domain"] not in finish_domains:
                # print '---'
                domain_q.put(domain)
    print '获取域名结束...'



def generate_new_domains_handler():
    '''
    根据原域名列表生成新的域名
    '''
    global domain_q
    global domain_verify_q
    while not domain_q.empty():
        domain_info = domain_q.get()
        '''全部首字母生成'''
        # new_domains = domain_generate.generateBy_all_words(domain_info)
        '''拼音不连续词生成 '''
        # new_domains = domain_generate.generateBy_part_Pinyinwords(domain_info)
        '''英文不连续词生成 '''
        # new_domains = domain_generate.generateBy_part_Enwords(domain_info)
        '''前若干个字首字母生成'''
        new_domains = domain_generate.generateBy_head_words(domain_info)
        # print new_domains
        domain_verify_q.put([domain_info["domain"], new_domains])
    print "new domains over ..."


def verify_domains_handler():
    '''
    对新生成的域名验证是否注册
    '''
    global domain_verify_q
    global domain_rew_q
    while True:
        try:
            domain,new_domains = domain_verify_q.get(timeout=200)
            time.sleep(2)
        except:
            print '无待验证域名...\n'
            break
        domain_res = domain_verify.domain_verify_by_whois(new_domains)
        domain_res_q.put([domain, new_domains, domain_res])
        # time.sleep(3)
    print 'domain verify over ...'


def save_json_data():
    global domain_res_q
    global res_json
    global collection
    counter = 0
    while True:
        try:
            domain, new_domains, domain_res = domain_res_q.get(timeout=200)
            print domain
            collection.update({'domain': domain}, {'$set':{'flag':1, 'new_domains':new_domains, 'domains_reg':domain_res}})
            print '----'
        except:
            print '存储结束...\n'
            break

def main():
    json_load()
    print "开始生成新域名\n"
    generate_new_domains = threading.Thread(target=generate_new_domains_handler)
    generate_new_domains.start()
    domain_verify_td = []
    print "验证新域名\n"
    for _ in range(thread_num):
        domain_verify_td.append(threading.Thread(target=verify_domains_handler))
    for td in domain_verify_td:
        td.start()
    print "开始存储结果\n"
    save_res = threading.Thread(target=save_json_data)
    save_res.start()
    save_res.join()


if __name__ == '__main__':
    main()
