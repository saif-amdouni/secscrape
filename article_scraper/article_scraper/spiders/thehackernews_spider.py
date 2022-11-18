import scrapy
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
from article_scraper.items import hackerNewsItem

class newsSpider(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.BackupFolder = "DataBackup"
        
        if not os.path.exists(self.BackupFolder):
            os.makedirs(self.BackupFolder)
    name = "thehackernews"
    
    def start_requests(self):
        urls = [
            'https://thehackernews.com/search/label/data breach',
            'https://thehackernews.com/search/label/Cyber Attack',
            'https://thehackernews.com/search/label/Vulnerability',
            'https://thehackernews.com/search/label/Malware'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_name = response.url.split("/")[-1].split("?")[0]
        filename = f'news-{page_name}.csv'
        if os.path.isfile(os.path.join(self.BackupFolder,filename)):
            df=pd.read_csv(os.path.join(self.BackupFolder,filename),sep='\t')
        else:
            df = pd.DataFrame(columns=["title","date","link"])

        for article in response.xpath("//div[@class='body-post clear']"):
            item = self.extractObject(article,page_name)
            df = df.append({"title" : item["title"],"date" : item["date"],"link" : item["link"]},ignore_index=True)
            yield item
        # update csv
        df.to_csv(os.path.join(self.BackupFolder,filename),index=False,sep='\t')
        self.log(f'Saved file {filename}')
        # go to next page
        try :
            next_page = response.xpath("//div[@class='blog-pager clear']/span[@id='blog-pager-older-link']/a[@class='blog-pager-older-link-mobile']/@href").extract()[0]
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
        except IndexError as e :
            print("no more pages to crawl !")

    def extractObject(self,article,alertType):
        item = hackerNewsItem()
        link = article.xpath("a[@class='story-link']/@href").extract()[0]
        info = article.xpath("a/div[@class='clear home-post-box cf']/div[@class='clear home-right']")
        title = info.xpath("h2[@class='home-title']/text()").extract()[0]
        date = info.xpath("div[@class='item-label']/text()").extract()[0]
        
        item['alertType'] = alertType
        item['link'] = link
        item['title'] = title
        item['date'] = date
        return item