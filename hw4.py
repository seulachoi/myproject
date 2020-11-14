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


#super Resolution : 초해상도모델, edsr 은 해상도 3배 모델
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel('models/EDSR_x4.pb')
sr.setModel('edsr', 4)

img = cv2.imread('imgs/07.jpg')

resized_img = cv2.resize(img, dsize=None, fx = 1/4, fy = 1/4)

result = sr.upsample(img) #이미지 4배 늘린것을 결과에 입력해

h, w, c = result.shape #이미지 높이 너비 채널 저장해두기

img_input = result.copy() #이미지 복사해서 img_input에 저장

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


cv2.imshow('img', img)
cv2.imshow('result', result)
cv2.imshow('resized_img', resized_img)
cv2.imshow('output', output_bgr)
cv2.waitKey(0)



