#coding=utf-8

'''
    域名生成的一些辅助函数
'''
from pypinyin import pinyin,Style
import jieba
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
import re


tlds_list = ['.com', '.cn', '.com.cn', '.gov.cn', '.net', '.org']


def pinyin_2_hanzi(pinyin_str):
    '''
    zhao qing shi ding hu qu fang di chan xie hui --- 肇庆市鼎湖区房地产协会
    '''
    pinyin_list = pinyin_str.split()
    dagParams = DefaultDagParams()
    # 1个候选值
    result = dag(dagParams, pinyin_list, path_num=1, log=True)
    if result:
        res = result[0].path # 转换结果
        hanzi_str = ''.join(res)
        return hanzi_str
    else:
        return ''
        logger.info("转化有误：" + pinyin_str)


def get_first_letter_str(word):
    '''
    肇庆市 --- zqs
    '''
    word_first_letter_list = pinyin(word, style=Style.FIRST_LETTER) # 提取每个词拼音的首字母有
    word_first_letter = ''
    for i in word_first_letter_list:
        if len(i[0]) > 0 and (i[0].isdigit() or i[0].isalpha() or i[0] == '-'):
            word_first_letter += i[0]
    return word_first_letter


def pinyin_get_first_letters_list(pinyin_array):
    '''
    zhao qing shi ding hu qu fang di chan xie hui --- [u'zqs', u'dhq', u'fdc', u'xh']
    '''
    hanzi_str = pinyin_2_hanzi(pinyin_array) # 转化为汉字
    if hanzi_str == '':
        return []
    hanzi_list = list(jieba.cut(hanzi_str)) # 将汉字分词
    word_letter_list = [] # 分词后所有词的首字母列表
    # 分词后获取每个词的首字母列表，并返回
    for word in hanzi_list:
        first_letter_str = get_first_letter_str(word)
        word_letter_list.append(first_letter_str)
    # print word_letter_list
    return word_letter_list


def combine_word_letter_to_maindomain(word_letter_list):
    '''
    将词的首字母组合，得到新的域名
    [u'zqs', u'dhq', u'fdc', u'xh'] --[u'zqsdhq.com', u'zqsdhq.cn', u'zqsdhq.com.cn',...]

    '''
    new_domains = []
    length = len(word_letter_list)
    for i,word_letter in enumerate(word_letter_list):
        j = i + 1
        while j < length :
            new_main_domain = word_letter + word_letter_list[j]
            if len(new_main_domain) < 7:
                for tld in tlds_list:
                    new_domain = new_main_domain + tld
                    new_domains.append(new_domain)
            j += 1
    return new_domains


def en_get_first_letter_list(en_name):
    '''
    得到分词各首字母的列表
    Local Taxation Bureau of Yiwu City, Zhejiang -- ['ltb', 'y', ',z']

    问题：地名只有第一个字的首字母
    '''
    first_letter_list = []
    en_name = en_name.lower()
    first_split = re.split(' of |,|city| and | district | in ',en_name)
    # print first_split
    if len(first_split) > 1:
        for word in first_split:
            word_first_letter = ''
            # print word.split()
            for i in word.split():
                if len(i[0]) > 0 and (i[0].isdigit() or i[0].isalpha() or i[0] == '-'):
                    word_first_letter += i[0]
                elif len(i) > 1 and i[0] == '(':
                    word_first_letter += i[1]
            first_letter_list.append(word_first_letter)
        print first_letter_list
    else:
        # 对于'of|,|city|and|district|'无法划分的，实际生成的域名与generateBy_all_words(domain_info)生成的会重复，故舍去
        return []
    return first_letter_list
