# ubuntu headless chrome 셀레니움 오류
## 문제 : 처음 종목 검색 , 검색결과 도출 의 셀레니움은 잘 수행이 되지만, 3번, 4번째 부터는 `python linux selenium: chrome not reachable - python`, `timeout error` 등이 발생 ㅠㅠ 
`211.200.56.44 - - [31/Aug/2020 01:28:47] "POST /keywords HTTP/1.1" 500 -`

### 시도 1 : chrome options 에 `chrome_options.add_argument("--remote-debugging-port=9222")` 을 추가해본다 
--결과 : 아래 오류가 뜸 
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created from disconnected: unable to connect to renderer
```
-재시도 : 다시 추가한 옵션 없애줌   
--재시도 결과 : `selenium.common.exceptions.WebDriverException: Message: unknown error: DevToolsActivePort file doesn't exist`
`File "/home/ubuntu/my_projects/app.py", line 219, in stocks_info` 오류 발생 ㅠㅠ 

## 문제 : 3,4번째 부터 로딩 시간이 아주 오래걸리면서 `211.200.56.44 - - [31/Aug/2020 01:28:47] "POST /keywords HTTP/1.1" 500 -`, `selenium.common.exceptions.TimeoutException: Message: timeout: Timed out receiving message from renderer: 285.715 (Session info: headless chrome=85.0.4183.83)` 에러가 뜸 
` File "/home/ubuntu/my_projects/app.py", line 135, in show_matched
    driver.get(url)` 에서 오류 발생 

## 파이썬 셀레니움 옵션 부분 코드 
```
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
  
