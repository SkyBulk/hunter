# crawler jobs
#-*- coding: utf-8 -*-
import requests
import json
import os
import sys 
from threading import Thread
from utils import *
class Spider:

	def __init__(self):
		self.data_extracted = {}
		self.data_extracted['jobs'] = []
		self.total_requests = 0 
		self.SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		self.file = os.path.join(self.SITE_ROOT, 'app', 'static','data.json')
		self.headers = {
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		}
		self.max_results_per_city = 200
		self.cities = {
			'US': open(os.path.join(self.SITE_ROOT, 'cities', 'US'), 'r').read().splitlines(),
			'CA': open(os.path.join(self.SITE_ROOT, 'cities', 'CA'), 'r').read().splitlines(),
			'AU': open(os.path.join(self.SITE_ROOT, 'cities', 'AU'), 'r').read().splitlines(),
			'NZ': open(os.path.join(self.SITE_ROOT, 'cities', 'NZ'), 'r').read().splitlines(),
			'DE': open(os.path.join(self.SITE_ROOT, 'cities', 'DE'), 'r').read().splitlines(),
			'GB': open(os.path.join(self.SITE_ROOT, 'cities', 'GB'), 'r').read().splitlines(),
			'IE': open(os.path.join(self.SITE_ROOT, 'cities', 'IE'), 'r').read().splitlines(),
			'BE': open(os.path.join(self.SITE_ROOT, 'cities', 'BE'), 'r').read().splitlines(),
			'FR': open(os.path.join(self.SITE_ROOT, 'cities', 'FR'), 'r').read().splitlines(),
			'IT': open(os.path.join(self.SITE_ROOT, 'cities', 'IT'), 'r').read().splitlines(),
			'NL': open(os.path.join(self.SITE_ROOT, 'cities', 'NL'), 'r').read().splitlines(),
			'ES': open(os.path.join(self.SITE_ROOT, 'cities', 'ES'), 'r').read().splitlines(),
			'MX': open(os.path.join(self.SITE_ROOT, 'cities', 'MX'), 'r').read().splitlines(),
			'CH': open(os.path.join(self.SITE_ROOT, 'cities', 'CH'), 'r').read().splitlines(),
			'SE': open(os.path.join(self.SITE_ROOT, 'cities', 'SE'), 'r').read().splitlines(),
			'PL': open(os.path.join(self.SITE_ROOT, 'cities', 'PL'), 'r').read().splitlines(),
			'RO': open(os.path.join(self.SITE_ROOT, 'cities', 'RO'), 'r').read().splitlines(),
			'CZ': open(os.path.join(self.SITE_ROOT, 'cities', 'CZ'), 'r').read().splitlines(),
			'RU': open(os.path.join(self.SITE_ROOT, 'cities', 'RU'), 'r').read().splitlines(),
			'CN': open(os.path.join(self.SITE_ROOT, 'cities', 'RU'), 'r').read().splitlines(),
			'JP': open(os.path.join(self.SITE_ROOT, 'cities', 'RU'), 'r').read().splitlines(),
			'KR': open(os.path.join(self.SITE_ROOT, 'cities', 'RU'), 'r').read().splitlines(),
			'SG': open(os.path.join(self.SITE_ROOT, 'cities', 'SG'), 'r').read().splitlines(),

		}
		self.urls = {
			'US': 'https://www.indeed.com',
			'CA': 'https://ca.indeed.com',
			'AU': 'https://au.indeed.com',
			'NZ': 'https://nz.indeed.com',
			'DE': 'https://de.indeed.com',
			'GB': 'https://www.indeed.co.uk',
			'IE': 'https://ie.indeed.com',
			'BE': 'https://be.indeed.com',
			'FR': 'https://www.indeed.fr',
			'IT': 'https://it.indeed.com',
			'NL': 'https://www.indeed.nl',
			'ES': 'https://www.indeed.es',
			'MX': 'https://www.indeed.com.mx',
			'CH': 'https://www.indeed.ch',
			'SE': 'https://se.indeed.com',
			'PL': 'https://pl.indeed.com',
			'RO': 'https://ro.indeed.com',
			'CZ': 'https://cz.indeed.com', # Source Code Security Analyst
			'RU': 'https://ru.indeed.com', # Разработчик-исследователь , CWE
			'JP': 'https://jp.indeed.com/',
			'CN': 'https://cn.indeed.com/',
			'KR': 'https://kr.indeed.com/',
			'SG': 'https://www.indeed.com.sg',
		}
		self.job_title = ['penetration tester','ethical hacker','offensive security','reverse engineer','product security','application security','vulnerability researcher','vulnerability research','cwe','information security']

	def run(self):
		for country in self.cities:
			for city in self.cities[country]:
				if country == 'JP':
					self.job_title = ['侵入テスト担当者','倫理ハッカー','攻撃的セキュリティ','リバースエンジニア','製品セキュリティ','アプリケーションセキュリティ','脆弱性調査者','脆弱性調査','cwe',' 情報セキュリティー']
				if country == 'RU':
					self.job_title = ['тестер проникновения', 'этический хакер', 'наступательная безопасность', 'обратный инженер', 'безопасность продукта', 'безопасность приложения', 'исследователь уязвимости', 'исследование уязвимости', 'cwe', ' информационной безопасности']
				if country == 'CN':
					self.job_title = ['滲透測試人員','道德黑客','攻擊性安全','反向工程師','產品安全性','應用程序安全性','漏洞研究人員','漏洞研究','cwe',' 信息安全']
				if country == 'KR':
					self.job_title = [ '침투 테스터', '윤리적 해커', '공격 보안', '역 엔지니어', '제품 보안', '응용 프로그램 보안', '취약성 연구원', '취약성 연구', 'cwe', ' 정보 보안']
				for job_title in self.job_title:
					for start in range(0, self.max_results_per_city, 10):
						url = self.urls[country] + \
							"/jobs?q={}&l={}&sort=date&start={}".format(
								job_title, city, start)
						response = requests.get(url, headers=self.headers)
						data = response.text
						soup = get_soup(data)
						html = soup.find_all(name="div", attrs={"class": "row"})
						for page in html:
							if country == 'JP':
								skills = ['セキュリティ保護','ida pro','gdb','windbg','immunity debugger','boofuzz','peach fuzzer','winafl','python','assembly','mitre att＆ck','ttps','侵入テスト','エクスプロイト','metasploit','metasploitフレームワーク','pentest','コンピューターセキュリティ','hacking','ceh','oscp','osce','osee' ,'侵入テスト','mitre att＆ck','fuzzing','clang','llvm','address sanitizer','afl','fuzzers']
							elif country == 'RU':
								skills = ['средства защиты', 'ida pro', 'gdb', 'windbg', 'отладчик иммунитета', 'boofuzz', 'персиковый фаззер', 'winafl', 'python', 'сборка', 'miter att & ck ',' ttps ',' тестирование на проникновение ',' эксплойты ',' metasploit ',' инфраструктура metasploit ',' pentest ',' computer security ',' hacking ',' ceh ',' oscp ',' osce ',' osee ',' тестирование на проникновение ',' miter att & ck ',' fuzzing ',' clang ',' llvm ',' address sanitizer ',' afl ',' fuzzers ']
							elif country == 'CN':
								skills = ['安全保护',' ida pro',' gdb',' windbg','免疫调试器',' boofuzz','桃子模糊器',' winafl',' python',' assembly',' mitre att＆ck','ttps','渗透测试','利用','metasploit','metasploit框架','pentest','计算机安全性','hacking','ceh','oscp','osce',' osee','渗透测试',' mitre att＆ck',' fuzzing',' clang',' llvm',' address sanitizer','afl',' fuzzers']
							elif country == 'KR':
								skills = [ '보안 보호', 'ida pro', 'gdb', 'windbg', '면역 디버거', 'boofuzz', 'peach fuzzer', 'winafl', 'python', 'assembly', 'mitre att & ck ','ttps ','침투 테스트 ','exploits ','metasploit ','metasploit framework ','pentest ','computer security ','hacking ','ceh ','oscp ','osce ',' osee ','침투 테스트 ','mitre att & ck ','fuzzing ','clang ','llvm ','address sanitizer ','afl ','fuzzers ']
							else:
								prefix = ['30', 'monaten', 'meses', 'luni', 'mois', 'month', 'months', 'maanden', 'mesi', 'mies.', 'm\u00e5nader', '\u043c\u0435\u0441\u044f\u0446\u0435\u0432']
								forbidden = ['clearance','ts/sci','4+ years','5+ years','6+ years','7+ years','8+ years','9+ years','10+ years','11+ years','12+ years','u.s. citizens only','u.s. military veteran','active top secret','us citizen','top secret clearance','top secret/sci','security clearance'] # ,'4 years','5 years','6 years','7 years','8 years','9 years','10 years','11 years','12 years'
								skills = ['security protections', 'ida pro', 'gdb', 'windbg', 'immunity debugger', 'boofuzz', 'peach fuzzer', 'winafl', 'python', 'assembly', 'mitre att&ck', 'ttps', 'penetration testing','exploits', 'metasploit', 'metasploit framework',  'pentest', 'computer security', 'hacking', 'ceh', 'oscp', 'osce', 'osee', 'penetration testing','mitre att&ck', 'fuzzing', 'clang', 'llvm', 'address sanitizer', 'afl', 'fuzzers']
							job = extract_job_title(page)
							date_str = extract_date(page)
							try:
								job_description = extract_fulltext(page['data-jk'])
							except:
								pass
							s_date = date_str.replace('+', '') or date_str.replace('just posted', 'today')
							month_match = [match_prefix for match_prefix in prefix if match_prefix in s_date]
							job_title_match = [job_prefix for job_prefix in self.job_title if job_prefix in job]
							skill_match = check(job_description,forbidden,skills)
							if len(month_match) > 0:
							    pass
							elif "NOT_FOUND" in s_date:
							    pass
							elif not len(skill_match) > 0 :
								pass
							elif not len(job_title_match) > 0:	
								pass
							else:
								self.data_extracted['jobs'].append({
									'job_title': extract_job_title(page).casefold(),
									'company': extract_company(page),
									'city': extract_location(page),
									'date': {
										"display": extract_date(page),
										"timestamp": get_timestamp(extract_date(page))
									},
									'job_description': extract_fulltext(page['data-jk']).casefold(),
									'url':  self.urls[country] + extract_link(page)
								})

							with open(self.file, 'w') as outfile:
								json.dump(unique(self.data_extracted), outfile, indent=4)
							self.total_requests += 1
							print('Total requests: {}'.format(self.total_requests))
from app import app
T1 = Thread(target=Spider().run)
T1.start()
app.run(host='0.0.0.0' , port=5000)
T1.join()
