import scrapy
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

class newsSpider(scrapy.Spider):
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
        if os.path.isfile(filename):
            df=pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["title","date","link"])

        for article in response.xpath("//div[@class='body-post clear']"):
            link = article.xpath("a[@class='story-link']/@href").extract()[0]
            
            info = article.xpath("a/div[@class='clear home-post-box cf']/div[@class='clear home-right']")
            title = info.xpath("h2[@class='home-title']/text()").extract()[0]
            date = info.xpath("div[@class='item-label']/text()").extract()[0]
            df = df.append({"title" : title,"date" : date,"link" : link},ignore_index=True)
        df.to_csv(filename,index=False,sep='\t')
        self.log(f'Saved file {filename}')
        try :
            next_page = response.xpath("//div[@class='blog-pager clear']/span[@id='blog-pager-older-link']/a[@class='blog-pager-older-link-mobile']/@href").extract()[0]
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
        except IndexError as e :
            print("no more pages to crawl !")
    