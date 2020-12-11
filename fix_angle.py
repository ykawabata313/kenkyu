import cv2
import numpy as np

def trimming_image(file,thresh=35):

    # 画像によっていい感じの値に変えてください(光の加減などによっていろいろ変わってしまいます)
    ksize = 5

    img = cv2.imread(file)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _thre, img_ic = cv2.threshold(img_HSV, thresh, 255, cv2.THRESH_BINARY_INV)
    img_ic = cv2.medianBlur(img_ic, ksize)
    contours, hierarchy = cv2.findContours(img_ic, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:

            # ゴミを取り除く
            if cv2.contourArea(contours[i]) < 50000:
                    continue
            
            # 回転を考慮した外接矩形を描く
            rect = cv2.minAreaRect(contours[i])
            angle = rect[2]                                         #ICの傾きの角度
            box = cv2.boxPoints(rect)
            box = np.int0(box)         

            # 最小外接円を描く
            (x,y),radius = cv2.minEnclosingCircle(contours[i])
            circle_center = (int(x),int(y))                         #外接円の中心座標(x,y)
            radius = int(radius)                                    #外接円の半径

            #画像内に輪郭を付けたいときはこの処理をする
            #img = cv2.circle(img,circle_center,radius,(0,255,0),4)
            #cv2.drawContours(img, [box],0,(0,0,255),4) 
    
    if angle >= 45 or angle <= -45:
        angle += 90

    center_x = circle_center[0] 
    center_y = circle_center[1]

    # ICを中心に画像をトリミング
    img_trim = img[center_y-radius : center_y+radius, center_x-radius : center_x+radius]

    # トリミング後、画像を回転
    center_height = int(img_trim.shape[0]/2)
    center_width = int(img_trim.shape[1]/2)
    center = (center_width, center_height)
    scale = 1.0
    trans = cv2.getRotationMatrix2D(center, angle, scale)
    img2 = cv2.warpAffine(img_trim, trans, (2*center_width,2*center_height))

    # 画像を回転後、もう一度トリミング
    img3 = img2[center_height-int(radius) : center_height+int(radius), center_width-int(radius) : center_width+int(radius)]

    return img3

