import requests
from lxml import etree
import time
import json


class DouBan:
    # 判断是否有过实例化的东西
    _instance = None

    def __init__(self, page=1):
        # 保存用的容器
        self.content = []
        self.page = page
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }

    def __new__(cls, *args, **kwargs):
        # 如果_instance 为空则证明是第一次创建实例
        if cls._instance is None:
            # 通过父类的 __new__(cls)创建实例
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            # 返回上一个对象的引用
            return cls._instance

    def get_html(self, page):
        """
        获取指定页数的html代码
        :param page:
        :return:
        """
        res = requests.get(
            f'https://movie.douban.com/top250?start={25*(page - 1)}&filter=',
            headers=self.headers)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            html = etree.HTML(res.text)
            return html
        else:
            print(f"可能遇到了 {res.status_code} 错误")
            return 0

    def parse_html(self, html):
        """
        分析页面
        :param html:
        :return:
        """
        if html != 0:
            nameList = html.xpath('//div[@class="hd"]/a/span[position()=1]')
            authorList = html.xpath('//div[@class="bd"]/p[position()=1]')
            rates = html.xpath('//span[@class="rating_num"]')
            rateNums = html.xpath('//div[@class="star"]/span[position()=4]')
            inqs = html.xpath('//span[@class="inq"]')
            for name, author, rate, rate_num, inq in zip(
                    nameList, authorList, rates, rateNums, inqs):
                content = {
                    'name': name.text,
                    'doctor': author.text.strip().replace('\xa0', ''),
                    'rate': rate.text,
                    'rate_num': rate_num.text,
                    'inq': inq.text
                }
                self.content.append(content)
        else:
            print("网页返回值格式有错误")

    def get_all_info(self):
        """
        获取所有的信息
        :return:
        """
        for page in range(1, 11):
            html = self.get_html(page)
            self.parse_html(html)
            print(f"获取 {page} 页的数据完毕,程序休眠三秒...")
            time.sleep(3)

    def get_choice_info(self):
        """
        获取指定页数的信息,默认第一页
        :return:
        """
        html = self.get_html(self.page)
        self.parse_html(html)

    def save(self):
        """
        保存查到的数据到本地提供给后续使用
        :return:
        """
        with open('data.json', 'w') as f:
            json.dump(self.content, f)
        print("保存数据到本地完毕...")


if __name__ == '__main__':
    # db = DouBan()
    # db.get_choice_info()
    # db.get_all_info()
    # db.save()
    with open('data.json', 'r') as f:
        data = json.load(f)

    print(len(data))


