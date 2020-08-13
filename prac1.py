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
stock = '주식'
url = 'https://www.google.com/search?q='+keyword+'intitle:'+stock+'&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjR946125XrAhUSPXAKHeE9AnEQ_AUoAXoECA4QAw'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
news_divs=soup.select('#rso> div')

for div in news_divs:
    head = div.select_one('g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.JheGif.nDgy9d').text
    print(head)

