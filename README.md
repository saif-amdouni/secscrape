# secscrape

This project allows the collection of cyber security news from multiple sources and blogs 
The Current version only collects news from one source "thehackernews.com"

The implemented data pipeline is composed of mulitple components :

# 1- Data scraping
    
    This component is responsible for scraping news article from web sites and organizing them in a standard format as well as publishing the data to Apache Kafka broker. 
    This component is based on scrapy framework.

# 2- kafka 

    This component is rasponsible for collecting the published news articles and ensuring the delivery to the consumers 

# 3- MongoDB consumer

    This component is responsible for listening to specific topics from the kafka broker and processing any new published message as well as saving the data to mongoDB cloud database  