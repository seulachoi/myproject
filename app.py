from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

client = MongoClient('localhost',27017)
db=client.sparta

path = "C:/Users/sara/Desktop/chromedriver"
driver = webdriver.Chrome(path)

keyword = '코끼리'
url = 'https://www.google.com/search?q='+keyword+'&hl=ko&sxsrf=ACYBGNSTW5YFeVU0I4abA6H_bXsmwJ-gag:1582014089814&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj7kune1drnAhXaAYgKHQY3CwkQ_AUoAXoECBUQAw&biw=1440&bih=712'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')

images = soup.select('#islrg > div.islrc > div')

for count, image in enumerate(images):
    img = image.select_one('img')
    print(img['src'])
    if count == 5:
        break

driver.close()