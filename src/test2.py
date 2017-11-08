#coding=utf-8
import json
from log import *
from pypinyin import pinyin,Style
import jieba
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

# domain_info = {
#     "domain": "www.spyjk.com",
#     "province_pinyin": "tian jin shi",
#     "web_name_pinyin": "tian jin shi ke xue ji shu qi kan xue hui",
#     "department_pinyin": "tian jin shi ke xue ji shu qi kan xue hui",
#     "department_en": "Tianjin society of science and Technology Periodicals",
#     "web_name_en": "Tianjin society of science and Technology Periodicals"
#   }

domain_info = {
    "domain": "www.tjkjxm.org.cn",
    "province_pinyin": "tian jin shi",
    "web_name_pinyin": "tian jin ke ji xing mao xin xi wang",
    "department_pinyin": "tian jin shi ke xue ji shu xin xi yan jiu suo",
    "department_en": "Tianjin Institute of science and technology information",
    "web_name_en": "Tianjin science and Technology Information Network"
  }

def store(data):
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def json_load():
    with open('domains_data.json') as json_file:
        data = json.load(json_file)
        return data

def pinyin_2_hanzi(pinyin_str):
    pinyin_list = pinyin_str.split()
    dagParams = DefaultDagParams()
    # 1个候选值
    result = dag(dagParams, pinyin_list, path_num=1, log=True)
    if result:
        res = result[0].path # 转换结果
        hanzi_str = ''.join(res)
        return hanzi_str
    else:
        logger.info("转化有误：" + pinyin_str)


def get_first_letter_str(word):
    '''
    肇庆市 --- zqs
    '''
    word_first_letter_list = pinyin(word, style=Style.FIRST_LETTER) # 提取每个词拼音的首字母有
    word_first_leter = ''
    for alpha in word_first_letter_list:
        word_first_leter += alpha[0]
    return word_first_leter


def get_first_letters_list(pinyin_array):
    '''
    zhao qing shi ding hu qu fang di chan xie hui --- [u'zqs', u'dhq', u'fdc', u'xh']
    '''
    hanzi_str = pinyin_2_hanzi(pinyin_array) # 转化为汉字
    hanzi_list = list(jieba.cut(hanzi_str)) # 将汉字分词
    word_letter_list = [] # 分词后所有词的首字母列表
    # 分词后获取每个词的首字母列表，并返回
    for word in hanzi_list:
        first_letter_str = get_first_letter_str(word)
        word_letter_list.append(first_letter_str)
    return word_letter_list



if __name__ == '__main__':
    # word_letter_list = get_first_letters_list("zhao qing shi ding hu qu fang di chan xie hui")
    # print word_letter_list
    print pinyin_2_hanzi("zhao qing shi ding hu qu fang di chan xie hui")
