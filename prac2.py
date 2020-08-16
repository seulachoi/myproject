from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

krxlist = pd.read_excel("krxlist.xls")
krxlist_data =krxlist[['기업명']]

client = MongoClient('localhost',27017)
db=client.sparta

path = "C:/Users/sara/Desktop/chromedriver"
driver = webdriver.Chrome(path)

#rso > div:nth-child(3) > div > div.s > div > span #검색결과에서 보이는 본문만 가져오기
#div > div.r > a > h3  #제목만

## 1.keyworkd 관련주 검색
keyword = '빨대'
stock = '관련주'
url = 'https://www.google.com/search?q='+keyword+'+'+stock+'&aqs=chrome..69i57j69i61.1790j0j7&sourceid=chrome&ie=UTF-8'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
news_divs=soup.select('#rso> div.g') #div중에서 class 'g' (div.g)인 것만 가져옴! 이미지가 중간에 나오는데, 이미지는 div class g가 아니어서 걸러짐

for div in news_divs:
    head = div.select_one('div > div.s > div > span').text
    print(head)

## 2.keyword 수혜주 검색
keyword = '빨대'
stock = '수혜주'
url = 'https://www.google.com/search?q='+keyword+'+'+stock+'&aqs=chrome..69i57j69i61.1790j0j7&sourceid=chrome&ie=UTF-8'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
news_divs=soup.select('#rso> div.g')

for div in news_divs:
    head = div.select_one('div > div.s > div > span').text
    print(head)

#rso > div:nth-child(1) > div > div.s > div > span
#rso > div:nth-child(5) > div > div.s > div:nth-child(2) > span

## 3.주식 intitle: keyword 검색
stock = '주식'
keyword = '빨대'
url = 'https://www.google.com/search?q='+stock+'intitle:'+keyword+'&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjR946125XrAhUSPXAKHeE9AnEQ_AUoAXoECA4QAw'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
news_divs=soup.select('#rso> div')

for div in news_divs:
    head = div.select_one('g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.JheGif.nDgy9d').text
    print(head)

#질문
##2페이지로 넘어가서 검색결과 크롤링하는 법
##검색 결과1,2,3을 db에 따로 저장해야하는지?
#<셀레니움 클릭>
#selenium element click
#for 문을 돌면서 포함되어 있는지 string contains ("ffff")

