#TV.CCTV.COM/YXG
# https://tv.cctv.com/yxg/#datacid=dsj&datafl=&datadq=&fc=%E7%94%B5%E8%A7%86%E5%89%A7&datanf=&dataszm=
import hashlib
from common import *

start_date = 202010
end_date = 202013
view_date_list = list(range(start_date,end_date))
speci_date_jsurl = []
speci_info_list = []
ep_list = ['隐秘而伟大','启鱼·成语故事—古物篇','大秦赋',]
zy_list = ['今日说法','新闻周刊','动物世界','百家讲坛','远方的家','挑战不可能', '一线', '第10放映室', ]
namelist = []
namelist.extend(zy_list)
namelist.extend(ep_list)
pp(namelist)

def search(name):
    so_headers = {
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "User-Agent":UA,
    "Upgrade-Insecure-Requests": '1',

    }

    headers = {
    
    "User-Agent":UA,
    "Accept": '*/*',
    "Accept-Encoding": 'gzip, deflate, br',
    "Referer": 'https://search.cctv.com/',

    }
    so_url = f'https://search.cctv.com/search.php?qtext={quote(name)}&type=video'
    so_html = try_get(so_url,headers = so_headers)
    regx = r'<div class="search\d+_ind01">\s+<script src="(.*?)" type="text/javascript'
    js_url = re.findall(re.compile(regx),so_html.content.decode('utf-8'))
    
    # https://r.img.cctvpic.com/so/cctv/list/13/202101/p63996_202101.js?_=1611731690399
    # pp(so_html.content.decode('utf-8'))
    if js_url:
        js_url = js_url[0]
        pp(js_url)
        r = try_get(js_url,headers = headers)
        # r.encoding = 'utf-8'
        js_html = r.text
        regy =  r'title":"(.*?)","album_order_id":"\d+","targetpage":"(.*?)"'
        # regy = r'album_order_id":"\d+","targetpage":"(.*?)"'
        info = re.findall(re.compile(regy),js_html)
        
        info.reverse()
        # info = 
        # pp(info)
        if name in zy_list:
            js_split = js_url.split('?t')[0].split('/')
            pre_js = '/'.join(js_split[:-1]) + '/'
            p_num = js_url.split('/')[-1].split('.js?t')[0]
            
            for i in view_date_list:
                select_view_url = pre_js + str(i) + '/' + p_num + '_' + str(i) + '.js'
                speci_date_jsurl.append(select_view_url)
                pp('select_view_url',select_view_url)
                time.sleep(33)
                r = try_get(select_view_url,headers = headers)
                # r.encoding = 'utf-8'
                js_html = r.text
                if js_html:
                    regy =  r'title":"(.*?)","album_order_id":"\d+","targetpage":"(.*?)"'
                    # regy = r'album_order_id":"\d+","targetpage":"(.*?)"'
                    speci_info = re.findall(re.compile(regy),js_html)
                    if speci_info:
                        speci_info.reverse()
                        speci_info_list.extend(info)
                        speci_info_list.extend(speci_info)
                        speci_info_list = set(speci_info_list)
                        speci_info_list = list(speci_info_list)
                        return speci_info_list

        return info
        


def get_videoGuid(url):
    # url = "http://tv.cctv.com/2018/06/16/VIDEjxPlWJL10pNgwYSjZtHW180616.shtml"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-cn",
        "Referer": "http://tv.cctv.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1",
    }

    r = try_get(url,headers=headers)
    html = r.content.decode('utf-8')
    regx = 'guid\s*=\s*[\'"]([0-9a-f]{32})[\'"]'
    res = re.findall(re.compile(regx),html)
    if res:

        guid = res[0]
        pp('guid',guid,sep=':')
        res = get_dlink(guid)
        pp('Current video url: ',url)
        # pp(res)
        return res
    else:
        pp('guid 404')
        return 0



def get_dlink(guid):
    first_date = datetime.datetime(1970, 1, 1)
    time_since = datetime.datetime.now() - first_date
    seconds = str(time_since.total_seconds()).split('.')[0]
    # pp(seconds)
    vdn_tsp = seconds
    vdn_vn = "2049"
    vdn_vc = ""
    staticCheck = "47899B86370B879139C08EA3B5E88267"
    vdn_uid = ""
    vdn_wlan = ""
    dataUrl = "http://vdn.apps.cntv.cn/api/getIpadVideoInfo.do?pid=" + guid + "&tai=ipad&from=html5"
    md5_data = vdn_tsp + vdn_vn + staticCheck + vdn_uid
    hl = hashlib.md5()
    hl.update(md5_data.encode(encoding='utf-8'))
    vdn_vc = md5_data.upper()
    dataUrl += "&tsp=" + vdn_tsp + "&vn=" + vdn_vn + "&vc=" + vdn_vc + "&uid=" + vdn_uid + "&wlan=" + vdn_wlan
    r= try_get(dataUrl)
    js = r.content.decode('utf-8')
    # pp('js is:',js)
    regx = '\{.+\}'
    e = re.findall(re.compile(regx),js)
    if e:
        dict_data = json.loads(e[0])
        # pp(dict_data)
        hls_url = dict_data['hls_url']
        # pp(hls_url)
        time.sleep(1)
        prefix = hls_url.split('/')[0:3]
        prefix = '/'.join(prefix)
        # pp('prefix is:',prefix)
        resp = try_get(hls_url)
        if resp:
            r_html = resp.content.decode('utf-8')
        else:
            r_html = 0
        if r_html:

            # pp('hls_url-html is',r_html)
            m_quality = re.findall(re.compile(r'(BANDWIDTH=[^/]+[\S]+)'),r_html)
            pp('m_quality is:',m_quality)
            time.sleep(3)
            menus = []
            urls = []# menuItems = { menus: [], urls: [] }

            for quality in m_quality:
                regx = r'BANDWIDTH=([\d]+)(.+RESOLUTION=([\S]+))?[^/]+?([\S]+)'
                m = re.findall(re.compile(regx),quality)[0]
                # pp(m)
                # resolution = m[2] + "-" + str(int(int(m[0]) / 1024)) + " kbps"
                resolution = str(int(int(m[0]) / 1024))
                dlink = prefix + m[3]
                
                
                menus.append(resolution)
                urls.append(dlink)
            # pp(resolution,'\n',dlink)
            return (resolution,dlink)
        else:
            return 0
with open('ctv.m3u','a',encoding='utf-8') as f:
    f.write('#EXTM3U')

for i in namelist:
    pp('当前节目：',i)
    
    data = search(i)
    if data:
        pp(f'-------{i}-------------Total:{len(data)}.---------------------')
        for x in data:
            t = unquote(x[0])
            if i in t:
	            title = t.replace(i,'')
            if '《' in t:
	            title = t.replace('《','')
            if '》' in t:
	            title = t.replace('》','')
            pp(i,'   ----   ',t)
            result = get_videoGuid(x[1])
            if result:
                res,dlink = result 
                pp(res,dlink)
                pp(f'-------{i}-------------Total:{len(data)}.---------------------')
                res.replace(' ','')
                if int(res) <1000:
                    pp('\n\n\n------', res  + " kbps-------\n\n\n\n")
                    time.sleep(3)
                time.sleep(1)
                msg = f"\n#EXTINF:-1 group-title=\"{i} {res}kbps\",{title}\n{dlink}"
                with open('ctv.m3u','a',encoding='utf-8') as f:
	                f.write(msg)
    else:
    	pp(f'{i} has no data!')
    pp('\n\n\n',i,'over，rest for 10 secs\n\n\n')
    time.sleep(10)
