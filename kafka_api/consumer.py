from kafka import KafkaConsumer
from json import loads
from config import *

class kafkaListener :
    def __init__(self, topic) -> None:
        self.ip , self.port = kafkaIP ,kafkaPort
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic ,
                                    bootstrap_servers=[f'{self.ip}:{self.port}'],
                                    auto_offset_reset= auto_offset_reset,
                                    enable_auto_commit= enable_auto_commit,
                                    value_deserializer=self.deserializer )
    def startListening(self):
        print(f"start listening to {self.topic} ...")
        try :
            for message in self.consumer:
                val = message.value
                print(f"{val}")
        except Exception as e :
            print(f"can't listen to topic : {self.topic} !")

    @staticmethod
    def deserializer(x):
        return loads(x.decode('utf-8'))

if __name__ == "__main__":
    listener = kafkaListener(topic = "thehackernews")
    listener.startListening()


