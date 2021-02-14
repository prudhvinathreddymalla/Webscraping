# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 23:32:06 2021

@author: ASD
"""

# =============================================================================
# Install beautifulsoup4 and requests before running this script
# =============================================================================

#%% Importing the libraries

import requests
from bs4 import BeautifulSoup
import pprint
import json


res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')
links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

all_links = links + links2
all_subtexts = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k: k['votes'], reverse = True)


def create_custom_news(links, subtexts):
    
    news_list = []
    
    for idx, item in enumerate(links):
        
        title = item.getText()
        href = item.get('href', None)
        vote = subtexts[idx].select('.score')
        
        if len(vote):
            points = int(vote[0].getText().replace('points','' ))
            
            if points > 99:
                news_list.append({'title' : title, 
                                  'link': href, 
                                  'votes': points})        
    
    return sort_stories_by_votes(news_list)

news_to_read = create_custom_news(all_links, all_subtexts)



# creating a json file to transfer the information to read
json_news = json.dumps(news_to_read, indent=4)
# print(json_news)

json_file = open('json_news_file', 'w')
json_file.write(json_news)
json_file.close()













