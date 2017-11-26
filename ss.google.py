# -*- coding: utf-8 -*-
"""
Created on Mon May  8 23:16:01 2017

@author: kisud
"""

# 참고: http://pleasebetrue.tistory.com/201

import requests
from bs4 import BeautifulSoup

def ss_google(max_pages):
    page=1
    while page <= max_pages:
        url = "http://www.naver.com"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        ranks = soup.find("div", {"class":"rankup"}) # div 태그 중 class: rankup인 것을 가져옴. 유일하니까 find

        for keywords in ranks.findAll('li'): # 왜 에러?
            print(keywords.a['title'])
        page += 1
ss_google(1)
