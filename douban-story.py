# 豆瓣小说排行爬取
import requests
from lxml import etree
import json


class DouBan:
    def __init__(self):
        self.url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/67.0.3396.99 Safari/537.36"}

    def parse_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_shuju(self,html_str):
        element = etree.HTML(html_str)
        ret1 = element.xpath("//li[@class='subject-item']")
        with open("douban_story.txt", "a", encoding="utf-8") as f:
            for content in ret1:
                story_dict = {}
                story_dict["书名"] = content.xpath(".//div[@class='info']/h2/a/text()")[0].strip()
                story_dict["封面图片"] = content.xpath(".//a[@class='nbg']/img/@src")[0]
                story_dict["作者"] = content.xpath(".//div[@class='pub']/text()")[0].split("/")[0].strip()
                story_dict["出版社"] = content.xpath(".//div[@class='pub']/text()")[0].split("/")[-3].strip()
                story_dict["出版时间"] = content.xpath(".//div[@class='pub']/text()")[0].split("/")[-2].strip()
                story_dict["售价"] = content.xpath(".//div[@class='pub']/text()")[0].split("/")[-1].strip()
                story_dict["评价人数"] = content.xpath(".//span[@class='pl']/text()")[0].strip()
                story_dict["评价人数"] = story_dict["评价人数"] if len(story_dict["评价人数"]) >0 else None
                story_dict["评分"] = content.xpath(".//span[@class='rating_nums']/text()")[0]
                # print(story_dict["售价"])
                f.write(json.dumps(story_dict, ensure_ascii=False))
                f.write("\n")

    def run(self):
        num = 0
        while num<110:
            url = self.url.format(num)
            html_str = self.parse_url(url)
            self.get_shuju(html_str)
            num += 20


if __name__ == '__main__':
    douban = DouBan()
    douban.run()
