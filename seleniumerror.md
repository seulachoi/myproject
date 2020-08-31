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
 -시도 : 종목 매칭 리스트 다음에 `driver.quit()` 세부 종목 리서치 정보 셀레니움 다음에 `driver.quit()` 을 추가함 
 

## 파이썬 셀레니움 옵션 부분 코드 
```
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-browser-side-navigation')
```

## 문제 : `/stocksinfo GET` 요청에서 `chrome not reachable` 오류 발생 
```
File "/home/ubuntu/my_projects/app.py", line 306, in stocks_info
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
  File "/home/ubuntu/.local/lib/python3.6/site-packages/selenium/webdriver/chrome/webdriver.py", line 81, in __init__
    desired_capabilities=desired_capabilities)
  File "/home/ubuntu/.local/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 157, in __init__
    self.start_session(capabilities, browser_profile)
  File "/home/ubuntu/.local/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 252, in start_session
    response = self.execute(Command.NEW_SESSION, parameters)
  File "/home/ubuntu/.local/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "/home/ubuntu/.local/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: chrome not reachable
211.200.56.44 - - [31/Aug/2020 05:57:08] "GET /stocksinfo?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 200 -
```


  
