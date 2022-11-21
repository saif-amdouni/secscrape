import scrapy
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

from article_scraper.items import securityweekItem

class securityweekSpider(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.BackupFolder = "DataBackup"

        
        if not os.path.exists(self.BackupFolder):
            os.makedirs(self.BackupFolder)
    name = "securityweek"

    def start_requests(self):
        urls = [
            'https://www.securityweek.com/virus-threats/email-security',
            'https://www.securityweek.com/virus-threats/vulnerabilities',
            'https://www.securityweek.com/virus-threats/virus-malware',
            'https://www.securityweek.com/cybercrime/fraud-identity-theft',
            'https://www.securityweek.com/cybercrime/phishing',
            'https://www.securityweek.com/cybercrime/cyberwarfare',
            'https://www.securityweek.com/cybercrime/malware',
            'https://www.securityweek.com/mobile-wireless/mobile-security',
            'https://www.securityweek.com/mobile-wireless/wireless-security',
            'https://www.securityweek.com/security-infrastructure/cloud-security',
            'https://www.securityweek.com/security-infrastructure/identity-access',
            'https://www.securityweek.com/security-infrastructure/data-protection',
            'https://www.securityweek.com/security-infrastructure/network-security',
            'https://www.securityweek.com/security-infrastructure/application-security'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_name = response.url.split("/")[-2] + ' ' + response.url.split("/")[-1].split("?")[0]
        print(page_name)
        filename = f'securityweek-{page_name}.csv'
        if os.path.isfile(os.path.join(self.BackupFolder,filename)):
            df=pd.read_csv(os.path.join(self.BackupFolder,filename),sep='\t')
        else:
            df = pd.DataFrame(columns=["title","date","link"])
        articls = response.xpath("//div[@class='panel-pane pane-block pane-views-recent-user-story-block-1']//div[@class='view-content']/div")
        
        for article in articls:
            item = self.extractObject(article,page_name)
            # print(item)
            df = df.append({"title" : item["title"], "author" : item["author"], 'link':item["link"]},ignore_index=True)
            yield item
        # update csv
        df.to_csv(os.path.join(self.BackupFolder,filename),index=False,sep='\t')
        # self.log(f'Saved file {filename}')
        # # go to next page
        try :
            next_page = response.xpath("//div[@class='panel-pane pane-block pane-views-recent-user-story-block-1']/div[@class='pane-content']//li[@class='pager-next last']/a/@href").extract()[0]
            # print(next_page)
            if next_page is not None:
                yield scrapy.Request("https://www.securityweek.com"+next_page, callback=self.parse)
        except IndexError as e :
            print("no more pages to crawl !")
    
    def extractObject(self,article,alertType):
        item = securityweekItem()
        link = article.xpath("div[@class='views-field-title']//a/@href").extract()[0]
        title = article.xpath("div[@class='views-field-title']//a/text()").extract()[0]
        author = article.xpath("div[@class='views-field-tid']//a[@class='username']/text()").extract()[0]

        
        
        item['alertType'] = alertType
        item['link'] = "https://www.securityweek.com/"+link
        item['title'] = title
        item['author'] = author
        return item
            