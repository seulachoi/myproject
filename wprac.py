from wordcloud import WordCloud
from PIL import Image
import numpy as np

f = open("test.txt", "w", encoding="utf-8")
f.write("안녕, 스파르타!\n")
for i in [1,2,3,4,5]:
    f.write(f"{i}번쨰 줄입니다\n")
f.close()

text=''

with open("KakaoTalk.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[5:]:
        if '] [' in line:
            text += line.split('] ')[2].replace('오후','').replace('이모티콘\n','').replace('사진\n','').replace('멘토님들','').replace('다들','').replace('톡게시판','').replace('ㅎㅎ','').replace('오늘','')
print(text)

wc = WordCloud(font_path='C:/WINDOWS/Fonts/malgun.ttf', background_color="white", width=600, height=400)
wc.generate(text)
wc.to_file("result.png")

mask = np.array(Image.open('cloud.png'))
wc = WordCloud(font_path='C:/WINDOWS/Fonts/malgun.ttf', background_color="white", mask=mask)
wc.generate(text)
wc.to_file("result_masked.png")


# import matplotlib.font_manager as fm
#
# # 이용 가능한 폰트 중 '고딕'만 선별
# for font in fm.fontManager.ttflist:
#     if 'Gothic' in font.name:
#         print(font.name, font.fname)