import requests
from tools.UserAgent import USERAGENT_LIST
import time
import re
import random
from lxml import etree
import pymysql

class ZiruSpider(object):
	def __init__(self):
		self.url = "http://www.ziroom.com/z/p{}/"
		self.db = pymysql.connect('localhost', 'root', '123456', 'House_db', charset='utf8')
		self.cursor = self.db.cursor()
	
	def get_headers(self):
		headers = {'User-Agent': random.choice(USERAGENT_LIST)}
		return headers
	
	# 功能函数 1 获取页面信息
	def get_html(self, url):
		# ua = UserAgent()
		# header = {"User-Agent": ua.random}
		res = requests.get(url=url, headers=self.get_headers())
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
	
	def parse_one_html(self, url):
		item = {}
		a_html = self.get_html(url)
		# 设置详情链接基准xpath
		x_dbs = '/html/body/section/div[3]/div[2]/div/div/h5/a'
		r_list = self.parse_func(a_html, x_dbs)
		for li in r_list:
			# 链接
			hf_xpath = './@href'
			href_ = li.xpath(hf_xpath)
			item['href'] = 'http:' + href_[0]
			sec_html = self.get_html('http:' + href_[0])
			# message
			info_xpath = './text()'
			room_xpath = '//html/body/section/aside/div[3]/div//dd/text()'
			room_ = self.parse_func(sec_html, room_xpath)
			
			info_ = li.xpath(info_xpath)
			# print(info_)
			item['message'] = ''.join(info_) + '-'.join(room_)
			# 价钱
			
			price_re = '<div class="Z_house_img">.*?<img src=".*?" alt="(.*?)">'
			price = self.re_func(price_re, sec_html)
			# 北京整租矩阵一期6990
			try:
				item['price'] = price[0][-11:-7]
			except:
				continue
			locat_re = '"resblockPosition":.*?[(.*?)].*?"now"'
			position = self.re_func(locat_re, sec_html)[0]
			position = position.split(':')[1]
			# [116.363332,40.088118],"now"
			post = position.split(',')
			position = [post[0][1:],post[1][:-1]]
			item['position'] = position
			item['house_name'] = item['message'].split('-')[0]
			imgs = './static/imgs/img' + str(random.randint(21, 24)) + '.jpeg'
			value = [item['house_name'],'自如租房',item['message'],item['price'],item['position'][0],item['position'][1],item['href'],imgs]
			print(value)
			try:
				ins = 'insert into LianJia_table(house_name,platform,house_message,price,lon,lat,url,images) values(%s,%s,%s,%s,%s,%s,%s,%s)'
				self.cursor.execute(ins, value)
				self.db.commit()
			except Exception as e:
				print(e)
			time.sleep(random.uniform(0, 1))

	# 入口函数
	def run(self):
		# url
		for i in range(50):
			url = self.url.format(i)
			self.parse_one_html(url)
			time.sleep(random.uniform(0, 1))

if __name__ == '__main__':
	spider = ZiruSpider()
	spider.run()
