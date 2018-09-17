# 将夜小说爬取
# 未使用多线程爬取，得花费时间许多
import requests
from lxml import etree
import json


class JiangYe:
    def __init__(self):
        self.url = "https://www.zhuaji.org/read/848/{}.html"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                        " AppleWebKit/537.36 (KHTML, like Gecko)"
                        " Chrome/67.0.3396.99 Safari/537.36"}

    def parse_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode("gbk")

    def get_shuju(self,html_str):
        element = etree.HTML(html_str)
        with open("《将夜》全文爬取(排版就这样，已经尽力了).txt", "a", encoding="utf-8") as f:
            dict = {}
            dict["章节"]= element.xpath("//div[@class='title']/h1/text()")
            print(dict["章节"])
            response_list = element.xpath("//div[@id='content']/text()")
            a_list = response_list[-1][0:-25]
            response_list[-1] = a_list
            dict["正文"] = response_list
            f.write(json.dumps(dict,ensure_ascii=False, indent=2))
            f.write("\n")

    def run(self):
        num = 342745
        sum = 1
        while num < 343874:
            url = self.url.format(num)
            html_str = self.parse_url(url)
            # print(html_str)
            self.get_shuju(html_str)
            print("成功爬取第{}章".format(sum))
            num += 1
            sum += 1
        print("爬取完成")


if __name__ == '__main__':
    jiangye = JiangYe()
    jiangye.run()
