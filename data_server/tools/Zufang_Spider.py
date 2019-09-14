# 链家租房
import requests
from tools.UserAgent import USERAGENT_LIST
from lxml import etree
import random
import time
import re


class LianjiaSpider(object):
    def __init__(self):
        self.url = "https://bj.lianjia.com/"

    def get_headers(self):
        headers = {'User-Agent': random.choice(USERAGENT_LIST)}
        return headers

    # 功能函数:获取页面内容
    def get_html(self, url):
        res = requests.get(url=url, headers=self.get_headers())
        res.encoding = 'utf-8'
        html = res.text
        return html

    # 功能函数:解析
    # xpath_dbs:'//div[@class="content__list--item"]/a/@href'
    def xpath_func(self, html, xpath_dbs):
        parse_obj = etree.HTML(html)
        re_list = parse_obj.xpath(xpath_dbs)
        return re_list

    # 　正则解析
    def re_func(self, re_dbs, html):
        pattern = re.compile(re_dbs, re.S)
        r_list = pattern.findall(html)
        return r_list

    def parse_html(self, url):
        item = {}
        a_html = self.get_html(url)
        # 设置基准xpath
        xpath = '//div[@class="content__list--item"]'
        li_list = self.xpath_func(a_html, xpath)
        # xpath_dbs1 = '//div[@class="content__list--item"]/a/@href'
        # xpath_dbs2 = '//div[@class="content__list--item"]//p[@class="content__list--item--title twoline"]/a/text()'
        # info_list = self.xpath_func(a_html, xpath_dbs2)
        # ['/zufang/BJ2341868613260558336.html'','','','']
        # 在这里拿到 所有房源详情链接
        # print(li_list)
        # 对房源链接发请求获取 经纬度+名字+详情链接+其他信息(价钱)
        for li in li_list:
            # 1,房源详情链接
            re_dbs1 = './a/@href'
            href = li.xpath(re_dbs1)
            second_url = self.url + href[0]
            item['url:'] = second_url
            # 2,房源信息
            re_dbs2 = './/p[@class="content__list--item--title twoline"]/a/text()'
            message = li.xpath(re_dbs2)
            item['message:'] = message[0].strip()
            # 3,价钱
            re_dbs3 = './/span/em/text()'
            price = li.xpath(re_dbs3)
            item['price'] = price[0].strip()
            # 4,房源经纬度---返回值:{'lon:': '116.192696', 'lat:': '39.921511'}
            locat = self.get_locat(second_url)
            item['locat'] = locat

            print(item)

    # 获取经纬度
    def get_locat(self, second_url):
        locat = {}
        second_html = self.get_html(second_url)
        re_dbs = "var contact = {};.*?longitude: '(.*?)'.*?latitude: '(.*?)'.*?</script>"
        a_list = self.re_func(re_dbs, second_html)
        # locat['lon:'] = a_list[0][0].strip()
        # locat['lat:'] = a_list[0][1].strip()
        a_list = [float(i) for i in a_list[0]]
        print(a_list)
        return a_list

    def run(self):
        for pg in range(1, 2):
            url = self.url + 'zufang/pg{}'.format(pg)
            self.parse_html(url)
            time.sleep(random.uniform(1, 3))


if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()
