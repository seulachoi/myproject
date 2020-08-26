 ## 한글 -> 웹페이지 코드로 바꾸기 (%EC%A0%9C%EC%A3%BC%EB%8F%84.)
```
var decodeName = decodeURI(decodeURIComponent(keyword_search));
```
keyword_search가 제주도 였는데, 제주도를 읽으려 하니 이상한 웹페이지 코드로 나와서, `decodeURI` 로 변환! `decodeURIComponet`로 한번 더 감쌌는데, 이유는...?

## 로딩 인디케이터 보이게 하기
1. getUrlParams()를 통해 /kewords?q=키워드 의 키워드값을 받아옴 (ex.http://127.0.0.1:5000/keywords?q=제주도)
`console.log(params)`하면 `{q: "%EC%A0%9C%EC%A3%BC%EB%8F%84"}`값이 출력됨 
`console.log(params[key])`는 `%EC%A0%9C%EC%A3%BC%EB%8F%84`

2. `let params = getUrlParams()` 로 전달된 url중에서 'q'라는 파라미터가 있으면(`if (params.q)`), 로딩인디케이터를 javascript 로 css 속성을 제어해서 나타나게 한다
`$('#title-box').css('display', 'none');`

3. ajax 요청 후 응답이 오면, html에 새로 그려야 하니까 로딩인디케이터 다시 안보이게 
`$('#title-box').css('display', 'block');`

```
function getUrlParams() {
                const params = {};
                window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (str, key, value) {
                    params[key] = value;
                    console.log(params[key])
                });
                return params;
            }

            $(document).ready(function () {
                let params = getUrlParams();
                // URL로 전달된 `q` 파라미터가 있으면
                if (params.q) {
                    console.log(params.q)
                    // 1. 로딩 인디케이터를 보이도록 처리하고
                    $('#title-box').css('display', 'none');
                    $('#loading-container').css('display', 'block');
                    $('#re-result-box').css('display', 'none');
                    // $('#loader').css('display', 'block');
                    ```
