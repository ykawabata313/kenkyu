import cv2
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import os

from cap import capture
from fix_angle import add_rectangle         #画像に外接矩形を描く関数
from fix_angle import trimming_image        #icチップに着目した画像を作成する関数(第２引数は60前後で調整)
from threshold import thresh                #完成した画像の下処理をする関数(第２引数は200前後で調整)
from pixel import create_graph              #画像からグラフを作成する関数
from match import matching

for i in range(1,5):
    capture()
    img = trimming_image("image/image.jpg")
    cv2.imwrite("u.jpg", img)
    img_comp = thresh("u.jpg")
    cv2.imwrite("image/two_value.jpg", img_comp)
    #create_graph("image/two_value.jpg")
    diff = matching("image/two_value.jpg")
    cv2.imwrite("image/img_compare_sample/diff_false{}.jpg".format(i), diff)

    os.remove("u.jpg")
    os.remove("image/image.jpg")



