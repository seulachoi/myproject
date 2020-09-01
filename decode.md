# decodeUri / encodeUri
1. ajax 요청으로 데이터를 받아오고 <a href="/stocksinfo?title=${dataname}" onclick="loadingContainer()">${dataname}</a>
2. html에서 받아온 데이터로 <a href="/stocksinfo?title=서부T&D" onclick="loadingContainer()">서부T&D</a> 를 그리는데,
3. 다시 app.py로 서부T&D를 GET 요청으로 받아올 때 서부T 까지만 받아오네요, & 가 중간에 있어서 에러가 생기는 것 같은데, 어떻게 해결하면 좋을까요? 한글/영문로만 된 키워드에서는 문제는 없었습니다..! 
https://twpower.github.io/113-uri-encode-decode-in-javascript

## 방법 : url에 넣을 때 encode 해줘서 넣고, 다시 받을 때 decode 하기! 
title= 에 넣어서 다시 보내실 때, 다시 인코딩을 해서 보내야합니다! 그러고 받는 쪽에서 디코딩을 해야합니다.

지금
title=동원f&b 인데요,

title=동원f %26b로 나오게 해주시면 됩니다.
간단히 title에 넘기기 전에,
& 를 %26 로 리플레이스 하는 것도 방법이겠네요~!
[https://www.convertstring.com/ko/EncodeDecode/UrlEncode]

```
for (let i = 0; i < data.length; i++) {
                                    var encodeData = encodeURI(encodeURIComponent(data[i]));
                                    makeLink(encodeData, data[i])
                                    console.log(encodeData)
```
