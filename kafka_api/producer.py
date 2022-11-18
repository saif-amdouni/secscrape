from kafka import *
from json import dumps
from .config import *

class kafkaPublisher :
    def __init__(self) -> None:
        self.ip , self.port = kafkaIP ,kafkaPort
        self.producer = KafkaProducer(bootstrap_servers=[f'{kafkaIP}:{kafkaPort}'],
                        value_serializer=self.serializer)

    def publishDataOne(self, data, topic):
        self.producer.send(topic, value=data)
        self.producer.flush()
        
    def publishDataMultiple(self, dataMulti, topic):
        for data in  dataMulti:
            self.producer.send(topic, value=data)
        self.producer.flush()

    @staticmethod
    def serializer(x):
        return dumps(x).encode('utf-8')

if __name__ == "__main__":
    producer = kafkaPublisher()
    for i in range(100000):
        print(i)
        producer.publishDataOne({"test":i},"thehackernews")

