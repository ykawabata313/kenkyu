# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

i = 100
while i < 200:
    # フレームをキャプチャする
    ret, frame = cap.read()

    # 画面に表示する
    cv2.imshow('frame',frame)
    path = "image/origin/false/f_{}.jpg".format(i)
    cv2.imwrite(path,frame)
    time.sleep(0.5)
    i+=1
    # キーボード入力待ち
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()