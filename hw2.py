import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat') #랜드마크모델을 로드하게 하는 method

cap = cv2.VideoCapture(0)
sticker_img = cv2.imread('imgs/pig.png',cv2.IMREAD_UNCHANGED) #오버레이 이미지를 불러올 때는 cv2.IMREAD_UNCHANGED를 적용

while True:
    ret, img = cap.read()

    if ret == False:
        break

    dets = detector(img)

    for det in dets:
        shape = predictor(img, det) #shape안에 landmark 점이 저장됨

        x1 = det.left()
        y1 = det.top()
        x2 = det.right()
        y2 = det.bottom()
        
        h, w, c = sticker_img.shape

        center_x = shape.parts()[4].x
        center_y = shape.parts()[4].y - 10


        nose_w = int((x2-x1) / 4) #코의 크기는 얼굴크기(x2-x1)의 1/4이라고 가정
        nose_h = int(h / w * nose_w) #코의 높이는 가로길이에 비례하도록 

        nose_x1 = int(center_x - nose_w /2) #돼지코의 왼쪽 x1은 돼지코 중심에서 돼지코길이의 1/2만큼 왼쪽으로
        nose_y1 = int(center_y - nose_h /2)

        nose_x2 = nose_x1 + nose_w
        nose_y2 = nose_y1 + nose_h


        overlay_img = sticker_img.copy()
        overlay_img = cv2.resize(overlay_img, dsize=(nose_w, nose_h))

        overlay_alpha = overlay_img[:, :, 3:4] / 255.0
        background_alpha = 1.0 - overlay_alpha

        img[nose_y1:nose_y2, nose_x1:nose_x2] = overlay_alpha * overlay_img[:, :, :3] + background_alpha * img[nose_y1:nose_y2, nose_x1:nose_x2]
        
        # try:
        #     x1 = det.left()
        #     y1 = det.top()
        #     x2 = det.right()
        #     y2 = det.bottom()

        #     cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)
        # except:
        #     pass

    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break