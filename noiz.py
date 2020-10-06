#-*- coding:utf-8 -*-
import cv2
import numpy as np

# load image (grayscale)
# 入力画像をグレースケールで読み込み
gray = cv2.imread("diff.jpg", 0)

# Spatial filtering
# 方法2
dst = cv2.medianBlur(gray, ksize=1)

# output
# 結果を出力
cv2.imwrite("output.png", dst)
