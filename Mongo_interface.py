from pymongo import MongoClient
import data_extract
import json

#mongo interface
client = MongoClient('localhost', 27017)
database = client['buzz_db']

XML_OUT_JSON = open('XML_scrape.json', 'r')
data_ex_driver =  data_extract.data_extract_driver()
for url, category in XML_OUT_JSON.read():
    print(url)
    print(category)