import scrapy
import json
from ..items import CafefbotItem

BASE_URL = "https://s.cafef.vn/Ajax/CongTy/BaoCaoTaiChinh.aspx?sym="

class CafefSpider(scrapy.Spider):
    name = "cafef"

    def start_requests(self):
        urls = []
        f = open("src/kby_v1.json")
        data = json.load(f)
        for stock_info in data:
            stock_code = stock_info['c']
            urls.append("{}{}".format(BASE_URL, stock_code))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        item = CafefbotItem()
        list_pdf = response.xpath("//td/a/@href").getall()
        if len(list_pdf) >=10:
            list_pdf = list_pdf[:10]
        
        for pdf_url in list_pdf:
            item['file_urls'] = [pdf_url]
            yield item