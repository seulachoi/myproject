import cv2
import numpy as np

net = cv2.dnn.readNetFromTorch('models/eccv16/starry_night.t7')
#torch로 만들어진 모델을 로드하여, net에 저장함

img = cv2.imread('imgs/01.jpg')

h, w, c = img.shape #이미지의 형태를 높이, 너비, 채널로 나타냄

img = cv2.resize(img, dsize=(500, int(h / w * 500)))
#이미지 비율을 유지하면서 크기를 변형하기!
# h:w = new_H : 500 으로 New_h를 구하기한 다음 int()를 붙여서 정수로만듦
print(img.shape) 
#(325, 500, 3)
MEAN_VALUE = [103.939, 116.779, 123.680]
blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
#blobFromImage 전처리하는 함수 img각 값에서 mean value를 빼줌
#blobFromImage 차원 변형을 지원 : 딥러닝 모델에 넣기 전에 차원 변형을 꼭 해줘야함
print(blob.shape)
#(1, 3, 325, 500) 로 바뀌면서, 차원이 앞으로 오도록 변형

net.setInput(blob)
output = net.forward() #컴퓨터만 알 수 있는 형태니까, 후처리를 해줘야함

output = output.squeeze().transpose((1, 2, 0))
#전처리에서 차원을 늘렸으니, 차원을 줄이는 squeeze
#차원을 다시 변형해주는 transpose
output += MEAN_VALUE
#전처리에서 MEAN_VALUE를 더해주었었으니, 후처리에서 mean_value를 더해줌


output = np.clip(output, 0, 255) #mean_value 처리 후 255 넘는 경우가 있어서, 0-255까지만 값을 허용해줌: clip 함수 사용 
output = output.astype('uint8') #사람이 인식가능한 이미지로 변형

cv2.imshow('output',output)
cv2.imshow('img',img)
cv2.waitKey(0)
