import requests
import re, time
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
import random,base64
import os


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
headers = {'User-Agent':UA}
search_headers = {'User-Agent':UA,'Referer':'https://www.jy3y.com/'}

stime = time.time()
mov_list = []

cmmd = 'ip a'
ff = os.popen(cmmd)
rr = ff.read()
print('ip a 结果为:\n\n\n',rr)


def print_time():
	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	return '【' + t + '】 '
date = print_time()[1:-2].replace('-','').split(' ')[0]
print('date is ',date,'\n')
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

def parseitem(url):
	r = try_get(url)
	data = r.json()
	return data['subjects']
  
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

def get_series_detail_page_url(namelist):
	search_url = f"https://www.jy3y.com/search.php?searchword={quote(namelist[0])}&submit="
	r = try_get(f"{search_url}",headers = search_headers)
	search_soup = BeautifulSoup(r.text,'lxml')

	ul_tag = search_soup.find('ul',id = "searchList")
	mov_url = ''
	if ul_tag:
		title = ul_tag.find_all('h4',class_='title')
		for i in title:
			mov_name = i.text
			if namelist[0] in mov_name and namelist[1] in mov_name:
				mov_url = i.a['href']

	if mov_url:
		series_play_page_url = 'https://www.jy3y.com' + mov_url
		print('Series page url:',series_play_page_url)
		return series_play_page_url
	return 0

def get_db_series(data):
	num = 1
	no_list = []
	series_info_list = []
	print('FN getdbseries',len(data))
	for mov in data:
		print()
		print(mov['title'],mov['rate'])
		print(f'{print_time()}此类别单页进度：{num}/{len(data)}')
		num += 1
		detail_link = get_detail_page_url(mov['title'])
		print('before enter if in FN get_db_series')
		if detail_link:
			print('FN getdbseries No.1 if')
			r = try_get(detail_link,headers=headers)
			print(f'{print_time()}已获取RESPONSE')
			series_soup = BeautifulSoup(r.text,'lxml')
			epsoide_tag = series_soup.find('div',id = "playlist1").ul.find_all('li')
		
			epsoide_links = []
			series_info = {}
			series_info['name'] = mov['title']
			series_info['rate'] = mov['rate']
			print('\n集数',len(epsoide_tag))
			for li in epsoide_tag:
				link = 'https://www.jy3y.com' + li.a['href']
				epsoide_num = mov['title'] + ' E' + str(epsoide_tag.index(li) + 1)
				
				txt_num = ' E' + str(epsoide_tag.index(li) + 1)
				
				play_page_r = try_get(link,headers=headers)
				print('\n\nplay_page_r is _\n',play_page_r,'\n')
				if play_page_r:
					p = r'var vfrom="\d+";var vpart="\d+";var now="(.*?)";var pn='
					pattern = re.compile(p)
					epsoide_play_link = re.findall(pattern,play_page_r.text)
					print(print_time(),epsoide_play_link)
					epsoide_links.append((epsoide_num, epsoide_play_link[0]))
					
					msg = f"\n{mov['title']}{mov['rate']}分{txt_num}，{epsoide_play_link[0]}"
					with open(date + '.txt','a',encoding='utf-8') as f:
						f.write(msg)
			if epsoide_links:
				print('\ntest1 目录mov_title\n',mov['title'],mov['rate'])
				mlmsg = f"\n#EXTINF:-1 group-title=\"目录\",{mov['title']}{mov['rate']}分 共{len(epsoide_links)}集\n##"
				with open('Series.m3u','a',encoding='utf-8') as f:
					f.write(mlmsg)
				series_info['epsoide_links'] = epsoide_links
				series_info_list.append(series_info)
		elif ' ' in mov['title']:
			print('FN getdbseries No.1 if elif ' ' in mov[title]')
			mov_title = mov['title'].split(' ')
			detail_link = get_series_detail_page_url(mov_title)
			if detail_link:
				print('entered no.2 if deatil link')
				r = try_get(detail_link,headers=headers)
				print(f'{print_time()}已获取RESPONSE')
				series_soup = BeautifulSoup(r.text,'lxml')
				epsoide_tag = series_soup.find('div',id = "playlist1").ul.find_all('li')
				print('\n集数',len(epsoide_tag))
			
				epsoide_links = []
				series_info = {}
				series_info['name'] = mov['title']
				series_info['rate'] = mov['rate']
				for li in epsoide_tag:
					link = 'https://www.jy3y.com' + li.a['href']
					epsoide_num = mov['title'] + ' E' + str(epsoide_tag.index(li) + 1)
					
					txt_num = ' E' + str(epsoide_tag.index(li) + 1)
					
					play_page_r = try_get(link,headers=headers)
					print('\n\nplay_page_r is _\n',play_page_r,'\n')
					if play_page_r:
						p = r'var vfrom="\d+";var vpart="\d+";var now="(.*?)";var pn='
						pattern = re.compile(p)
						epsoide_play_link = re.findall(pattern,play_page_r.text)
						print(print_time(),epsoide_play_link)
						epsoide_links.append((epsoide_num, epsoide_play_link[0]))
						msg = f"\n{mov['title']}{mov['rate']}分{txt_num}，{epsoide_play_link[0]}"
						with open(date + '.txt','a',encoding='utf-8') as f:
							f.write(msg)
				if epsoide_links:
					print('\ntest2 目录mov_title\n',mov['title'],mov['rate'])
					mlmsg = f"\n#EXTINF:-1 group-title=\"目录\",{mov['title']}{mov['rate']}分 共{len(epsoide_links)}集\n##"
					with open('Series.m3u','a',encoding='utf-8') as f:
						f.write(mlmsg)
					series_info['epsoide_links'] = epsoide_links
					series_info_list.append(series_info)
			else:
				print(mov['title'],' 404\n')
		else:
			print(mov['title'],' 404\n')
	if series_info_list:
		return series_info_list
	else:
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
			epsoide_num = name + ' E' + str(epsoide_tag.index(li) + 1)
			txt_num = ' E' + str(epsoide_tag.index(li) + 1)
			
			play_page_r = try_get(link,headers=headers)
			if play_page_r:
				p = r'var vfrom="\d+";var vpart="\d+";var now="(.*?)";var pn='
				pattern = re.compile(p)
				epsoide_play_link = re.findall(pattern,play_page_r.text)
				
				msg = f"\n{series_name}{txt_num}，{epsoide_play_link[0]}"
				with open(date + '.txt','a',encoding='utf-8') as f:
					f.write(msg)
				print(print_time(),epsoide_play_link)
				epsoide_links.append((epsoide_num, epsoide_play_link[0]))
		if epsoide_links:
			print('\ntest3 目录mov_title\n',mov['title'],mov['rate'])
			mlmsg = f"\n#EXTINF:-1 group-title=\"目录\",{series_name} 共{len(epsoide_links)}集\n##"
			with open('Series.m3u','a',encoding='utf-8') as f:
				f.write(mlmsg)
			series_info['epsoide_links'] = epsoide_links
		return series_info
	else:
		return 0		
		
def save_series(data):
	msg = ''
	print('START SAVE DATA...')
	for i in data['epsoide_links']:
		msg += f"\n#EXTINF:-1 group-title=\"{data['name']}\",{i[0]}\n{i[1]}"
	with open('Series.m3u','a',encoding='utf-8') as f:
		f.write(msg)
	print('All DONE.')
	return msg

def save_db_series(data,token):
	
	print('START SAVE DATA...\n')
	for x in data:
		msg = ''
		#print(x['name'],len(x['epsoide_links']))
		#print('has ',len(data))
		for i in x['epsoide_links']:
			text = f"\n#EXTINF:-1 group-title=\"{token} {x['name']}_{x['rate']}分\",{i[0]}\n{i[1]}"
			msg += text
			#print(text)
		with open('Series.m3u','a',encoding='utf-8') as f:
			f.write(msg)
	print('All DONE.')
	return msg


def main():
	all_mov_list = []
	token = '热门 美剧 英剧 韩剧 日剧 国产剧 港剧 日本动画 综艺 纪录片'.split(' ')
	with open('Series.m3u','a',encoding='utf-8') as f:
		f.write("#EXTM3U")
	check_list = []
	for e in token:
		real_mov_list = []
		url = f'https://movie.douban.com/j/search_subjects?type=tv&tag={quote(e)}&sort=recommend&page_limit=20&page_start=0'
		print(url,f'\n{print_time()}当前类别：{e}')
		mov_list = parseitem(url)[:10]
		# 单分类里去重
		for y in mov_list:
			if y not in real_mov_list:
				real_mov_list.append(y)
		# 各分类间去重
		really_mov_list = []
		for x in real_mov_list:
			if x not in check_list:
				really_mov_list.append(x)
		print(e,'分类 ',len(real_mov_list),'部')
		if e != '热门':
			check_list.extend(real_mov_list)
		all_mov_list.extend(real_mov_list)
		
		series_info_list = get_db_series(really_mov_list)
		if series_info_list:
			#print(series_info_list)
			save_db_series(series_info_list,e)
		else:
			print('404')
	time.sleep(30)
	# 剧集
	all_msg  = ''
	name_list = ['流金岁月','上阳赋','阳光之下','山海情','大江大河','大江大河2','巡回检察组','隐秘的角落','终极笔记','半泽直树2','陈翔六点半2015','陈翔六点半2016','陈翔六点半2019','陈翔六点半2020']
	compare_list = []
	result_list = []
	for i in all_mov_list:
		compare_list.append(i['title'])
	print(f'已搜寻豆瓣剧集{len(compare_list)}部，如下：\n',compare_list)
	for x in name_list:
		if x not in compare_list:
			result_list.append(x)
	print('result list = ',result_list)
	for i in result_list:
		data = get_Series(i)
		if data:
			print(data['name'],len(data))
			all_msg += save_series(data)
		time.sleep(3)
      
main()
