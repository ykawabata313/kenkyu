import cv2
import numpy as np

img = cv2.imread("image/circle1.jpg")
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_thre, img_ic = cv2.threshold(img_HSV, 63, 70, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(img_ic, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

for i in range(0, len(contours)):
    if len(contours[i]) > 0:

        # ゴミを取り除く
        if cv2.contourArea(contours[i]) < 100000:
            continue
        
        # 外接矩形を描く
        rect = contours[i]
        x, y, w, h = cv2.boundingRect(rect)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

        # 回転を考慮した外接矩形を描く
        rect = cv2.minAreaRect(contours[i])
        angle = int(rect[2])
        print(rect)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box],0,(0,0,255),2)

        # 最小外接円を描く
        (x,y),radius = cv2.minEnclosingCircle(contours[i])
        center = (int(x),int(y))
        radius = int(radius)
        img = cv2.circle(img,center,radius,(0,255,0),2)



# 回転前の画像を保存
cv2.imwrite('image/add_contour.jpg', img)

# 画像を回転する
height = img.shape[0]
width = img.shape[1]
center = (int(width/2), int(height/2))
scale = 1.0
trans = cv2.getRotationMatrix2D(center, angle, scale)
img2 = cv2.warpAffine(img, trans, (width,height))
cv2.imwrite('image/fixed_angle.jpg', img2)