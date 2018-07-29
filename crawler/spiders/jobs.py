# -*- coding: utf-8 -*-
import scrapy
from urls import career_urls


class JobItem(scrapy.Item):
    url = scrapy.Field()
    posting = scrapy.Field()
    noposting = scrapy.Field()

    
class JobsSpider(scrapy.Spider):
    name = 'jobs'

    def start_requests(self,):
##        career_urls=['https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab']
        
        for url in career_urls:
            template='https://postinglist.herokuapp.com/?url={}'
            req_url=template.format(url.strip())
            #print(req_url)        
            yield scrapy.Request(req_url,self.parse,meta={"url":url})
            #break
        

    def parse(self, response):
        
        item = JobItem()
        item["url"]=response.url
        item["posting"]=[]
        item["noposting"]=[]

        mayjobsection=response.xpath('//*[@class="MayPosting"]/table/tr')
        for sec in mayjobsection:
            text=sec.xpath('./td//text()').extract()
            strip_text=[x.strip() for x in text if x.strip()]
            item["posting"].append(strip_text)

        mayjobsection=response.xpath('//*[@class="MayNotPosting"]/table/tr')
        for sec in mayjobsection:
            text=sec.xpath('./td//text()').extract()
            strip_text=[x.strip() for x in text if x.strip()]
            item["noposting"].append(strip_text)
        yield item

            
