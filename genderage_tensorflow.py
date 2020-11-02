import numpy as np
import cv2

facenet = cv2.dnn.readNet('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel')

gender_list = ['Male', 'Female'] #리스트형이니까 male이면 0, female이면 1로 인식 
age_list = ['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)'] #인덱스형이니까 각 범위를 0,1,2,3,....순서대로 인식

gender_net = cv2.dnn.readNetFromCaffe('models/deploy_gender.prototxt', 'models/gender_net.caffemodel')
age_net = cv2.dnn.readNetFromCaffe('models/deploy_age.prototxt', 'models/age_net.caffemodel')

img = cv2.imread('imgs/02.jpg')

h, w, c = img.shape

# 이미지 전처리하기
blob = cv2.dnn.blobFromImage(img, size=(300, 300), mean=(104., 177., 123.))

# 얼굴 영역 탐지 모델로 추론하기
facenet.setInput(blob)
dets = facenet.forward()

# 각 얼굴에 대해서 반복문 돌기
for i in range(dets.shape[2]):
    confidence = dets[0, 0, i, 2]

    if confidence < 0.5:
        continue

    # 사각형 꼭지점 찾기
    x1 = int(dets[0, 0, i, 3] * w)
    y1 = int(dets[0, 0, i, 4] * h)
    x2 = int(dets[0, 0, i, 5] * w)
    y2 = int(dets[0, 0, i, 6] * h)

    face = img[y1:y2, x1:x2] #얼굴영역 크롭/ 여기서부터 모델 적용 코드짜기

    #이미지 사이즈를 227로 바꿍어주고, mean 값을 빼주고, 차원변형 실행
    blob = cv2.dnn.blobFromImage(face, size=(227, 227), mean=(78.4263377603, 87.7689143744, 114.895847746))

    gender_net.setInput(blob)
    gender_index = gender_net.forward().squeeze().argmax() #argmax: 인덱스에서 리스트를 추출해내줌
    gender = gender_list[gender_index]

    age_net.setInput(blob)
    age_index = age_net.forward().squeeze().argmax()
    age = age_list[age_index]

    cv2.putText(img, text='%s,%s' % (gender,age), org=(x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0), thickness=2)

    cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)


cv2.imshow('result', img)
cv2.waitKey(0)

