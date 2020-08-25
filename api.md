## Keyword
`api` `POST요청` `keyword검색` `mongodb저장`

## keyword 검색어를 mongodb에 저장하고, 검색 횟수를 counting 하기 
  1. html파일에서 검색부분의 값을 불러옴 `$('#inputKeyword').val()`
  ### 클라이언트 
  1. 검색 버튼을 누를 때, 동작 : `onclick="keywordResearch()"` 
  2. `script`부분에서 `keywordResearch()`를 선언
  3. POST 요청이니까, url 및 data 값을 지정
  ```
  function keywordResearch() {
                // 1. keyword을 가져옵니다.
                let keyword = $('#inputKeyword').val();
                window.onload = function() {
                    var getInput = Prompt(keyword);
                    localStorage.setItem("storage",getInput);
                }

                // 2. 입력하지 않았을 경우, 띄어쓰기있는경우 alert를 띄웁니다.
                if (keyword == "") {
                    alert("검색어를 입력해주세요");
                    $('#inputKeyword').focus();
                    return;
                } else if (keyword.indexOf(" ") !== -1) {
                    alert("한단어로 검색해주세요");
                    $('#keyword').focus();
                    return;
                }
                // 3. POST /keyword 에 저장을 요청합니다.
                $.ajax({
                    type: 'POST',
                    url: '/keywords',
                    data: {keyword_give: keyword},
                    success: function (response) {
                        if (response["result"] == "success") {
                            alert(response["msg"]);
                        }
                    }
                });
            }
  ```
  
  ### backend api
  1. 검색어 변수를 받아서, DB에 저장하고 카운팅을 업데이트 하는 것이니까 *POST요청*
  2. 클라이언트가 전달한 변수는 `request.form[`  `]`형태로 받음
  3. if문을 이용, 새로운 키워드라면, db에 저장(keyword, counting)하고 / 이미 있는 키워드라면, counting 수만 1 증가
  4. 
  ##keyword
  ```
  @app.route('/keywords', methods=['POST'])
  def count_keyword():
    # 1. 클라이언트가 전달한 keyword_give를 keyword_receive 변수에 넣습니다.
    keyword_receive = request.form['keyword_give']
    
    # 2. 새로운 키워드라면, mongoDB에 데이터 넣고, db keywords 목록에서 find_one으로 keyword가 keyword_receive와 일치하는 keyword를 찾습니다.
    keyword = db.db_keywords.find_one({'keyword': keyword_receive})
    if keyword is None:
        doc = {
        'keyword': keyword_receive,
        'count': 0
        }
        db.db_keywords.insert_one(doc)
        keyword = db.db_keywords.find_one({'keyword': keyword_receive}) #if 문에서 db에 추가하고 나서 한번 더 keyword를 find_one으로 선언해줘야 4번이 동작함 
    else: # 3. 이미 있는 키워드라면, db keywords 목록에서 find_one으로 keyword가 keyword_receive와 일치하는 keyword를 찾습니다.
        keyword = db.db_keywords.find_one({'keyword': keyword_receive})

    # 4. keyword의 count 에 1을 더해준 new_like 변수를 만듭니다.
    new_count=keyword['count']+1
    
    # 5. keywords 목록에서 keyword가 keyword_receive인 문서의 count 를 new_count로 변경합니다.
    db.db_keywords.update_one({'keyword':keyword_receive}, {'$set':{'count':new_count}})
    # 참고: '$set' 활용하기!
    
    # 6. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '성공!'})
```

## keyword 검색어를 받아서 셀레니움 검색 결과를 페이지에 보여주기 
  - keyword 검색어를 받아오는 방법은 2가지
    1) 클라이언트에서 ajax POST 요청을 통해 받기 
    2) html 클라이언트의 form action을 통해 바로 POST 요청을 날리기 
    **이때, 서버에 주는 키 값은 Form안에서 주는 것이니까, input의 name을 'keyword_give'로 서버에서 받을 이름이랑 맞춰줘야함!**
    
    ```
    <form action="/keywords" method="POST">
                            <input name="keyword_give" id="inputKeyword" type="text" placeholder="검색어를 입력해주세요.">
                            <button type="submit">검색</button>
                        </form>
    ```
  ### 클라이언트에서 GET 요청 /keyword로 보내는 것 보다 위의 검색결과 counting 요청 보낼 때, counting -> selenium까지 한번에 하는 것으로 해결!>_< 
  
  ### backend 
  1. 클라이언트 POST /keywords 로 요청을 보내면, keyword counting 먼저 실행 
  2. 이어서 셀레니움 실행 -> 결과를 matched list에 넣어줌
  3. return json이 아니라 return render_template('index1-2.html', data=matched_list)로 작성 : post 요청 완료 시에 index1-2로 전환되면서, data가 표시됨! 꺅 
  
  ### 클라이언트에서 matched list 표현 방법 javascript
  '{{data}}' 를 먼저 선언해주고 data를 for 문 형태로 나타내고 , list 속성을 줌
  `{% for i in data %}`
  `<li> {{i}} </li>` 
  `{% endfor %}` 
  
  ```
    # API 역할을 하는 부분
    @app.route('/keywords', methods=['POST'])
    def show_matched():
    #<검색한 키워드를 저장, counting 하기>
    # 1. 클라이언트가 전달한 keyword_give를 keyword_receive 변수에 넣습니다.
    keyword_receive = request.form['keyword_give']
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
    print("값이 넘어와요")

    # 2. keyword_receive를 셀레니움으로 keyword를 검색합니다. 셀레니움 으로 키워드 크롤링해서 매칭 종목 찾기
    path = "C:/Users/sara/Desktop/chromedriver"
    driver = webdriver.Chrome(path)

    ###셀레니움 코드####

    # 여러 종목일 경우, 가장 많이 나온 5개를 출력하기
    print(resultlist)
    word_ranking = pd.Series(resultlist).value_counts()
    word_top5 = word_ranking[:5]

    matched_list = []
    i = 0
    while i < 5:
        matched_list.append(word_top5.index[i])
        i += 1
    print(matched_list)
    # 참고) star_list = list(db.mystar.find({},{'_id':False}).sort("like",-1))
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!

    # 2. 마지막에 index1-2를 data와 함께 전달! 
    return render_template('index1-2.html', data=matched_list)
```

## keyword 검색 후 매칭된 주식 종목리스트를 클릭 시 -> 해당 종목 상세 페이지로 넘어가기 
  - 주식 종목 이름을 클릭 시, 해당 종목 상세페이지html로 이동
  ###클라이언트
    1) html에서 a tag로 `<a href="/stocksinfo?title={{i}}">` 로 링크를 걸어주기! `href`뒤에 /stocksinfo 로 url을 넣어주고, **변수 `title`에 들어가야 할 종목 이름을 넣어주기**
    **이때는 get 요청에 해당함**
  ###Backend
    1) 서버에서 /stocksinfo url로 요청에 대한 api 구성
    2) get요청이니까 `requests.args.get()`로 변수를 받아줌 (post 요청일 때는 `requests.form[]` get일때는 ()이구 post 요청일때는 [])
    ```
    @app.route('/stocksinfo', methods=['GET'])
    def stocks_info():
    matched_receive = request.args.get('title')
    ```
    
## ajax POST 매칭된 주식 종목리스트를 클릭 시 -> 해당 종목 상세 페이지로 넘어가기 
  - 주식 종목 이름을 클릭 시, 해당 종목 상세페이지html로 이동
  ###클라이언트
    1) html에서 a tag로 `<a href="/stocksinfo?title={{i}}">` 로 링크를 걸어주기! `href`뒤에 /stocksinfo 로 url을 넣어주고, **변수 `title`에 들어가야 할 종목 이름을 넣어주기**
    **이때는 get 요청에 해당함**
  ###Backend
    1) 서버에서 /stocksinfo url로 요청에 대한 api 구성
    2) get요청이니까 `requests.args.get()`로 변수를 받아줌 (post 요청일 때는 `requests.form[]` get일때는 ()이구 post 요청일때는 [])
    ```
    @app.route('/stocksinfo', methods=['GET'])
    def stocks_info():
    matched_receive = request.args.get('title')
    ```
  
  
