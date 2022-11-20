import mongoengine as me
from datetime import datetime
import os 
import pandas as pd 
from entity_manager import theHackerNewsArticle
from tqdm import tqdm

DataBackupFolder = "article_scraper\DataBackup"

files = os.listdir(DataBackupFolder)
mongoCred = "mongodb+srv://saifamd:geF5PALFtULS7XB@cluster0.uv6ltxj.mongodb.net/"
me.connect("theHackerNews",host = mongoCred)

for file in files :
    path = os.path.join(DataBackupFolder, file)
    newsDF = pd.read_csv(path,sep="\t")
    articleType = file.split(".csv")[0].split("-")[1]
    for id, row in tqdm(newsDF.iterrows()):
        theHackerNewsArticle(articleType=articleType, date=datetime.strptime(row["date"], '%B %d, %Y'), title=row["title"], link=row["link"]).save()