import cv2
import numpy as np

def matching(file):
    img1 = cv2.imread("image/比較元画像/true_two_value.jpg")
    img2 = cv2.imread(file)
    img1 = cv2.resize(img1, dsize=(870, 710))
    img2 = cv2.resize(img2, dsize=(870, 710))

    dst = np.where(img1 >= img2, img1 - img2, 0)

    return dst
