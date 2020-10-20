import cv2
import numpy as np

net = cv2.dnn.readNetFromTorch('models/instance_norm/mosaic.t7')
#torch로 만들어진 모델을 로드하여, net에 저장함

img = cv2.imread('imgs/hw.jpg')

h, w, c = img.shape #이미지의 형태를 높이, 너비, 채널로 나타냄

cropped_img = img[146:369, 479:815]
#이미지 자르기 [ y 축 범위 : x축 범위]
print(cropped_img.shape) 

MEAN_VALUE = [103.939, 116.779, 123.680]
blob = cv2.dnn.blobFromImage(cropped_img, mean=MEAN_VALUE)
#blobFromImage 전처리하는 함수 img각 값에서 mean value를 빼줌
#blobFromImage 차원 변형을 지원 : 딥러닝 모델에 넣기 전에 차원 변형을 꼭 해줘야함
print(blob.shape)
#(1, 3, 325, 500) 로 바뀌면서, 차원이 앞으로 오도록 변형

net.setInput(blob)
output = net.forward()
#컴퓨터만 알 수 있는 형태니까, 후처리를 해줘야함

output = output.squeeze().transpose((1, 2, 0))
#전처리에서 차원을 늘렸으니, 차원을 줄이는 squeeze
#차원을 다시 변형해주는 transpose
output += MEAN_VALUE
#전처리에서 MEAN_VALUE를 더해주었었으니, 후처리에서 mean_value를 더해줌

output = np.clip(output, 0, 255) #mean_value 처리 후 255 넘는 경우가 있어서, 0-255까지만 값을 허용해줌: clip 함수 사용 
output = output.astype('uint8') #사람이 인식가능한 이미지로 변형


img[146:370, 479:815] = output 
#이미지 끼워넣기! 
# 1. 바꿀이미지를 cropped_img로 저장해서, 
# 2. blob 처리 -> 후처리 후 output 으로 따로 저장 
# 3. 끼워넣어지는 배경 사진에서 cropped_img의 크기를 맞춰줘야함. 관련 오류: "could not broadcast input array from shape (224,336,3) into shape (223,336,3)""
# 4. 기존 이미지중에서 바꿀 부분을 output으로 바꿔줌 

cv2.imshow('output',output)
cv2.imshow('img',img)
cv2.waitKey(0)

