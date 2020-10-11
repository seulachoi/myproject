import cv2

cap = cv2.VideoCapture('03.mp4')

while True:
    ret, img = cap.read()
    
    if ret == False:
        break

    img = img[183:465, 721:878]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('result',img)

    if cv2.waitKey(10) == ord('q'):
        break


import cv2

cap = cv2.VideoCapture(0)
#VideoCapture : 비디오 불러오기
#VideoCapture(0) 으로 하면 웹캠 영상이 뜬다

while True:
    ret, img = cap.read()
    #ret 은 프레임이 존재하지 않거나(동영상 끝) 오류로 에러가 발생했을 때 ret변수가 생성되며, false로 저장됨
    if ret == False:
        break
    
    cv2.rectangle(img, pt1=(721,183), pt2=(878,465),color=(255,0,0),thickness=2)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dsize=(640,360))
    # img = img[100:200, 150:250]

    cv2.imshow('result', img)

    
    if cv2.waitKey(100) == ord('q'):
        break
    #1msecond만큼 기다리고 다음프레임을 실행
    #100msecond 만큼 기다리고 다음 프레임을 실행(동영상이 느리게 재생)
