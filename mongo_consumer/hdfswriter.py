import sys
import os

myDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.split(myDir)[0]
print(parentDir)
sys.path.append(parentDir)

from kafka_api import consumer
from config import *
from utlis import standardized_timestamp

class hdfsWriter :
    def __init__(self) -> None:
        self.topics = topics
        self.kafkaListeners = self.createListerners()
    
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
            self.dumpToHdfs(messages=messages,topic=listener.topic)
    def dumpToHdfs(self,messages,topic) :
        f = open(os.path.join(output_dir,topic+".txt"),"a")
        f.writelines(messages)            
            
    
if __name__ == "__main__":
    Writer = hdfsWriter()
    while 1 :
        Writer.consume_topics()