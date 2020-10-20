import cv2
import numpy as np

net = cv2.dnn.readNetFromTorch('models/instance_norm/mosaic.t7')
net2 = cv2.dnn.readNetFromTorch('models/instance_norm/the_scream.t7')
net3 = cv2.dnn.readNetFromTorch('models/instance_norm/candy.t7')
net4 = cv2.dnn.readNetFromTorch('models/instance_norm/feathers.t7')

img = cv2.imread('imgs/03.jpg')

h, w, c = img.shape

img = cv2.resize(img, dsize=(500, int(h / w * 500)))
print(img.shape)

MEAN_VALUE = [103.939, 116.779, 123.680]
blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

#1번째 이미지 후처리
net.setInput(blob)
output = net.forward()

output = output.squeeze().transpose((1, 2, 0))

output += MEAN_VALUE
output = np.clip(output, 0, 255)
output = output.astype('uint8')

#2번째 이미지 후처리
net2.setInput(blob)
output2 = net2.forward()

output2 = output2.squeeze().transpose((1, 2, 0))

output2 = output2 + MEAN_VALUE
output2 = np.clip(output2, 0, 255)
output2 = output2.astype('uint8')

#3번째 이미지 후처리
net3.setInput(blob)
output3 = net3.forward()

output3 = output3.squeeze().transpose((1, 2, 0))

output3 = output3 + MEAN_VALUE
output3 = np.clip(output3, 0, 255)
output3 = output3.astype('uint8')

#4번째 이미지 후처리
net4.setInput(blob)
output4 = net4.forward()

output4 = output4.squeeze().transpose((1, 2, 0))

output4 = output4 + MEAN_VALUE
output4 = np.clip(output4, 0, 255)
output4 = output4.astype('uint8')


output_c1 = output[:157, :250] #가로 크기가 500이니까 X축만 잘라줌
output_c2 = output2[:157, 250:500] 
output_c3 = output3[157:, :250] 
output_c4 = output4[157:, 250:500] 

output_f1 = np.concatenate([output_c1, output_c3], axis=0)
output_f2 = np.concatenate([output_c2, output_c4], axis=0)
print(output_f1.shape)
print(output_f2.shape)
output_f2 = cv2.resize(output_f2, dsize=(250, 316))
print(output_f2.shape)
output_ff = np.concatenate([output_f1, output_f2], axis=1)
#axis = 1 이란 axis 방향으로 합쳐주세요 ! 1은 x 축 방향

cv2.imshow('img', img)

cv2.imshow('output_ff',output_ff)

cv2.waitKey(0)
