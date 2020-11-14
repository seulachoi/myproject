import cv2

#super Resolution : 초해상도모델, edsr 은 해상도 3배 모델
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel('models/EDSR_x3.pb')
sr.setModel('edsr', 3)

img = cv2.imread('imgs/06.jpg')

result = sr.upsample(img) #이미지 3배 늘린것을 결과에 입력해

#3배씩 늘려주세요
resized_img = cv2.resize(img, dsize = None, fx=3, fy=3)

cv2.imshow('img', img)
cv2.imshow('result', result)
cv2.imshow('resized_img', resized_img)
cv2.waitKey(0)



