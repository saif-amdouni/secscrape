import sys
import os

myDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.split(myDir)[0]
print(parentDir)
sys.path.append(parentDir)

from kafka_api import consumer
from config import *
from utlis import standardized_timestamp
import mongoengine as me
from datetime import datetime
from entity_manager import *
from tqdm import tqdm

class hdfsWriter :
    def __init__(self) -> None:
        self.topics = topics
        self.kafkaListeners = self.createListerners()
        mongoCred = "mongodb+srv://saifamd:geF5PALFtULS7XB@cluster0.uv6ltxj.mongodb.net/"
        me.connect("theHackerNews",host = mongoCred)
        self.messagesProcessors = {"thehackernews" : self.processTheHackerNewsMessages}
        
    def createListerners(self):
        Listeners = []
        for topic in self.topics :
            try :
                Listeners.append(consumer.kafkaListener(topic))
                print(f"created listener on topic : {topic}")
            except Exception as e :
                print("Broker not available")
        return Listeners

    def consume_topics(self):
        # for topic in self.topics : print(f"Consuming from topics {topic} into {output_dir}...")
        for listener in self.kafkaListeners :
            messages, bufferState = listener.startListening()
            self.saveMongo(messages=messages,topic=listener.topic)

    def saveMongo(self, messages, topic) :
        print(f"got new {len(messages)} messages on topic {topic}!")
        if len(messages)>0:
            self.messagesProcessors[topic](messages)

    def processTheHackerNewsMessages(self, messages):
        for message in tqdm(messages,total=len(messages)) :   
            #print(message.keys())
            try :
                alertType=message["alertType"]
                date=datetime.strptime(message["date"], '%B %d, %Y')
                title=message["title"]
                link=message["link"]
            except Exception as e:
                print("message is corrupt !")
                continue
            theHackerNewsArticle(alertType=alertType, 
                                date = date, 
                                title=title, 
                                link=link).save()

             
            
    
if __name__ == "__main__":
    Writer = hdfsWriter()
    while 1 :
        Writer.consume_topics()