import cv2
import numpy as np
import matplotlib.pyplot as plt

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
