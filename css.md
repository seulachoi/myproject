## Keyword
`responsive css` `가운데 정렬` `mobile first css`

## 반응형 웹 제작에서 mobile first에서 component 가운데 정렬하기
  - `width:100%` `text-align:center` `margin: 0 auto` 모두 같이 써주어야 가운데 정렬 됩니다.

## 반응형 웹 제작에서 mobile first, web css 분리하기 
  - `@media (min-width: 768px)`으로 css 속성을 mobile, web 따로 적용해주기
  - css 속성을 mobile, web 따로 적용해줄 때, 중복 선언된 개별 속성에 대해 케스케이딩 규칙이 적용되어 `@media`쿼리를 따로 지정할 경우, 개별 속성에 중복 선언하지 않으면 위의 스타일을 적용시킴
  ```.list-box {
    margin-top: 10%;
    margin-left: 20%;
}
.list-group {
    width: 100%;
    text-align: left;
} 
@media (min-width: 768px) {
.list-box {
    margin-top: 10%;
    margin-left: 0; *케스케이딩 규칙*
}
.list-group {
    width: 100%;
    text-align: left;
}
```

## CSS border 
css border link [https://www.w3schools.com/css/css_border.asp]
`border: outset;`
can give css charateristic on childeren by selecting clss `.date-item` of children, even if parent's CSS is adjusted 
children CSS has higher hierachy! 
