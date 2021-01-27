import requests
import re, time
from urllib.parse import quote,unquote
import json
from bs4 import BeautifulSoup
import random,datetime


user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                       'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                       'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                       r'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                       r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                       'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1']
index = random.randint(0, 9)

UA = user_agents[index]
headers = {'User-Agent':UA}

def pp(*values,sep = ' '):
	return print(*values)
# pp(index)
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
date = print_time()[1:-2].replace('-','').split(' ')[0]
pp(date)

pp(print_time()[1:-2].replace('-','').split(' ')[0])