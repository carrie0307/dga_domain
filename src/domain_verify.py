#coding=utf-8
'''

功能： 通过whois信息判断域名是否被注册

'''
import whois



def domain_verify_by_whois(new_domains):
	'''
	功能： 通过whois信息判断域名是否被注册

	param: new_domains:待验证域名的列表

	return: domain_res 域名验证结果对应列表，与new_domains中域名一一对应
	'''
	domain_res = []
	for domain in new_domains:
		flag = False
		for _ in range(3):
			try:
				whois_info = whois.whois(domain)
				if whois_info.status:
					domain_res.append(1)
					flag = True
					break
				else:
					domain_res.append(0)
					flag = True
					break
			except Exception, e:
				if "No match" in str(e):
					domain_res.append(0)
					flag = True
					break
				else:
					continue

		if not flag:
			print domain, str(-1)
			domain_res.append(-1)
	return domain_res


if __name__ == '__main__':
	domains = [u'tjfejkw.com', u'tjfejkw.cn', u'tjfejkw.com.cn', u'tjfejkw.gov.cn', u'tjfejkw.net', u'tjfejkw.org', u'tjsfnetbjzx.com', u'tjsfnetbjzx.cn', u'tjsfnetbjzx.com.cn', u'tjsfnetbjzx.gov.cn', u'tjsfnetbjzx.net', u'tjsfnetbjzx.org', u'Twachcc.com', u'Twachcc.cn', u'Twachcc.com.cn', u'Twachcc.gov.cn', u'Twachcc.net', u'Twachcc.org', u'Twachn.com', u'Twachn.cn', u'Twachn.com.cn', u'Twachn.gov.cn', u'Twachn.net', u'Twachn.org']
	print domain_verify_by_whois(['TsosaTP.com'])
