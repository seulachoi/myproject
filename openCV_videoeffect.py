import cv2
import numpy as np

net = cv2.dnn.readNetFromTorch('models/instance_norm/mosaic.t7')

cap = cv2.VideoCapture('imgs/03.mp4')
#VideoCapture : 비디오 불러오기
#VideoCapture(0) 으로 하면 웹캠 영상이 뜬다

while True:
    ret, img = cap.read()
    #ret 은 프레임이 존재하지 않거나(동영상 끝) 오류로 에러가 발생했을 때 ret변수가 생성되며, false로 저장됨
    if ret == False:
        break
    
    # cv2.rectangle(img, pt1=(721,183), pt2=(878,465),color=(255,0,0),thickness=2) #동영상 안에 사각형 그리기
    
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.resize(img, dsize=(640,360))
    # # img = img[100:200, 150:250]

    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

    net.setInput(blob)
    output = net.forward()
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE
    output = np.clip(output, 0, 255) 
    output = output.astype('uint8') 

    cv2.imshow('result', output)

    
    if cv2.waitKey(1) == ord('q'):
        break
    #1msecond만큼 기다리고 다음프레임을 실행
    #100msecond 만큼 기다리고 다음 프레임을 실행(동영상이 느리게 재생)
