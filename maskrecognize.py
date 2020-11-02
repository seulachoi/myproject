from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
import cv2

facenet = cv2.dnn.readNet('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel') #얼굴 영역 탐지 모델
model = load_model('models/mask_detector.model') #마스크 썼는지 찾아내는 모델

cap = cv2.VideoCapture('videos/04.mp4') #동영상 플레이어 만드는 코드

while True:
    ret, img = cap.read()

    if ret == False:
        break

    h, w, c = img.shape #이미지 shape 저장해주기
    # 이미지 전처리하기 (img라는 변수를 전처리, resize기능으로 300 사이즈 + mean 값을 빼주고 + 차원변형)
    blob = cv2.dnn.blobFromImage(img, size=(300, 300), mean=(104., 177., 123.))

    # 얼굴 영역 탐지 모델로 추론하기 (입력값: 얼굴을 찾아낼 이미지, 출력값: confidence)
    facenet.setInput(blob)
    dets = facenet.forward() #dets라는 변수에 얼굴영역 탐지결과를 저장

    # 각 얼굴에 대해서 반복문 돌기 (사람의 얼굴은 여러개일 수 있으니까 반복문 돌아가면서 처리)
    for i in range(dets.shape[2]):
        confidence = dets[0, 0, i, 2] #얼굴인지 아닌지 얼마나 확신하는가?를 나타내는 지표-> 숫자를 높일수록 엄격하게 설정가능

        if confidence < 0.5: #0.5 아래는 제외
            continue

        # 사각형 꼭지점 찾기 (x1,x2,y1,y2를 찾아야하는데 / 모델이 왼쪽위부터 %로 인식-> w,h를 곱해주어서 위치로 변환)
        x1 = int(dets[0, 0, i, 3] * w) #x1의 % * 원래이미지의 가로길이 / #int 로 정수형으로 변환
        y1 = int(dets[0, 0, i, 4] * h) #y1의 % * 원래이미지의 세로길이
        x2 = int(dets[0, 0, i, 5] * w)
        y2 = int(dets[0, 0, i, 6] * h)

        #얼굴영역 잘라내기 (잘라낼때에는 y 부터!)
        face = img[y1:y2, x1:x2]
        
        #얼굴잘라낸 이미지 전처리 : 
        face_input = cv2.resize(face, dsize=(224, 224)) #dsize사이즈를 줄이고
        face_input = cv2.cvtColor(face_input, cv2.COLOR_BGR2RGB) #color를 바꾸어줌, 전처리할 때 컬러시스템 바꾸어줘야 할 때가 있음
        face_input = preprocess_input(face_input) #preprocess_input : 이 함수를 거쳐야 전처리가 되니까, 거쳐야하는 과정
        face_input = np.expand_dims(face_input, axis=0) #차원변형, expand_dims 로 차원을 추가해줌, 앞에 차원 1을 추가하여 (1,224,224,3) 

        #모델 결과 출력 : predict 사용. mask는 썼을 확률 nomask는 마스크 안썼을 확률 / 둘 더하면 1 
        mask, nomask = model.predict(face_input).squeeze()

        if mask > nomask:
            color = (0,255,0)
        else:
            color = (0,0,255)

        # 사각형 그리기
        cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=color)

    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
