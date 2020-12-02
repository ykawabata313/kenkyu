import cv2
import numpy as np
import sys
import time
import matplotlib.pyplot as plt

from photo import capture                   #画像を保存する関数
from fix_angle import add_rectangle         #画像に外接矩形を描く関数
from fix_angle import trimming_image        #icチップに着目した画像を作成する関数(第２引数は60前後で調整)
from threshold import thresh                #完成した画像の下処理をする関数(第２引数は200前後で調整)
from pixel import create_graph              #画像からグラフを作成する関数

img1 = trimming_image("image/false.jpg")
cv2.imwrite("u.jpg", img1)
img = thresh("u.jpg")
cv2.imwrite("i.jpg", img)
create_graph("i.jpg")

