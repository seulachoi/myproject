import cv2
import numpy as np

#모델 로드하기 : 모델 튜닝과정
proto = 'models/colorization_deploy_v2.prototxt'
weights = 'models/colorization_release_v2.caffemodel'

#딥러닝 프레임워크 readNetFromCaffe
net = cv2.dnn.readNetFromCaffe(proto, weights)

pts_in_hull = np.load('models/pts_in_hull.npy')
pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1).astype(np.float32)
net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull]

net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full((1, 313), 2.606, np.float32)]

#이미지 사진 전처리하기
img = cv2.imread('imgs/05.jpg')

h, w, c = img.shape #이미지 높이 너비 채널 저장해두기

img_input = img.copy() #이미지 복사해서 img_input에 저장

img_input = img_input.astype('float32') / 255. # 정수형을 float32는 소수점32형태로 바꾸어라
img_lab = cv2.cvtColor(img_input, cv2.COLOR_BGR2Lab)
img_l = img_lab[:, :, 0:1]

blob = cv2.dnn.blobFromImage(img_l, size=(224, 224), mean=[50, 50, 50])

net.setInput(blob)
output = net.forward()

#결과추론을 인간이 이해할 수 있는 형태로 바꾸는 후처리! 
output = output.squeeze().transpose((1,2,0))

output_resized = cv2.resize(output, (w, h)) #전처리과정에서 사이즈를 224로 조정했으니, 원본 이미지의 사이즈로 다시 되돌리기

output_lab = np.concatenate([img_l, output_resized], axis=2)

output_bgr = cv2.cvtColor(output_lab, cv2.COLOR_Lab2BGR)
output_bgr = output_bgr * 255
output_bgr = np.clip(output_bgr, 0, 255)
output_bgr = output_bgr.astype('uint8')


mask = np.zeros_like(img, dtype='uint8') #이미지와 같은 형태로, 0으로 채운 이미지를 만들어! 즉 검정색 이미지
mask=cv2.rectangle(mask, pt1=(200,100), pt2=(400,350), color=(1,1,1), thickness=-1)
#mask = cv2.circle(mask, center =(260,260), radius=200, color=(1,1,1), thickness=-1)

color = output_bgr * mask #마스크처리한 원 부분에 output_bgr로 컬러를 입힘
gray = img * (1 - mask) #1-mask로 이미지를 반전시킴.

output2 = color + gray

cv2.imshow('result2', output2)


cv2.imshow('img', img)
cv2.imshow('output', output_bgr)
cv2.waitKey(0)


