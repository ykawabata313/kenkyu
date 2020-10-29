import cv2
import numpy as np

def add_rectangle(file):

    # 画像によっていい感じの値に変えてください(光の加減などによっていろいろ変わってしまいます)
    thresh = 63
    thresh_max = 70

    img = cv2.imread(file)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _thre, img_ic = cv2.threshold(img_HSV, thresh, thresh_max, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(img_ic, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:

            # ゴミを取り除く
            if cv2.contourArea(contours[i]) < 100000:
                continue

            # 回転を考慮した外接矩形を描く
            rect = cv2.minAreaRect(contours[i])
            angle = int(rect[2])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box],0,(0,0,255),4)

            # 最小外接円を描く
            (x,y),radius = cv2.minEnclosingCircle(contours[i])
            circle_center = (int(x),int(y))
            radius = int(radius)
            img = cv2.circle(img,circle_center,radius,(0,255,0),4)

    return angle, circle_center, radius, img, rect


def trimming_image(file):
    # 矩形描写関数の呼び込み
    result = add_rectangle(file)

    # 画像の回転角
    angle = result[0]
    # ICの中心座標
    center_locate = result[1]
    x = center_locate[0]
    y = center_locate[1]
    # 最小外接円の半径
    radius = result[2]
    # 画像のデータ
    img = result[3]

    # 外接矩形の幅と高さを取得
    rect = result[4]
    w = rect[1][0]
    h = rect[1][1]

    # ICを中心に画像をトリミング(余裕を持って+-100)
    img_trim = img[y-radius-100 : y+radius+100, x-radius-100 : x+radius+100]

    # トリミング後、画像を回転
    center_height = int(img_trim.shape[0]/2)
    center_width = int(img_trim.shape[1]/2)
    center = (center_width, center_height)
    scale = 1.0
    trans = cv2.getRotationMatrix2D(center, angle, scale)
    img2 = cv2.warpAffine(img_trim, trans, (2*center_width,2*center_height))

    # 画像を回転後、もう一度トリミング
    img3 = img2[center_height-int((h/2))-30 : center_height+int((h/2))+30, center_width-int((w/2))-200 : center_width+int((w/2))+200]
    cv2.imwrite("image/fixed_angle.jpg", img3)

trimming_image("image/origin1.jpg")

