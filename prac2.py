from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

client = MongoClient('localhost',27017)
db=client.sparta

path = "C:/Users/sara/Desktop/chromedriver"
driver = webdriver.Chrome(path)

keyword = '빨대'
stock = '관련주'
url = 'https://www.google.com/search?q='+keyword+'+'+stock+'&aqs=chrome..69i57j69i61.1790j0j7&sourceid=chrome&ie=UTF-8'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
news_divs=soup.select('#rso> div')

for div in news_divs:
    head = div.select_one('div > div.s > div > span').text
    print(head)

#rso > div:nth-child(3) > div > div.s > div > span #검색결과에서 보이는 본문
#div > div.r > a > h3  #제목만