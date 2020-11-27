import requests 
import json
import pickle
import xml.etree.ElementTree as ET

# class save_state_xml:
#     def __init__(self):
#         self.save_file = open('XML_manager_save_state.json', 'wb')
#         self.save_state_dict = {}
    
#     def save(self):
#         json.dump(self.save_state_dict, self.save_file)

#     def save_sitemap(self, sitemap):
#         self.save_state_dict['sitemap'] = sitemap
#         self.save()
    
#     def save_url(self, url)
#         self.save_state_dict['current_url'] = urls

class XML_scrap_driver:
    def __init__(self, custom_site_maps = 0, save_location = 0):
        if custom_site_maps == 0:
            self.sitemaps = {
            'shop': 'https://www.buzzfeed.com/sitemap/shopping.xml',
             'asis': 'https://www.buzzfeed.com/sitemap/asis.xml',
             'buzzfeed': 'https://www.buzzfeed.com/sitemap/buzzfeed.xml',
             'community': 'https://www.buzzfeed.com/sitemap/buzzfeed-community.xml',
             'tasty': 'https://www.buzzfeed.com/sitemap/tasty.xml'
            }
        else:
            self.sitemaps = custom_site_maps
        
        if save_location == 0:
            self.out_json = open('XML_scrape.json', 'w')
        else:
            self.out_json = open(save_location, 'w')
 
    def urls_from_xml(self, url):
        '''Parse XML from urls returns list of fist subvalue from child'''
        url_list = []
        response =  requests.get(url)
        root = ET.fromstring(response.content)

        for child in root:
            url_list.append(child[0].text)

        return url_list

    def run_all(self):
        urls_data_dict = {}

        for sitemap in self.sitemaps:
            print(f'On Sitemap: {sitemap}\nXML: {self.sitemaps[sitemap]}')
            site_maps_secondary = self.urls_from_xml(self.sitemaps[sitemap])

            for secondary_url in site_maps_secondary:
                article_urls = self.urls_from_xml(secondary_url)
                for article_url in article_urls:
                    urls_data_dict[article_url] = sitemap

        json.dump(urls_data_dict, self.out_json)

    def run_new  ()


XML_driver = XML_scrap_driver()
XML_driver.run()