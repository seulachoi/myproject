# findAll class 여러개 조건 주기
`soup.findAll(True, {'class':['class1', 'class2']})` : class 여러개에 해당하는 id 를 가진 요소를 가져올 수 있음 
```
click_list1 = youtubetitle_first.find_all('ytd-video-meta-block',
                                                {'class': ['style-scope ytd-video-renderer byline-separated','style-scope ytd-video-renderer']})
                                                ```
