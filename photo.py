# -*- coding: utf-8 -*-
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # フレームをキャプチャする
    ret, frame = cap.read()

    # 画面に表示する
    cv2.imshow('frame',frame)
    
    for i in range(1,100):
        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF
        # sが押された場合は保存する
        if key == ord('s'):
            path = "image/origin/true/t_{}.jpg".format(i)
            cv2.imwrite(path,frame)
        # qが押された場合は終了する
        elif key == ord('q'):
            break

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()