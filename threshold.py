import cv2

def thresh(file):
    img = cv2.imread(file, 0)
    # 閾値の設定
    threshold = 170
    ksize = 9

    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    img_thresh = cv2.medianBlur(img_thresh, ksize)

    #cv2.imwrite("image/tt.jpg", img_thresh)

    return img_thresh

#thresh("image/true.jpg")