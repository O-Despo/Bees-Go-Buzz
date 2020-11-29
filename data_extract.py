import requests
import re
from pymongo import MongoClient
import json

#mongo interface
client = MongoClient('localhost', 27017)
database = client['buzz_db']
collection = database['buzz_gen']
class data_extract_driver():
    def __init__(self):
        #inits regex patterns 
        self.regex_patterns = {
            "title": re.compile(r'Bqpp">(.*?)</'),
            "desc": re.compile(r'baw8q">(.*?)</'),
            "topic": re.compile(r'jln58">.*?>(.*?)</'),
            "author": re.compile(r'GCD">(.*?)</'),
            "pos": re.compile(r'GCD.*?p>(.*?)</'),
            "date": re.compile(r'dateTime="(.*?)">'),
            "id": re.compile( r'buzzid" content="(.*?)"')
        }
        self.page_data = {}

    def init_api_strings_with_ids(self):
        '''Returns dict of api link f-strings if id is defined else it returns with {id} in ids place''' 

        if self.page_data['id'] == None:
            id = '{id}'
        else:
            id = self.page_data['id']

        self.api_strings = {
            "react": f"https://www.buzzfeed.com/content-reactions-api/v1/buzz/{id}?edition=en-us",
            "comments": f'https://www.buzzfeed.com/comments-api/v1/comments?content_type=buzz&content_id={id}',
            "views": f'https://www.buzzfeed.com/site-component/v1/en-us/buzzstats?buzz_ids={id}'
        }

        return self.api_strings

    def regex_html_info(self, html_text):
        for regex_pattern_key, regex_pattern in self.regex_patterns.items():
            self.page_data[regex_pattern_key] = re.findall(regex_pattern.pattern, html_text)[0]

        return self.page_data
    
    def make_api_request(self, api_string):
        response = requests.get(api_string)
        json_resp = response.json()
        return json_resp
    
    def api_request(self, return_full = True, specific_api = None):
        response_dict = {}

        if specific_api is not None:
            response_dict = self.make_api_request(specific_api)
        else:
            for api_type, api_string in self.api_strings.items():
                api_response = self.make_api_request(api_string)
                response_dict.update(api_response)
        
        if return_full == True:
            return response_dict
        else:
            managed_resp = [response_dict['count'], response_dict['total_reactions'], response_dict['results'][0]['total']]
            return managed_resp

    def run_on_url(self, url):
        
        response = requests.get(url)
        self.resp_text = response.text
        self.regex_html_info(self.resp_text)
        self.init_api_strings_with_ids()
        api_return = self.api_request()
        self.page_data.update(api_return)
        return self.page_data

url = 'https://www.buzzfeed.com/sallykaplan/cheap-ways-to-upgrade-the-things-you-already-own'
dex = data_extract_driver()
resp = dex.run_on_url(url)
collection.replace_one(
    {url: "https://www.buzzfeed.com/sallykaplan/cheap-ways-to-upgrade-the-things-you-already-own"},
    resp
)