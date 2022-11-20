# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os
import sys
myDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.split(os.path.split(myDir)[0])[0]  
if(sys.path.__contains__(parentDir)):
    print('parent already in path')
    pass
else:
    print('parent directory added')
    sys.path.append(parentDir)

from kafka_api.producer import kafkaPublisher

class publish2kafkaPipeline: 
    def __init__(self) -> None:
          
        self.producer = kafkaPublisher()
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        topic = spider.name
        try : 
            itemData = {}
            itemData["alertType"] = adapter.get("alertType")
            itemData["link"] = adapter.get("link")
            itemData["title"] = adapter.get("title")
            itemData["date"] = adapter.get("date")
        except Exception as e:
            raise DropItem(f"Missing data in {item}")

        try :
            self.producer.publishDataOne(itemData,topic)
            return item
        except Exception as e:
            raise DropItem(f"can't publish data to topic!")

        

class ArticleScraperPipeline:
    def process_item(self, item, spider):
        return item
