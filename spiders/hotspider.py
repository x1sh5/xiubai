# -*- coding: utf-8 -*-
import scrapy
from xiubai.items import XiubaiItem

class HotspiderSpider(scrapy.Spider):
    name = "hotspider"
    allowed_domains = ["qiushibaike.com"]
    start_url = 'https://www.qiushibaike.com/'
    headers = {
        'Host': 'www.qiushibaike.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    cookies = {
        '_xsrf': '2|1d7214fa|ba861207793ee8edfcf6d82b91ea3ebb|1508682882',
        'Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37': '1508682893,1508684438,1508685068,1508687752',
        'Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37': '1508687752',
        '_ga': 'GA1.2.672736136.1508682896',
        '_gid': 'GA1.2.1610091210.1508682896',
        '__cur_art_index': '9301',
        '_gat': '1'
    }
    def start_requests(self):
        return [
            scrapy.Request(self.start_url,headers=self.headers,cookies=self.cookies,callback=self.parse)
        ]
    
    def parse(self, response):
        item = XiubaiItem()

        # 找到热门段子主体
        main = response.xpath('//div[@id="content-left"]/div')
        next_page = response.xpath('/html/body/div[2]/div/div[1]/ul/li[8]/a/span/text()').extract()[0]
        if next_page is not None:
            next_url = response.xpath('/html/body/div[2]/div/div[1]/ul/li[8]/a/@href').extract()[0]
            next_page_url = "https://www.qiushibaike.com" + next_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print("没有下一页了")
        for div in main:
            #段子作者
            item['author'] =div.xpath('.//h2/text()').extract()[0]
            #段子主体： 
            item['body'] = ''.join( div.xpath('a[@class="contentHerf"]/div/span[1]/text()').extract())
            #段子footer
            item['funNum']= div.xpath('.//span[@class="stats-vote"]/i/text()').extract()[0]
            item['comNum']= div.xpath('.//span[@class="stats-comments"]/a/i/text()').extract()[0]
        yield item
