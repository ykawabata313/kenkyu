import cv2

def thresh(file):
    # 画像の読み込み
    img = cv2.imread(file, 0)
    # 閾値の設定
    threshold = 210

    ksize = 11

    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    img_thresh = cv2.medianBlur(img_thresh, ksize)

    return img_thresh

#for i in range(1,5):
    #img = thresh("image/fixed_{}.jpg".format(i))
    #cv2.imwrite("image/true{}.jpg".format(i+2), img)

img = thresh("image/t__1.jpg")
cv2.imwrite("image/aaa.jpg", img)

