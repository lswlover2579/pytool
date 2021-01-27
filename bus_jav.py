import requests
import time
import random
from bs4 import BeautifulSoup
import json
import urllib.request
import urllib.parse



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

def bark(title, content):
    """
    ios bark app 推送
    :param bark_machine_code:
    :param title:
    :param content:
    :return:
    """
    try:
        print('正在使用 bark 推送消息...', end='')
        response = requests.get(f'https://api.day.app/推送码/{title}/{content}', timeout=15).json()
        print(response)
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except:
        symbol = '-' * 50
        print(f'\n[⚠ /Scripts/utils/notify.py - bark(bark_machine_code, title, content) bark推送错误]')

def telegram_bot(tg_bot_token, tg_pic, tg_brief,tg_user_id = '',preview_video = '',token=''):
    """
    telegram bot 消息推送
    :param tg_bot_token:
    :param tg_user_id:
    :param title:
    :param content:
    :return:
    """
    try:
    	print('正在使用 telegram机器人 推送消息...', end='')
    	data = {
            'chat_id': tg_user_id,
            'photo': tg_pic,
            'caption':tg_brief,
            # 'disable_web_page_preview': 'true'
        }
    	response = requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendPhoto', data=data, timeout=15).json()
    	if response['ok']:
            print('图文推送成功！')
    	else:
            print('图文推送失败！')

    	if preview_video:
	        print('print preview',preview_video)
	        # headers = {'Accept':'*/*','Accept-Encoding':'gzip,deflate','Accept-Laguage':'zh-Hans-CN;q=1 en-US;q=0.9, zh-Hant-CN;q=0.8','Connection':'close','Content-Type':'application/json'}
	        headers = {"Accept": "*/*","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-Hans-CN;q=1, en-US;q=0.9, zh-Hant-CN;q=0.8","Connection": "close","Content-Type": "application/json"}
	        media_data = {
	        	'chat_id': tg_user_id,
	        	# 'media':dict_data,
	            'video':preview_video,
	            'caption':token + ' Preview'
	            }
	        print('media_data',media_data)
	        response = requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendVideo', data = media_data, timeout=15).json()
	        # response = requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendvideo', data = media_data, headers=headers, timeout=15).json()
	        print(response)
	        if response['ok']:
	            print('Preview Video 推送成功！')
	        else:
	            print('Preview Video 推送失败！')
    except:
    	print(f'\n[⚠ 异常！推送错误]')
    	if response:
    		print(response)
    	else:
    		print('ERROR!NO RESPONSE!')

def telegram_bot_pre_img(tg_bot_token, tg_pic, tg_brief,preview_img_list,tg_user_id = '',token=''):
    """
    telegram bot 消息推送
    :param tg_bot_token:
    :param tg_user_id:
    :param title:
    :param content:
    :return:
    """
    try:
    	
        print('正在使用 telegram机器人 推送 pre IMG 消息...', end='')
	        # headers = {'Accept':'*/*','Accept-Encoding':'gzip,deflate','Accept-Laguage':'zh-Hans-CN;q=1 en-US;q=0.9, zh-Hant-CN;q=0.8','Connection':'close','Content-Type':'application/json'}
        headers = {"Accept": "*/*","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-Hans-CN;q=1, en-US;q=0.9, zh-Hant-CN;q=0.8","Connection": "close","Content-Type": "application/json"}
        
        data_list =[]
        n = 0
        for i in preview_img_list:
        	n += 1
        	p = {
        						'type':'photo',
				            	'media':i,
				            	'caption':token
        	}
        	data_list.append(p)
        	if n  == 10:
        		print(n,'preview IMGS')
        		break
        # print(len(data_list))
        media_data = {
        	'chat_id': tg_user_id,
        	'media':data_list,
            # 'video':preview_video,
            'caption':token + ' Preview'
            }
        response = requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMediaGroup', data = json.dumps(media_data), headers=headers, timeout=15).json()
        # print(response)
        if response['ok']:
            print('Preview IMG 推送成功！')
        else:
            print('Preview IMG 推送失败！')
    except:
    	print(f'\n[⚠ Preview IMG 异常！推送错误]')
    	print('ERROR!NO RESPONSE!')


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


def parse_all_star_page(Collection_page):
	"""get actor detail page url"""
	# print(f'{print_time()}in FN parse_all_star_page')
	actor_list,real_star_name_list = [],[]
	if Collection_page == 1:
		actresse_doc = try_get("https://www.javbus.com/actresses").text
	else:
		actresse_doc = try_get("https://www.javbus.com/actresses/" + str(Collection_page)).text
	actresse_soup = BeautifulSoup(actresse_doc,'lxml')
	actresse_page_link_tag = actresse_soup('a',class_= 'avatar-box text-center')
	real_star_name_tag = actresse_soup('div',class_= 'photo-info')
	for x in real_star_name_tag:
		real_star_name = x.get_text().strip()
		real_star_name_list.append(real_star_name)
	for actor in actresse_page_link_tag:
		actor_page_link = actor.get('href')
		actor_list.append(actor_page_link)
	return actor_list,real_star_name_list
def get_star_av_url_list(real_star_name,star_av_url):
	# print('in FN get_star_av_url_list')
	print(f'{print_time()}演员 {real_star_name} 请就位.\n个人作品页：{star_av_url}\n')
	time.sleep(0.5)
	star_headers = {'user-agent':UA,'referer':'https://www.javbus.com/actresses'}
	actor_page = try_get(star_av_url,star_headers).text
	
	# 存放电影详情页链接
	av_url_list = []

	soup = BeautifulSoup(actor_page,'lxml')
	# print(soup.prettify())
	movie = soup('a',class_="movie-box")
	next_page = soup('a',id='next')
	page_num = 1
	if next_page:
		for x in range(100):
			page_num += 1
			next_page_url = 'https://www.javbus.com' + next_page[0].get('href')
			# print(next_page_url)
			r = try_get(next_page_url,star_headers).text
			next_soup = BeautifulSoup(r,'lxml')
			for i in movie:
				# print(i['href'])
				av_url_list.append(i['href'])
			next_page = next_soup('a',id='next')
			time.sleep(1.1)
			if not next_page:
				break
	print(f'Done for star-{real_star_name} Collection\n(Total:{len(av_url_list)}) movie page url.\nStar Collection detail page url:{star_av_url}\n')
	return av_url_list
def get_av_preview(token):
	# print(f'{print_time()}in FN get_av_preview')
	# get avgle prev
	# print('\ntoken is :',token)
	query = token
	page = 0
	limit = 2
	AVGLE_SEARCH_JAV_API_URL = 'https://api.avgle.com/v1/jav/{}/{}?limit={}'
	try:
		response = json.loads(urllib.request.urlopen(AVGLE_SEARCH_JAV_API_URL.format(urllib.parse.quote_plus(query), page, limit)).read().decode())
		# print(f'response is \n {response} \n')
	except:
		print("\n\t\t\t\tIN get_av_preview Max retries exceeded.\n \t\t\t\tTERMINATE 10s")
		time.sleep(10)
		print('ERROR IN GET PREVIEW ')
	try:
		if response['success']:
		    has_video = response['response']['videos']
		    if has_video:
		    	for video in has_video:
		    		video_title = video['title']
		    		video_avgle_url = video['video_url']
		    		condi = video_title + video_avgle_url
			    	if token in condi:
			    		preview_video_url = video['preview_video_url']
			    	else:
			    		print(f'{print_time()}{token} has not preview_video_url')
			    	if preview_video_url:
			    		# av_info_dict['preview_video_url'] = preview_video_url
			    		print(preview_video_url)
			    		print(f'\n{print_time()} 预览视频获取成功.\n')
			    		return preview_video_url
			    	else:
			    		print(f'{print_time()}{token} has not preview_video_url')
		else:
			print(f'{print_time()}{token} has not preview_video_url')
	except:
		print(f'\n\n{print_time()}TRY ERROR IN get_av_preview\n')
def get_av_info(star_name,page_soup):
	# av_url_list all movies of one star
	# 循环获取每部作品 简介信息
	movie_msg = {}
	#获取作品简介 演员 识别码 发行商 导演 发行时间
	big_img = page_soup.find('a',class_='bigImage')
	if big_img:
		big_img_url = big_img['href']
	else:
		big_img_url = '404'
	print(f"{print_time()}big image url is: ",big_img_url)
	movie_msg['POST'] = big_img_url
	content = page_soup.find_all('div',class_='col-md-3 info')[0].get_text().split('\n')
	genre = page_soup.find('p',text='類別:').next_sibling.next_sibling.get_text().replace('\n','b#')[1:-1]
	titles = page_soup('div',class_='container')[0].find('h3').text
	movie_msg['title'] = titles
	genre = 'b#' + genre
	genre = genre.replace('b',' ')
	movie_msg['類別'] = genre
	preview_img = page_soup('a',class_='sample-box')
	preview_img_list = []
	for i in preview_img:
		preview_img_list.append(i['href'])
		movie_msg['preview_img_list'] = preview_img_list
	for x in content:
		x.replace(' ','')
		if ":" in x and x:
			a,b = x.split(':')
			if b:
				movie_msg[a]=b
	time.sleep(0.3)
	# 获取类别
	return movie_msg
def tg_data(dict_of_av):
	tg_brief = ''
	for key,value in dict.items(dict_of_av):
		# print(key,value)
		if key == 'preview_video_url' or key == 'POST' or key == 'preview_img_list':
			continue
		if key != 'magnet_urls':
			tg_brief += key + ': ' + value + '\n'
		else:
			if value:
				if len(value) > 2:
					tg_brief += '磁力信息： ' + value[0][2] + '\n' + value[0][1] + '\n' + value[1][2] + '\n' + value[1][1] + '\n' + value[2][2] + '\n' + value[2][1]
				else:
					tg_brief += '磁力信息： ' + value[0][2] + '\n' + value[0][1]
	post = dict_of_av['POST']
	return tg_brief,post

	# if key 
def get_magnet(star_av_url,page_soup):
	""" Get all magnet of one star and RETURN list"""
	all_magnet_list = []
	magnet_referer = star_av_url
	magnet_headers = {'user-agent':UA,'referer':magnet_referer}
	# 抓取磁力链接
	# 从网页源代码获取gid,uc,img的值 拼接
	magnet_need = page_soup('script')[8].string.replace(' ','').replace('\r','=').replace('\'','').replace(';','').replace('\n','').replace('\t','').strip()[1:].split('=')
	# print(magnet_need)
	gid = magnet_need[1]
	uc = magnet_need[3]
	img = magnet_need[5]
	magnet_ajax_url = f'https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid={gid}&lang=zh&img={img}&uc={uc}'
	magnet_r = try_get(magnet_ajax_url,magnet_headers)
	if magnet_r:
		magnet_r = magnet_r.text
		magnet_soup = BeautifulSoup(magnet_r,'lxml')
		# print(magnet_soup.prettify())
		a = magnet_soup('tr')
		for o in a:#o = tr
			magnet_list = []
			magnet_title = o.contents[1].get_text().strip()
			magnet_size = o.contents[3].get_text().strip()
			magnet_year = o.contents[5].get_text().strip()
			# print(magnet_title,magnet_size,magnet_year)
			# size,year,title 待精准匹配磁力
			magnet_url = o.contents[1].get('onclick')[13:-10]
			magnet_list.append(magnet_size)
			magnet_list.append(magnet_year)
			magnet_list.append(magnet_url)
			all_magnet_list.append(magnet_list)
			# print(magnet_list)
			time.sleep(1)
			return all_magnet_list
	else:
		return 0
def count_down(secs):
	'''Counting down for ses second
	   like 倒计时中-sec.
	  ：param secs:
	  '''
	while secs >= 0:
		print(f'----------------倒计时中----------------\n---------------------{secs}---------------------')
		secs -= 1
		time.sleep(1)
def save(star_movies):
	#存放本地
	b_save = time.time()
	with open('javbus.json','w',encoding='utf-8') as f:
		json.dump(star_movies,f)
	save_cost_time = time.time() -a_save
	print(f'Save file cost time {save_cost_time}.')
def count_single_star_cost_time(start_time):
	single_star_crawled_time = time.time()
	single_star_cost_time = single_star_crawled_time - start_time
	print(f'{print_time()}one_star_cost_time: {single_star_cost_time}')
	# print(f'Star {star_name} has all crawled.\n Cost time:{single_star_cost_time}')

def main():
	# t = print_time()
	print(f'{print_time()} Crawler START.')	

	# All star avs
	# all_star_avs = 
	#存放所有 单个star所有影片. 字典
	# eg:{'okq':[{'ssni':{'post_url':url,'title':,'magnet_urls':}}]}
	#列表：[{'ssni':{'post_url':url,'title':,'magnet_urls':}},]
	star_movies = {}
	# 存放所有av_dict
	all_av_info_list = []
	# 存放单部影片番号对应信息 eg:{'ssni':{'post_url':url,'title':,'magnet_urls':}}
	av_dict = {}
	# 存放av info
	av_info_dict = {}

	# 获取 一定页数的star COLLECTION  URL 
	star_collection_url_list = []
	real_star_name_list =[]
	start_time = time.time()
	token_list=[]
	Duplicate_tokens = []

	specified_nums = [i*10 for i in range(1,31,3)]
	for n in range(1,2):
		star_collection_url_list.extend(parse_all_star_page(n)[0])
		real_star_name_list.extend(parse_all_star_page(n)[1])
	
	star_name_index = 2  #int(input("START FROM WHICH STAR:")) - 1
	# get each av url in star collection list

	for x in star_collection_url_list[star_name_index:]: # START FROM NO ? STAR IN ACTRESSES PAGE
		real_star_name = real_star_name_list[star_name_index]
		star_name_index += 1
		
		star_name = x.split('/')[-1]
		print(star_name)
		main_av_url_list = get_star_av_url_list(real_star_name,x)
		len_of_av_url_list = len(main_av_url_list)
		star_schedule = f'{star_name_index}@{len_of_av_url_list}'
		nums_of_av = 1 # 统计实时获取的av序数
		# get each av info  演员 识别码 发行商 导演 发行时间 系列 关键词
		for star_av_url in main_av_url_list:
			av_schedule = f'{nums_of_av}v{len_of_av_url_list}'
			token = star_av_url.split('/')[-1]
			
			av_page_headers = {'user-agent':UA,'referer':f'https://www.javbus.com/star/{star_name}/' + str(random.choice(range(1,5)))}
			r = try_get(star_av_url,av_page_headers).text
			page_soup = BeautifulSoup(r,'lxml')
			# t = print_time()
			print(f'{print_time()}No.{nums_of_av}\n\t\t\t\t\t\t\tCurrent schedule:{av_schedule} movie BY {real_star_name} {star_name}, url : {star_av_url}')
			av_info_dict = get_av_info(star_name,page_soup)
			nums_of_av += 1
			# t = print_time()
			print(f'{print_time()} 影片简介获取完毕.')
			av_info_dict['magnet_urls'] = get_magnet(star_av_url,page_soup)
			print(f'{print_time()} 磁力信息获取完毕.')
			prev_video_url = get_av_preview(token)
			av_info_dict['preview_video_url'] = prev_video_url
			av_dict[token] = av_info_dict
			all_av_info_list.append(av_dict)
			# print(av_info_dict)
			# TG 推送
			tg_bot_token = ''
			tg_user_id = ''
			tg_brief,post = tg_data(av_info_dict)
			tg_brief = '#' + real_star_name + '\n' + tg_brief
			tg_brief = tg_brief.replace('title:','')
			
			if token not in token_list:
				# tg_brief = '識別碼: ' + av_info_dict['識別碼'] + '\n發行日期: ' + av_info_dict['發行日期'] + '\n長度: '  + av_info_dict['長度'] + '\n系列: ' + av_info_dict[' 系列'] + '\n導演: ' + av_info_dict['導演'] + '\n製作商: ' +  av_info_dict['製作商'] + '\n發行商: ' + av_info_dict['發行商'] + '\n磁力信息： ' + str(av_info_dict['magnet'][0]) + '\n' + str(av_info_dict['magnet'][1])
				if av_info_dict.__contains__('preview_img_list'):
					if av_info_dict.__contains__('preview_video_url'):
						preview_video = av_info_dict['preview_video_url']
					else:
						preview_video = ''
					preview_img = av_info_dict['preview_img_list']
					telegram_bot(tg_bot_token,post,tg_brief,tg_user_id,preview_video,token)
					telegram_bot_pre_img(tg_bot_token,post,tg_brief,preview_img,tg_user_id = tg_user_id,token=token)

				else:
					telegram_bot(tg_bot_token,post,tg_brief,tg_user_id,token=token)
			else:
				Duplicate_tokens.append(token)
				print('Duplicate FOUNDED!!!-------Duplicate FOUNDED!!!-------Duplicate FOUNDED!!!-------')
				print(f'NOW HAS {len(Duplicate_tokens)} Duplicate_tokens \n {Duplicate_tokens}')
			print(f'{real_star_name} ADDED {len(token_list)} work now.')
			random_num = random.choice([5,2,7,3,1])
			time.sleep(random_num)
			token_list.append(token)


			#bark推送
			bark_time = (time.time() - start_time)/60
			bark_time = '%.2f' %bark_time
			bark_title = f'Star {real_star_name}({star_schedule}) Crawler working...'
			bark_content = f"{print_time()}Schedule:{av_schedule}\nCost_time:{bark_time}M."
			
			if nums_of_av in specified_nums:
				bark(bark_title,bark_content)
			# for test
			b_save_one_time = time.time()
			with open(real_star_name + '.txt','a',encoding='utf-8') as f:
				f.write(str(av_dict))
		token_info = f'{real_star_name} ADDED {len(token_list)} work.'
		print(token_info)
		bark(token_info,token_info)
		count_single_star_cost_time(start_time)
		print(f'{print_time()}\n\n\t\t\t{real_star_name}已经被你看光了！！!休息十秒吧！\n\n\t\t\t')
		count_down(10)
		
	star_movies[real_star_name] = all_av_info_list
	save(star_movies)
	end_time = time.time()
	all_cost_time = end_time - start_time
	print(f'{print_time()} 总耗时：{all_cost_time}秒. = {all_cost_time}/60分.\n')

if __name__ == '__main__':
	main()
