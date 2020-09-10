from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import krxlist
import datetime
from dateutil.relativedelta import relativedelta
from urllib import parse
import urllib
from pyvirtualdisplay import Display
import time
#pip install python-dateutil
#pip install urllib3
app = Flask(__name__)

client = MongoClient('mongodb://sara:sara@3.34.49.195', 27017)
db = client.dbsparta

# display = Display(visible=0, size=(1920, 1080))
# display.start()

stocklist=krxlist.stocklist    

# HTML 화면 보여주기
@app.route('/')
def home():
    recent_keywords_all=list(db.db_keywords.find({},{'_id':0, 'count':0}).sort('count',-1))
    recent_keywords=recent_keywords_all[:10]
    recent_list=[]
    rank_list=[]
    for i in range(len(recent_keywords)):
        keyword=recent_keywords[i]['keyword']
        recent_list.append(keyword)
        i+=1
        rank_list.append(i)

    recent_rank_list=zip(rank_list, recent_list)
    return render_template('index.html', recent_list=recent_rank_list)


# API 역할을 하는 부분
@app.route('/keywords', methods=['GET'])
def show_matched_only_html():
    return render_template('index1-2.html')

@app.route('/keywords', methods=['POST'])
def show_matched():
    #<검색한 키워드를 저장, counting 하기>
    # 1. 클라이언트가 전달한 keyword_give를 keyword_receive 변수에 넣습니다.
    keyword_receive_before = request.form['keyword_give']
    keyword_receive=parse.unquote(keyword_receive_before)

    # 2. 새로운 키워드라면, mongoDB에 데이터 넣고, db keywords 목록에서 find_one으로 keyword가 keyword_receive와 일치하는 keyword를 찾습니다.
    keyword = db.db_keywords.find_one({'keyword': keyword_receive})
    if keyword is None:
        doc = {
            'keyword': keyword_receive,
            'count': 0
        }
        db.db_keywords.insert_one(doc)
        keyword = db.db_keywords.find_one({'keyword': keyword_receive})
    else:  # 3. 이미 있는 키워드라면, db keywords 목록에서 find_one으로 keyword가 keyword_receive와 일치하는 keyword를 찾습니다.
        keyword = db.db_keywords.find_one({'keyword': keyword_receive})

    # 4. keyword의 count 에 1을 더해준 new_like 변수를 만듭니다.
    new_count = keyword['count'] + 1
    # 4. keywords 목록에서 keyword가 keyword_receive인 문서의 count 를 new_count로 변경합니다.
    db.db_keywords.update_one({'keyword': keyword_receive}, {'$set': {'count': new_count}})
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다. (필요한가?, 없어야 하나?)
    #return jsonify({'result': 'success', 'msg': '성공!'})

    #<검색어를 셀레니움으로 검색하고, 검색 결과를 index1-2.html에 보여줌
    # 1. 클라이언트가 전달한 keyword_give를 keyword_receive 변수에 넣습니다
    keyword_receive = request.form['keyword_give']

    # 2. keyword_receive를 셀레니움으로 keyword를 검색합니다. 셀레니움 으로 키워드 크롤링해서 매칭 종목 찾기
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-browser-side-navigation')
    #chrome_options.add_argument("--remote-debugging-port=9222")

    path = "/home/ubuntu/chromedriver"
    driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)

    # rso > div:nth-child(3) > div > div.s > div > span #검색결과에서 보이는 본문만 가져오기
    # div > div.r > a > h3  #제목만

    ## 1.keyworkd 관련주 검색
    keyword = keyword_receive
    print(keyword)
    stock = '관련주'
    url = 'https://www.google.com/search?q=' + keyword + '+' + stock + '&aqs=chrome..69i57j69i61.1790j0j7&sourceid=chrome&ie=UTF-8'
    search_list = []

    driver.get(url)

    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    news_divs = soup.select(
        '#rso> div.g')  # div중에서 class 'g' (div.g)인 것만 가져옴! 이미지가 중간에 나오는데, 이미지는 div class g가 아니어서 걸러짐

    for div in news_divs:
        head1 = div.select_one('div > div.s > div > span').text
        search_list.append(head1)

    ## 2.keyword 수혜주 검색
    keyword = keyword_receive
    stock = '수혜주'
    url = 'https://www.google.com/search?q=' + keyword + '+' + stock + '&aqs=chrome..69i57j69i61.1790j0j7&sourceid=chrome&ie=UTF-8'

    driver.get(url)

    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    news_divs = soup.select('#rso> div.g')

    for div in news_divs:
        head2 = div.select_one('div > div.s > div > span').text
        search_list.append(head2)

    # rso > div:nth-child(1) > div > div.s > div > span
    # rso > div:nth-child(5) > div > div.s > div:nth-child(2) > span

    ## 3.주식 intitle: keyword 검색
    stock = '주식'
    keyword = keyword_receive
    url = 'https://www.google.com/search?q=' + stock + 'intitle:' + keyword + '&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjR946125XrAhUSPXAKHeE9AnEQ_AUoAXoECA4QAw'

    driver.get(url)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    # topstuff > div > div > p:nth-child(2)
    # xjs > div > h1
    nonews=soup.select('#slim_appbar > div')
    pages=soup.select('#xjs > div > h1')
    matched_list = []
    print(pages)
    if nonews==[]:
        matched_list.append('관련 종목을 찾지 못했습니다, 다른 키워드로 검색해보세요')
        print(matched_list)

    elif pages=="페이지 탐색":
        news_divs = soup.select('#rso> div > g-card > div > div > div.dbsr > a > div')
        ##3-1
        for div in news_divs:
            head3_1 = div.select_one('div.JheGif.nDgy9d').text
            search_list.append(head3_1)

        ###셀레니움 2페이지 클릭하기 copy -> xpath 복사 후 driver.find_element_by_xpath 에 넣어주기
        element = driver.find_element_by_xpath("//*[@id='xjs']/div/table/tbody/tr/td[3]/a")
        element.click()

        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        news_divs = soup.select('#rso> div > g-card > div > div > div.dbsr > a > div')
        ##3-2
        for div in news_divs:
            head3_2 = div.select_one('div.JheGif.nDgy9d').text
            search_list.append(head3_2)
    else :
        news_divs = soup.select('#rso> div > g-card > div > div > div.dbsr > a > div')
        ##3-1
        for div in news_divs:
            head3_1 = div.select_one('div.JheGif.nDgy9d').text
            search_list.append(head3_1)

        # head1,2,3-1,3-2에서 stocklist에 매칭되는 종목이 있는지 확인하고, 있으면 resultlist에 추가하기
        search_sentences = " ".join(search_list)
        search_words = search_sentences.split(" ")

        resultlist = []
        for data in stocklist:
            for word in search_words:
                if data in word:
                    resultlist.append(data)

        # 여러 종목일 경우, 가장 많이 나온 5개를 출력하기
        print(resultlist)

        word_ranking = pd.Series(resultlist).value_counts()
        word_top5 = word_ranking[:5]
        list_number = len(word_ranking)

        if list_number == 0:
            matched_list.append('관련 종목을 찾지 못했습니다, 다른 키워드로 검색해보세요!')
        elif list_number < 5:
            i=0
            while i < len(word_ranking):
                matched_list.append(word_ranking.index[i])
                i+=1
        else:
            i=0
            while i <5 :
                matched_list.append(word_top5.index[i])
                i+=1
    print(matched_list)
    driver.quit();

    # 참고) star_list = list(db.mystar.find({},{'_id':False}).sort("like",-1))
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!

    # 2. 위 셀레니움 완료시, index1-2를 matched_list와 함께 보여줌

    return jsonify({'result':'success', 'data':matched_list, 'keyword_search':keyword_receive})
    return render_template('index1-2.html', data=matched_list, keyword_search=keyword_receive)

#매칭된 결과 종목 이름을 클라이언트에서 가져오고(클라이언트: form action을 통한 GET -> 셀레니움으로 검색 -> 검색결과를 새로운 HTML페이지에 그림
@app.route('/stocksinfo', methods=['GET'])
def stocks_info():
    matched_receive_before = request.args.get('title')
    print(matched_receive_before)
    matched_receive=urllib.parse.unquote(matched_receive_before)
    print(matched_receive)

    # 종목 리서치 정보 가져오기
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable - setuid - sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-browser-side-navigation')
    #chrome_options.add_argument("--remote-debugging-port=9222")

    path = "/home/ubuntu/chromedriver"
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)


    a = datetime.datetime.today()
    edate = a.strftime("%Y-%m-%d")
    edt = datetime.datetime.now() - relativedelta(months=3)
    sdate = edt.strftime("%Y-%m-%d")

    stock = matched_receive
    stock_name = db.stocklist.find_one({'name': stock})
    stock_code = db.stocklist.find_one({'name': stock}, {'_id': False, 'name': False})
    print(stock_name)
    print(stock_code)
    code = stock_code['code']

    title_list = []
    link_list=[]
    date_list=[]
    name_list=[]
    company_list=[]
    price_list=[]

    url = 'http://consensus.hankyung.com/apps.analysis/analysis.list?sdate=' + sdate + '&edate=' + edate + '&now_page=1&search_value=&report_type=CO&pagenum=20&search_text=' + code + '&business_code='

    driver.get(url)

    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    trs = soup.select('#contents > div.table_style01 > table > tbody > tr')
    td_none=soup.select('#contents > div.table_style01 > table > tbody > tr > td')
    td = td_none[0].text

    if td=="결과가 없습니다.":
        date_list.append("")
        price_list.append("")
        title_list.append("최근 리포트가 없습니다")
        company_list.append("")
        name_list.append("")
    else :
        for tr in trs:
            title = tr.select_one('td.text_l > div.layerPop > div > strong').text
            title_list.append(title)
            date = tr.select_one('td.first.txt_number').text
            date_list.append(date)
            price = tr.select_one('td.text_r.txt_number').text
            price_list.append(price)
            name = tr.select_one('td:nth-child(5)').text
            name_list.append(name)
            company = tr.select_one('td:nth-child(6)').text
            company_list.append(company)

    if td == "결과가 없습니다.":
        link_list.append("")
    else:
        for i in range(len(title_list)):
            link_a=driver.find_element_by_xpath('// *[ @ id = "contents"] / div[2] / table / tbody / tr / td[9] / div / a')
            link=link_a.get_attribute('href')
            link_list.append(link)

    mylist = zip(date_list, price_list, link_list, title_list, company_list, name_list)
    data = {
        'mylist': mylist
    }
    print(date_list)
    print(price_list)
    print(name_list)
    print(company_list)
    print(title_list)
    print(link_list)
    driver.quit()
    time.sleep(1)


    #<종목 기본 정보 가져오기 : 네이버 증권 기본 정보>
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-browser-side-navigation')
    #chrome_options.add_argument("--remote-debugging-port=9222")

    path = "/home/ubuntu/chromedriver"
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    url = 'https://finance.naver.com/item/coinfo.nhn?code=' + code

    driver.get(url)
    req = driver.page_source

    p_list=[]
    soup = BeautifulSoup(req, 'html.parser')
    div0 = soup.select('#middle > div.h_company > div.wrap_company > div > em.summary > div > div')

    p=div0[0].find_all('p')
    print(len(p))
    for i in range(len(p)):
        p_text=p[i].text
        p_list.append(p_text)
    print(p_list)
    driver.quit()
    time.sleep(1)

    #<종목 유튜브 정보 가져오기: 유튜브 썸네일, 제목, 조회수, 날짜>
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-browser-side-navigation')
    #chrome_options.add_argument("--remote-debugging-port=9222")

    path = "/home/ubuntu/chromedriver"
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    url = 'https://www.youtube.com/results?search_query=' + matched_receive + '+' + "%2B주식"'+'"-무료"'&sp=CAMSAhAB'
    driver.get(url)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    youtubeimg_list = []
    youtubetitle_list = []
    youtubeclick_list = []
    youtubedate_list = []
    youtubelink_list = []

    youtubeimg_first = soup.find('div', {'id': 'contents'})
    print(len(youtubeimg_first))
    # 검색 결과가 없을 때엔 div.contents 가 1개이고, 검색결과가 있을 때에는 div.contents가 2개
    if len(youtubeimg_first) == 1:
        youtubeimg_list.append("")
        youtubetitle_list.append("검색결과가 없습니다.")
        youtubeclick_list.append("")
        youtubedate_list.append("")
        youtubelink_list.append("")

    else:
        youtubeimg_first = soup.find('div', {'id': 'contents'})
        img_second = youtubeimg_first.find_all('ytd-video-renderer', {'class': 'style-scope ytd-item-section-renderer'})
        youtube_number = len(img_second)
        print(youtube_number) #동영상 개수

        # 동영상 검색 개수가 5개 보다 작으면, 검색 개수만큼 for문 돌리기
        if youtube_number < 5:
            for i in range(youtube_number):
                img_list1 = img_second[i].find('ytd-thumbnail', {'class': 'style-scope ytd-video-renderer'})
                img_list2 = img_list1.find_all('a',
                                               {'class': 'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})
                # 이미지 썸네일 부분
                print(img_list2)
                img_list3 = img_list2[0].find('img', {'class': 'style-scope yt-img-shadow'})
                print(img_list3)
                img_link = img_list3.get('src')
                youtubeimg_list.append(img_link);

                # href 링크 부분
                href_link0 = img_list2[0].get('href')
                href_link1 = "https://www.youtube.com" + href_link0
                youtubelink_list.append(href_link1)

            for i in range(youtube_number):
                # 동영상 제목
                youtubetitle_first = soup.find('div', {'id': 'contents'})
                title_second = youtubetitle_first.find_all('ytd-video-renderer',
                                                    {'class': 'style-scope ytd-item-section-renderer'})
                title_list0 = title_second[i].find('div', {'class': 'text-wrapper style-scope ytd-video-renderer'})
                title_list1 = title_list0.find_all('h3', {'class': 'title-and-badge style-scope ytd-video-renderer'})
                title_list2 = title_list1[0].find('yt-formatted-string', {'class': 'style-scope ytd-video-renderer'})
                title_list3 = title_list2.text
                youtubetitle_list.append(title_list3);

                # 동영상 조회수click, 동영상 업로드 시기 date
                cd_first = soup.find('div', {'id': 'contents'})
                click_list1 = cd_first.find_all('ytd-video-meta-block',
                                                {'class': 'style-scope ytd-video-renderer byline-separated'})
                click_list2 = click_list1[i].find_all('span', {'class': 'style-scope ytd-video-meta-block'})
                click_number = click_list2[0].text
                date_upload = click_list2[1].text
                youtubeclick_list.append(click_number)
                youtubedate_list.append(date_upload);

        else:
            for i in range(0, 5):
                img_list1 = img_second[i].find('ytd-thumbnail', {'class': 'style-scope ytd-video-renderer'})
                img_list2 = img_list1.find_all('a',
                                               {'class': 'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})
                # 이미지 썸네일 부분
                img_list3 = img_list2[0].find('img', {'class': 'style-scope yt-img-shadow'})
                img_link = img_list3.get('src')
                youtubeimg_list.append(img_link);
                # href 링크 부분
                href_link0 = img_list2[0].get('href')
                href_link1 = "https://www.youtube.com" + href_link0
                youtubelink_list.append(href_link1)

            for i in range(0, 5):
                # 동영상 제목
                youtubetitle_first = soup.find('div', {'id': 'contents'})
                title_second = youtubetitle_first.find_all('ytd-video-renderer',
                                                    {'class': 'style-scope ytd-item-section-renderer'})
                title_list0 = title_second[i].find('div', {'class': 'text-wrapper style-scope ytd-video-renderer'})
                title_list1 = title_list0.find_all('h3', {'class': 'title-and-badge style-scope ytd-video-renderer'})
                title_list2 = title_list1[0].find('yt-formatted-string', {'class': 'style-scope ytd-video-renderer'})
                title_list3 = title_list2.text
                youtubetitle_list.append(title_list3);

                # 동영상 조회수click, 동영상 업로드 시기 date
                click_list1 = youtubetitle_first.find_all('ytd-video-meta-block',
                                                {'class': ['style-scope ytd-video-renderer byline-separated','style-scope ytd-video-renderer']})

                click_list2 = click_list1[i].find_all('span', {'class': 'style-scope ytd-video-meta-block'})

                if len(click_list2)==2:
                    click_number = click_list2[0].text
                    date_upload = click_list2[1].text
                    youtubeclick_list.append(click_number)
                    youtubedate_list.append(date_upload)
                else:
                    click_number=click_list2[0].text
                    youtubeclick_list.append(click_number)
                    youtubedate_list.append("")


                #동영상 채널?
    youtube_list = zip(youtubeimg_list, youtubelink_list, youtubetitle_list, youtubeclick_list, youtubedate_list)
    print(youtubeimg_list)
    print(youtubelink_list)
    print(youtubetitle_list)
    print(youtubeclick_list)
    print(youtubedate_list)
    driver.quit();

    return render_template('index1-3.html', youtubelist=youtube_list, infolist=p_list, stockname=matched_receive, report=title_list, link=link_list, data=data, mylist=mylist, date=date_list, price=price_list, name=name_list, company=company_list, code=code)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)