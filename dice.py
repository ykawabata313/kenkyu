#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2

def dice_chacker(origin_image,compare_image):
    # 1.比較元イメージを読み込む
    # 比較元画像
    origin_image = cv2.imread(origin_image)
    # 比較したい画像
    compare_image = cv2.imread(compare_image)

    # 3.比較する
    orb = cv2.ORB_create()
    kpOk, desOk = orb.detectAndCompute(origin_image, None)
    kpTa, desTa = orb.detectAndCompute(compare_image, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desOk, desTa)
    matches = sorted(matches, key = lambda x:x.distance)
    dist = [m.distance for m in matches]

    # 4.比較結果を出力する
    print(sum(dist) / len(dist))
    coImage = cv2.drawMatches(origin_image,kpOk,compare_image,kpTa,matches[:10], None, flags=2)
    cv2.imwrite("image/match.jpg", coImage)

