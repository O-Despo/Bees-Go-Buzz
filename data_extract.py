import requests
import re

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
        self.init_api_strings()
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
        self.init_api_strings()
        api_return = self.api_request()
        self.page_data.update(api_return)
        return self.page_data

dex = data_extract_driver()
ur = ("https://www.buzzfeed.com/victoriavouloumanos/people-share-telling-loved-ones-holidays-cancelled-reactions?ref=hpsplash&origin=spl")
print(dex.run_on_url(ur))
