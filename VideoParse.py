import requests
import re, time
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
import random,base64


user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                       'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                       'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                       r'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                       r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']
index = random.randint(0, 9)
UA = user_agents[index]
headers = {'user-agent':UA}
search_headers = {'user-agent':UA,'referer':'https://www.jy3y.com/'}

stime = time.time()
mov_list = []


def print_time():
	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	return '【' + t + '】 '

def get(url,headers = headers):
	try:
		r = requests.get(url,headers = headers)
		return r
	except ConnectionError:
		print('---------------------<ConnectionError!>---------------------')
	except:
		return 0
	
def try_get(url,headers = headers):
	retry_nums = 0
	return_from_get = get(url,headers)
	if return_from_get == 0:		
		retry_nums += 1		
		if retry_nums >= 3:
			print('Have Retryed 4 times\n\nRetry after Terminate --80S')
			time.sleep(80)
			try_get(url,headers)
		else:
			print('Max retries exceeded\n\nRetry after Terminate --15S')
			time.sleep(15)
			try_get(url,headers)
	else:
		return return_from_get

def get_detail_page_url(name):
	search_url = f"https://www.jy3y.com/search.php?searchword={quote(name)}&submit="
	r = try_get(f"{search_url}",headers = search_headers)
	search_soup = BeautifulSoup(r.text,'lxml')

	ul_tag = search_soup.find('ul',id = "searchList")
	mov_url = ''
	if ul_tag:
		title = ul_tag.find_all('h4',class_='title')
		for i in title:
			mov_name = i.text
			if mov_name == name:
				mov_url = i.a['href']

	if mov_url:
		series_play_page_url = 'https://www.jy3y.com' + mov_url
		print('Series page url:',series_play_page_url)
		return series_play_page_url
	return 0

def get_Series(name):
	
	series_play_page_url = get_detail_page_url(name=name)
	if series_play_page_url:
		r= try_get(series_play_page_url,headers=headers)
		series_soup = BeautifulSoup(r.text,'lxml')
		# print(series_soup.prettify())
		series_name = series_soup.find('h1',class_="title").text
		print(series_name)
		time.sleep(1)
		epsoide_tag = series_soup.find('div',id = "playlist1").ul.find_all('li')
		# print(epsoide_tag)
		
		epsoide_links = []
		series_info = {}
		series_info['name'] = name
		for li in epsoide_tag:
			link = 'https://www.jy3y.com' + li.a['href']
			epsoide_num = '第 ' + str(epsoide_tag.index(li) + 1) + ' 集'
			
			play_page_r = try_get(link,headers=headers)

			p = r'var vfrom="\d+";var vpart="\d+";var now="(.*?)";var pn='
			pattern = re.compile(p)
			epsoide_play_link = re.findall(pattern,play_page_r.text)
			print(print_time(),epsoide_play_link)
			epsoide_links.append((epsoide_num, epsoide_play_link[0]))
		series_info['epsoide_links'] = epsoide_links
		return series_info
	else:
		return 0

def save_series(data):
	# #for github action
	# url = 'https://api.github.com/repos/lswlover2579/PyCrawlers/contents/Series.m3u'
	# req = requests.get(url)
	# print('已获取req')
	# if req.status_code == requests.codes.ok:
	#     print('req.status_code == requests.codes.ok')
	#     req = req.json()  # the response is a JSON
	#     # req is now a dict with keys: name, encoding, url, size ...
	#     # and content. But it is encoded with base64.
	#     print('start base64decode')
	#     content = base64.b64decode(req['content'])
	#     print('start decode to utf-8')
	#     all_text = content.decode('utf-8')
	# else:
	#     print(req.json())
	#     print('Content was not found.')

	msg = ''
	
	print('START SAVE DATA...')
	# with open('Series.m3u','r',encoding='utf-8') as f:
	# 	all_text = f.read()
	for i in data['epsoide_links']:
		msg += f"\n#EXTINF:-1 group-title=\"{data['name']}\",{i[0]}\n{i[1]}"
		# if i[1] not in all_text:
		# 	msg += f"\n#EXTINF:-1 group-title=\"{data['name']}\",{i[0]}\n{i[1]}"
		# 	print(f"{data['name']} {i[0]} *新* 待追加.")
		# else:
		# 	print(f"{data['name']} {i[0]} 已存在.")
		
	with open('Series.m3u','a',encoding='utf-8') as f:
		f.write(msg)
	print('All DONE.')
	return msg

def main():
	# 剧集
	all_msg  = ''
	name_list = ['流金岁月','上阳赋','阳光之下','山海情','大江大河','大江大河2','巡回检察组','隐秘的角落','终极笔记','半泽直树','陈翔六点半2015','陈翔六点半2016','陈翔六点半2019','陈翔六点半2020']
	with open('Series.m3u','a',encoding='utf-8') as f:
		f.write("#EXTM3U")
	for i in name_list:
		data = get_Series(i)
		if data:
			print(data['name'],len(data))
			all_msg += save_series(data)
		time.sleep(3)
	return all_msg


main()
