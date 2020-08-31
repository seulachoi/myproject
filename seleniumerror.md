# ubuntu headless chrome 셀레니움 오류
## 문제 : 처음 종목 검색 , 검색결과 도출 의 셀레니움은 잘 수행이 되지만, 3번, 4번째 부터는 `python linux selenium: chrome not reachable - python`, `timeout error` 등이 발생 ㅠㅠ 

### 시도 1 : chrome options 에 `chrome_options.add_argument("--remote-debugging-port=9222")` 을 추가해본다 
--결과 : 아래 오류가 뜸 
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created from disconnected: unable to connect to renderer
```
-재시도 : 다시 추가한 옵션 없애줌   
--재시도 결과 : `selenium.common.exceptions.WebDriverException: Message: unknown error: DevToolsActivePort file doesn't exist`
`File "/home/ubuntu/my_projects/app.py", line 219, in stocks_info` 오류 발생 ㅠㅠ 

## 파이썬 셀레니움 옵션 부분 코드 
```
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
  
