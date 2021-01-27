import requests
import time,random
from bs4 import BeautifulSoup

# 完成一页电影播放链接获取 2021年1月7日 21点56分
# 多页获取OK
# 临时 <12H！！
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
only_ua_header = {'user-agent':UA}

def print_time():
	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	return '【' + t + '】 '

def get(url,headers = only_ua_header):
	try:
		r = requests.get(url,headers = headers)
		return r
	except ConnectionError:
		print('---------------------<ConnectionError!>---------------------')
	except:
		return 0
	
def try_get(url,headers = only_ua_header):
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




def parse_home_info(url):
	all_movie_list = []
	print(url)
	response = try_get(url)
	if response.status_code == 200:
		soup = BeautifulSoup(response.text,'lxml')
		# Extract info we nd
		movie_detail_page = soup('p',class_='image')
		for each in movie_detail_page:
			movie_detail_page_tag = each('a')
			# print(len(movie_detail_page))
			for x in movie_detail_page_tag:
				one_movie_info = {}
				one_movie_info['name'] = movie_detail_page_tag[0].find('img').get('alt')
				# print(one_movie_info['name'])
				one_movie_info['detail_url'] = movie_detail_page_tag[0].get('href')# 电影详情页链接
				one_movie_info['rate'] = movie_detail_page_tag[0].text.strip()[:3]# 电影评分
				one_movie_info['post'] = movie_detail_page_tag[0].find('img').get('data-original')
				print(one_movie_info['name'],one_movie_info['detail_url'],'电影评分：',one_movie_info['rate'])
				if len(one_movie_info['rate']) > 2:
					if float(one_movie_info['rate']) > 6.0:
						print(f"{print_time()} {one_movie_info['name']} Over 6.0")
						all_movie_list.append(one_movie_info)
						# print(len(all_movie_list))
		return all_movie_list
	else:
		print('response != 200',response)

def parse_vod_m3u8(play_page_url):
	response = try_get(play_page_url)
	# print(response.status_code)
	if response.status_code == 200:
		vod_soup = BeautifulSoup(response.text,'lxml')
		# print(vod_soup.prettify())
		# time.sleep(2)
		vod_link = vod_soup('script')[6].string[17:-1]
		# print(type(vod_link))
		# print(vod_link)
		vod_link = vod_link.split('\",\"copyright')
		# print(vod_link[1],'\n',len(vod_link))
		# print(vod_link[0])
		# vod_link = eval(vod_link)
		#('div',id = 'cms_player')[0].find('script').text
		vod_link = vod_link[0].split('\"url\":"')[1].replace('\\','')
		print(vod_link,'lastvod')
		time.sleep(1)
		return vod_link


def save(dic_of_movies,group_title):

	msg = f"\n#EXTINF:-1 group-title=\"{group_title}\",{dic_of_movies['name']} 【{ dic_of_movies['rate']}⭐】\n{dic_of_movies['vod_play_link']}"
	# print(f'开始写入电影-【{dic_of_movies['name']}】\n')
	
	time.sleep(0.1)
	with open('movies.m3u', 'a',encoding='utf-8') as f:
		f.write(msg)

def main(url,group_title):
	all_movie_list = parse_home_info(url)
	# print(all_movie_list,'rrrr')
	n = 1
	if all_movie_list:
		for e in all_movie_list:
			detail_url = 'https://www.wandouys.com' + e['detail_url']
			print('detail_url',detail_url)
			r =try_get(detail_url)
			detail_soup = BeautifulSoup(r.text,'lxml')
			a_tag = detail_soup.find('a',class_ = "btn btn-default btn-block btn-sm text-ellipsis")
			if a_tag:
				vod_page_url = 'https://www.wandouys.com' + a_tag.get('href')
				print(vod_page_url)
				e['vod_play_link'] = parse_vod_m3u8(vod_page_url)
				print(f"{print_time()}开始写入第{n}部电影---{e['name']}")
				save(e,group_title)
				n += 1
			else:
				print('No Play Page')
				continue

	print(all_movie_list)

def run(token):
	base = f'https://www.wandouys.com/video/type/1-{token}-----addtime'
	start_url = f'https://www.wandouys.com/video/type/1-{token}-----addtime.html'
	start_referer = 'https://www.wandouys.com/video/type/1---2020---addtime.html'
	if token == '%E5%8A%A8%E4%BD%9C':
		group_title = '动作'
	elif token == '%E7%88%B1%E6%83%85':
		group_title = '爱情'
	elif token == '%E5%96%9C%E5%89%A7':
		group_title = '喜剧'
	start_time = time.time()
	for i in range(1,10):
		print(f'{print_time()}正在抓取第 {i} 页')
		if i == 1:
			main(start_url,group_title)
		else:
			start_url = base + '-' + str(i) + '.html'
			main(start_url,group_title)
		time.sleep(random.choice([3,2,2,1,5,4]))
	cost_time = time.time() - start_time
	print(f'Cost time {cost_time/60} minutes.')


# https://www.wandouys.com/video/type/1-%E5%96%9C%E5%89%A7-----addtime.html
if __name__ == '__main__':
	with open('movies.m3u', 'a',encoding='utf-8') as f:
		f.write('#EXTM3U')
	token = {'%E5%96%9C%E5%89%A7','%E7%88%B1%E6%83%85','%E5%8A%A8%E4%BD%9C'}
	for i in token:
		run(i)
