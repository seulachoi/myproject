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
