import requests
import re, time
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
import random


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
search_headers = {'user-agent':UA,'referer':'https://www.nfstar.net/'}


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

def parseitem(url):
	r = try_get(url)
	data = r.json()
	return data['subjects']

def search_f_site(data):
	"""accept a list
		reloop to find vod url in jy3y"""
	num = 1
	no_list = []
	for mov in data:
		print(mov['title'],mov['rate'])
		print(f'{print_time()}此类别单页进度：{num}/{len(data)}')
		num += 1
		detail_link = get_detail_page_url(mov['title'])
		if detail_link:
			r = try_get(detail_link,headers=headers)
			print(f'{print_time()}已获取RESPONSE')
			detail_soup = BeautifulSoup(r.text,'lxml')
			a_tag_link = detail_soup.find('a',class_ = "btn btn-warm")
			if a_tag_link:
				a_tag_link = a_tag_link.get('href')
			else:
				continue
			mov_play_page_url = 'https://www.nfstar.net' + a_tag_link
# link_next":"","link_pre":"","url":"(.*?)","url_next":"","from":"danmuku
			# 获取源
			play_r = try_get(mov_play_page_url,headers=headers)
			p = r'link_next":"","link_pre":"","url":"(.*?)","url_next":"","from":"\w+'
			pattern = re.compile(p)
			play_link = re.findall(pattern,play_r.text)
			
			if play_link:
				msg = f"\n#EXTINF:-1 group-title=\"目录\",{mov['title']} 【{ mov['rate']}⭐】\n192.168.1.1.1"

				with open('star_movs.m3u','a',encoding='utf-8') as f:
					f.write(msg)
				real_play_link = play_link[0].replace('\\','')
				mov['vod_url'] = real_play_link
				mov['playable'] = 'YES'
				print(f'{print_time()}m3u8链接为：',real_play_link,'\n')
			else:
				print(mov['title'],'评分',mov['rate'],'无源')
			time.sleep(1)
		else:
			print(mov['title'],'评分',mov['rate'],'未搜到\n')
			no_list.append((mov['title'],mov['rate']))
			continue
	return data,no_list

def save(mov_list,token):
	#存放本地
	b_save = time.time()
	print(f"{print_time()}正在保存...")
	for e in mov_list:
		# print(e)
		if e['playable'] == 'YES':
			msg = f"\n#EXTINF:-1 group-title=\"{token}\",{e['title']} 【{ e['rate']}⭐】\n{e['vod_url']}"
			with open('star_movs.m3u','a',encoding='utf-8') as f:
				f.write(msg)

	save_cost_time = time.time() -b_save
	print(f'{print_time()}Save file cost time {save_cost_time}.')

def get_movs():
	with open('star_movs.m3u','a',encoding='utf-8') as f:
		f.write('#EXTM3U')
	unfindmov = []
	token = ['热门', '豆瓣高分','动作','喜剧', '爱情','科幻','华语', '欧美', '韩国', '日本', '悬疑', '恐怖', '动画','治愈' ]
	for i in token:
		all_mov_list = []
		for n in range(0,20,20):
			select_url = f'https://movie.douban.com/j/search_subjects?type=movie&tag={quote(i)}&sort=recommend&page_limit=20&page_start={n}'
			print(select_url,f'{print_time()}当前类别：{i},当前页码：{n/20}')
			mov_list = parseitem(select_url)
			print('before search_f_site')
			mov_list,no_list = search_f_site(mov_list)
			unfindmov.extend(no_list)
			print(mov_list)
			save(mov_list,i)

		print(f'\n\n{i}分类下未找到的电影有{len(unfindmov)}部，如下：{unfindmov}\n')
		time.sleep(5)
	print(f'\n\n全部分类下未找到的电影有{len(unfindmov)}部，如下：{unfindmov}\n')
	time.sleep(30)

def get_detail_page_url(name):
	search_url = f"https://nfstar.net/vodsearch/{quote(name)}-------------/"
	r = try_get(f"{search_url}",headers = search_headers)
	search_soup = BeautifulSoup(r.text,'lxml')

	ul_tag = search_soup.find('ul',id = "searchList")
	mov_url = ''
	if ul_tag:
		title = ul_tag.find_all('h4',class_='title')
		for i in title:
			mov_name = i.text
			if name in mov_name:
				mov_url = i.a['href']

	if mov_url:
		series_play_page_url = 'https://www.nfstar.net' + mov_url
		print('Series page url:',series_play_page_url)
		return series_play_page_url
	return 0

def main():
	# get_movs()
	test_headers={'user-agent':UA,'authority': 'www.nfstar.net', 'referer':'https://www.nfstar.net/vodplay/100087-1-1/'}
	r = try_get('https://ladao.top/newmovie/20201228/%E7%96%AF%E7%8B%82%E5%8E%9F%E5%A7%8B%E4%BA%BA2.2020.m3u8',headers=test_headers)
	print(r.status_code,r.text)
main()
