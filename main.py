import cv2
import numpy as np
import os
import openpyxl

'''
画像を撮影するための関数(sキーで撮影、qキーで強制終了)
戻り値はsキーが押された時に撮影していた画像
'''
def capture():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        # 画面に表示する
        cv2.imshow('frame',frame)

        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            #path = "image.jpg"
            #cv2.imwrite(path,frame)
            image = frame
            break

    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()

    return image

'''
撮影した画像の向きと大きさを揃える関数(第１引数は処理したい画像で、第２引数は２値化の閥値)
戻り値はトリミングした画像
'''
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
    img = cv2.warpAffine(img_trim, trans, (2*center_width,2*center_height))

    # 画像を回転後、もう一度トリミング
    img = img[center_height-int(radius) : center_height+int(radius), center_width-int(radius) : center_width+int(radius)]

    return img

'''
画像を２値化する関数(第１引数は処理したい画像で、第２引数は２値化の閥値)
戻り値は2値化された画像
'''
def thresh(file, thresh):
    img = cv2.imread(file, 0)
    # 閾値の設定
    ksize = 9

    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    img_thresh = cv2.medianBlur(img_thresh, ksize)

    return img_thresh

'''
画像の足の曲がりを評価する関数(引数は評価したい画像)
戻り値は差分の画像と評価値
'''
def matching(file):
    img1 = cv2.imread("image/比較元画像/true_two_value.jpg")                      #足の曲がりがない比較元の画像
    img2 = cv2.imread(file)                                                     #比較対象の画像
    x = []                                                                      

    #画像の処理をするために２つの画像サイズを一緒にする
    x_trim = (img1.shape[0]+img2.shape[0])/2
    y_trim = (img1.shape[1]+img2.shape[1])/2
    img1 = cv2.resize(img1, dsize=(int(x_trim), int(y_trim)))
    img2 = cv2.resize(img2, dsize=(int(x_trim), int(y_trim)))

    #img2をx,y方向に1pixずつずらしていき、２枚の画像の差分が最小になる場所を探索する
    for m in range(-5,5):
        img2_shift1 = img2
        img2_shift1 = np.roll(img2_shift1,m,axis=1)
        for n in range(-5,5):
            img2_shift2 = img2_shift1
            img2_shift2 = np.roll(img2_shift2,n,axis=0)
            dst = np.where(img1 >= img2_shift2, img1 - img2_shift2, 0)
            x.append(np.count_nonzero(dst==255))

    #差分の画像を出力する処理
    x_index = x.index(min(x))
    x_shift = int(x_index/10)-5
    y_shift = int(str(x_index)[-1])-5
    img2 = np.roll(img2,x_shift,axis=1)     #x軸方向にシフト
    img2 = np.roll(img2,y_shift,axis=0)     #y軸方向にシフト
    dst = np.where(img1 >= img2, img1 - img2, 0)    #差分の画像(2値)

    judge_num = min(x)

    return dst, judge_num

'''
ICを評価する関数
'''
def judgement(file,num):
    img = cv2.imread(file)
    #足が折れていない時の処理
    if num < 3800:
        print(num)
        print("足は曲がっていないです")
    #足が折れている時の処理
    elif num >= 3800:
        print(num)
        print("足が曲がっています")

def main():
    img = capture()
    cv2.imwrite("cap.jpg", img)
    img_trim = trimming_image("cap.jpg", 35)
    cv2.imwrite("trim.jpg", img_trim)
    img_thresh = thresh("trim.jpg", 210)
    cv2.imwrite("thresh.jpg", img_thresh)
    judge = matching("thresh.jpg")
    cv2.imwrite("judge.jpg", judge[0])
    judgement("judge.jpg", judge[1])

    os.remove("cap.jpg")
    os.remove("trim.jpg")
    os.remove("thresh.jpg")
    os.remove("judge.jpg")

if __name__ == "__main__":
    main()