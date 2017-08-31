#coding=utf-8
import requests, json
from bs4 import BeautifulSoup
from lxml import html
r = requests.get('http://www.cdut.edu.cn/type_gxlm/020300010203.html')
tree = html.fromstring(r.text)
soup = BeautifulSoup(r.content,'lxml')
d = {}
d1 = {}
l1 = []
l2 = []
# soup = soup.select('.dq')[0]
soup = soup.select('.urlportlet_141041356879148118')[0]
# print soup
for link in soup.find_all('a'):
	a = str(link.get('href'))
	# if 'swun' in a:
	url = link.get('href')
	name = link.get_text().strip()
	print url
	# url1 = url.split('/')[2]
	# l1.append(url)
	# l2.append(url1)
	# d[url]=name
	# d1[url1]=name
print l1
print l2
print json.dumps(d,encoding='utf-8',ensure_ascii=False)
print json.dumps(d1,encoding='utf-8',ensure_ascii=False)

