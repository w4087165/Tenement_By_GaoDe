import requests
import re
import base64
from fontTools.ttLib import TTFont
from tools.UserAgent import USERAGENT_LIST
from time import sleep
import random
from lxml import etree
import pymysql

class five_eight:
    def __init__(self):
        self.dict = {}
        self.page = 0
        self.numbers = 0
        self.init_url = "https://bj.58.com/chuzu/"

        self.header = {
            "Accept": "text/html",
            "Referer": "",
            "Cookie": "f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; userid360_xml=83BC9320CEEB5E8BFEE1ADEBF939971F; time_create=1565148056280; id58=e87rZl0itmsKJ9mAA8SKAg==; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; city=bj; 58home=bj; 58tj_uuid=363461fd-14a8-4cd6-bf26-6a279fb42b84; new_session=0; new_uv=1; utm_source=; spm=; init_refer=; als=0; xxzl_deviceid=oa5vl60lIZlrEFC8ZvN564VHOoNXCCj2q3UCBNLKrz8VaXJXMBPETx1FRHK7rEua",
            "User-Agent": random.choice(USERAGENT_LIST),
        }

        self.db = pymysql.connect('localhost', 'root', '123456', 'House_db', charset='utf8')
        self.cursor = self.db.cursor()
    # 功能函数 1 获取页面信息
    def get_html(self, url):
        self.header['User-Agent'] = random.choice(USERAGENT_LIST)
        # ua = UserAgent()
        # header = {"User-Agent": ua.random}
        res = requests.get(url=url, headers=self.header)
        res.encoding = 'utf-8'
        html = res.text
        return html

    # 功能函数 2 xpath解析函数
    def parse_func(self, html, x_dbs):
        pattern = etree.HTML(html)
        r_list = pattern.xpath(x_dbs)
        return r_list

    # 功能函数 3 正则解析函数
    def re_func(self, re_dbs, html):
        pattern = re.compile(re_dbs, re.S | re.M)
        re_list = pattern.findall(html)
        return re_list

    def get_locat(self, re_dbs, second_url):
        locat = {}
        second_html = self.get_html(second_url)
        a_list = self.re_func(re_dbs, second_html)
        # locat['lon:'] = a_list[0][1].strip()
        # locat['lat:'] = a_list[0][0].strip()
        return a_list

    def convert_money(self, s):
        console = ''
        strs = {'&#x9476': 38006, '&#x958f': 38287, '&#x993c': 39228, '&#x9a4b': 39499, '&#x9e3a': 40506,
                '&#x9ea3': 40611, '&#x9f64': 40804, '&#x9f92': 40850, '&#x9fa4': 40868, '&#x9fa5': 40869}
        con_s = s.split(';')
        con_s = con_s[:-1]
        for i in con_s:
            temp = int(self.dict[strs[i]][-2:]) - 1
            console += str(temp)
        if console != '':
            return int(console)
        else:
            print("钱为空")

    def convert_title_room(self, s):
        strs = ['&#x9476;', '&#x958f;', '&#x993c;', '&#x9a4b;', '&#x9e3a;', '&#x9ea3;', '&#x9f64;', '&#x9f92;',
                '&#x9fa4;',
                '&#x9fa5;']
        nums = {'&#x9476;': 38006, '&#x958f;': 38287, '&#x993c;': 39228, '&#x9a4b;': 39499, '&#x9e3a;': 40506,
                '&#x9ea3;': 40611, '&#x9f64;': 40804, '&#x9f92;': 40850, '&#x9fa4;': 40868, '&#x9fa5;': 40869}
        for str_c in strs:
            beg = s.find(str_c)
            if beg != -1:
                temp = str(int(self.dict[nums[str_c]][-2:]) - 1)
                s = s.replace(str_c, temp)
            else:
                continue
        return s

    def onePage(self):

        param = 'pn' + str(self.page) + '/'
        self.header["Referer"] = self.init_url + param
        res = requests.get(self.init_url, headers=self.header)
        res_html = res.text

        # title_pattern = r'target="_blank"  rel="nofollow" >(.*?)</a>'
        title_pattern = '//ul//li//h2/a/text()'
        url_pattern = r'lazy_src="(.*?)"'
        room_pattern = r'<p class="room">(.*?)</p>'
        money_pattern = r'<b class="strongbox">(.*?)</b>'
        font_pattern = r"base64,(.*?)format"

        # titles = re.findall(title_pattern, res_html, re.S | re.M)
        titles = self.parse_func(res_html,title_pattern)
        urls = re.findall(url_pattern, res_html, re.S | re.M)
        rooms = re.findall(room_pattern, res_html, re.S | re.M)
        moneys = re.findall(money_pattern, res_html, re.S | re.M)
        font_base64 = re.findall(font_pattern, res_html, re.S | re.M)

        titles = [c.replace('\n', '') for c in titles]
        titles = [c.replace(' ', '') for c in titles]
        # urls = [c.replace('//', 'https://') for c in urls]
        rooms = [c.replace(' ', '') for c in rooms]
        rooms = [c.replace('&nbsp;', '') for c in rooms]
        xpath = '/html/body/div/div/ul/li/div/h2/a/@href'
        hf_list = self.parse_func(res_html, xpath)

        # 解码数字
        str_base64 = font_base64[0][:-3]
        bin_data = base64.decodebytes(str_base64.encode())
        with open("font.woff", r"wb") as f:
            f.write(bin_data)
        onlineFonts = TTFont('font.woff')
        self.dict = onlineFonts.getBestCmap()
        # 数字解决
        for i in range(len(titles)):
            titles[i] = self.convert_title_room(titles[i])
        for i in range(len(rooms)):
            rooms[i] = self.convert_title_room(rooms[i])
        for i in range(len(moneys)):
            moneys[i] = self.convert_money(moneys[i])

        # 内容输出
        print("\033[31m[INFO]第{}页开始\033[0m".format(self.page + 1))
        # print(titles)
        for i in range(len(titles)):
            item = {}
            try:
                item['house_name'] =titles[i].split('|')[1]
            except Exception as e:
                print(titles[i])
                print('未找到房子信息')
                continue
            item['href'] = hf_list[i].split('?')[0]
            item['message'] = "{}———{}".format(titles[i], rooms[i])
            item['money'] = "{}".format(moneys[i])
            re_dbs = r'"lat":(.*?),"lon":(.*?),"baidulat"'
            locat = self.get_locat(re_dbs, hf_list[i])
            item['locat'] = locat
            imgs = './static/imgs/img' + str(random.randint(1, 8)) + '.jpeg'
            print('地址是：',item['locat'])
            if not item['locat']:
                print('空')
                continue
            value = [item['house_name'], '58同城', item['message'], item['money'], item['locat'][0][1], item['locat'][0][0],
                     item['href'], imgs]
            print(value)
            try:
                ins = 'insert into LianJia_table(house_name,platform,house_message,price,lon,lat,url,images) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(ins,value)
                self.db.commit()
            except Exception as e:
                print(e)
            sleep(random.uniform(0, 1))
    def run(self):
        n = 30
        for i in range(n):
            self.page = i
            self.onePage()
        sleep(random.randint(1,3))
if __name__ == "__main__":
    fe = five_eight()
    fe.run()
