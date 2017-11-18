#coding=utf-8
import domain_gene_assis

# domain_info = {
#     "domain": "www.zqdhfx.com",
#     "province_pinyin": "guang dong sheng",
#     "web_name_pinyin": "zhao qing shi ding hu qu fang di chan xie hui",
#     "department_pinyin": "zhao qing shi ding hu qu fang di chan xie hui",
#     "department_en": "Dinghu Zhaoqing District Real Estate Association",
#     "web_name_en": "Dinghu District Real Estate Association of Zhaoqing"
#   }

domain_info = {
    "domain": "www.zqdhfx.com",
    "province_pinyin": "guang dong sheng",
    "web_name_pinyin": "zhao qing shi ding hu qu fang di chan xie hui",
    "department_pinyin": "zhao qing shi ding hu qu fang di chan xie hui",
    "department_en": "Dinghu Zhaoqing District Real Estate Association",
    "web_name_en": "Dinghu District Real Estate Association of Zhaoqing"
  }

# domain_info = {
#     "domain": "www.qc-center.com",
#     "province_pinyin": "tian jin shi",
#     "web_name_pinyin": "xin xi chan ye bu zhuan yong cai liao zhi liang jian du jian yan zhong xin",
#     "department_pinyin": "zhong guo dian zi ke ji ji tuan gong si di si shi liu yan jiu suo",
#     "department_en": "The forty-sixth Research Institute of China Electronic Technology Group Corporation",
#     "web_name_en": "Special material quality supervision and inspection center of Ministry of information industry"
#   }



# domain_info = {
#     "domain": "www.mzgcc.com",
#     "province_pinyin": "guang dong sheng",
#     "web_name_pinyin": "mei zhou shi gong shang ye lian he hui ( zong shang hui )",
#     "department_pinyin": "guang dong sheng mei zhou shi gong shang ye lian he hui",
#     "department_en": "Meizhou Guangdong Federation of industry and Commerce",
#     "web_name_en": "Meizhou Federation of industry and Commerce ( General Chamber of Commerce)"
#   }

tlds_list = ['.com', '.cn', '.com.cn', '.gov.cn', '.net', '.org']
ini_name_list = ["web_name_pinyin", "department_pinyin", "department_en", "web_name_en"]



def generateBy_all_words(domain_info):
    '''
    (方法一--连续所有词首字母生成)
    所有词首字母组合，如域名www.tjlgbw.cn的 web_name_pinyin: tian jin lao gan bu wang ,生成的主域名是 tjlgbw
    '''
    global ini_name_list
    global tlds_list
    all_words_new_domains = [] # 此法生成新域名列表
    for key in ini_name_list:
        if domain_info[key] != "None":
            ini_name = domain_info[key].split() # 产生新域名的原名称
            new_main_domain = ''
            for i in ini_name:
                if len(i[0]) > 0 and (i[0].isdigit() or i[0].isalpha() or i[0] == '-'):
                    new_main_domain += i[0]
            for tld in tlds_list:
                new_domain = new_main_domain + tld
                all_words_new_domains.append(new_domain)
    all_words_new_domains = list(set(all_words_new_domains))
    return all_words_new_domains


def generateBy_part_Pinyinwords(domain_info):
    '''
    (方法三--不连续拼音生成)
    (不连续)对"web_name_pinyin"、"department_pinyin"分词后两两组合进行生成
    '''
    global ini_name_list
    global tlds_list
    pinyin_part_new_domains = []
    # 对"web_name_pinyin"进行生成
    word_letter_list = domain_gene_assis.pinyin_get_first_letters_list(domain_info["web_name_pinyin"])
    web_new_domain_list = domain_gene_assis.combine_word_letter_to_maindomain(word_letter_list)
    pinyin_part_new_domains = web_new_domain_list
    # web_name_pinyin 和 department_pinyin可能重复
    if domain_info["web_name_pinyin"] != domain_info["department_pinyin"]:
        word_letter_list = domain_gene_assis.pinyin_get_first_letters_list(domain_info["department_pinyin"])
        department_new_domain_list = domain_gene_assis.combine_word_letter_to_maindomain(word_letter_list)
        pinyin_part_new_domains.extend(department_new_domain_list)
    # 去重
    pinyin_part_new_domains = list(set(pinyin_part_new_domains))
    return pinyin_part_new_domains


def generateBy_part_Enwords(domain_info):
    '''
    (方法三--不连续英文生成)
    (不连续)对"web_name_en"、"department_en"分词后两两组合进行生成
    '''
    global ini_name_list
    global tlds_list
    en_part_new_domains = []
    word_letter_list = domain_gene_assis.en_get_first_letter_list(domain_info["web_name_en"])
    web_new_domain_list = domain_gene_assis.combine_word_letter_to_maindomain(word_letter_list)
    en_part_new_domains = web_new_domain_list
    if domain_info["web_name_en"] != domain_info["department_en"]:
        word_letter_list = domain_gene_assis.en_get_first_letter_list(domain_info["department_en"])
        department_new_domain_list = domain_gene_assis.combine_word_letter_to_maindomain(word_letter_list)
        en_part_new_domains.extend(department_new_domain_list)
    # 去重
    en_part_new_domains = list(set(en_part_new_domains))
    return en_part_new_domains


def generateBy_head_words(domain_info):
    '''
    四个名称的前n个字首字母组合，得到长度为4,5,6的主域名
    '''
    global ini_name_list
    global tlds_list
    head_new_domains = []
    for key in ini_name_list:
        if domain_info[key] != "None":
            name = domain_info[key]
        else:
            continue
        name_list = name.split()
        new_main_domain = ''
        i = 0
        while i < min(len(name_list), 3): # 先组合出前3个字的首字母的组合
            if len(name_list[i][0]) > 0 and (name_list[i][0].isdigit() or name_list[i][0].isalpha() or name_list[i][0] == '-'):
                new_main_domain += name_list[i][0]
            i += 1
        if i >= len(name_list):# 说明len(name_list)<4,只能生成长度小于4的主域名,直接与顶级域组合
            new_main_domain = new_main_domain.lower()
            for tld in tlds_list:
                new_domain = new_main_domain + tld
                head_new_domains.append(new_domain)
        else: # 可以生成长度大于4的主域名
            while i < min(len(name_list), 6):
                if len(name_list[i][0]) > 0 and (name_list[i][0].isdigit() or name_list[i][0].isalpha() or name_list[i][0] == '-'):
                    new_main_domain += name_list[i][0]
                    new_main_domain = new_main_domain.lower()
                    for tld in tlds_list:# 与顶级域组合
                        new_domain = new_main_domain + tld
                        head_new_domains.append(new_domain)
                i += 1
    head_new_domains = list(set(head_new_domains)) # 去重
    return head_new_domains





if __name__ == '__main__':
    # pass
    # print generateBy_all_words(domain_info)
    # print generateBy_part_Pinyinwords(domain_info)
    # print generateBy_part_Enwords(domain_info)
    domains = generateBy_head_words(domain_info)
    print domains
    print len(domains)
