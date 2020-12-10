import cv2
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import os

from cap import capture
from fix_angle import add_rectangle         #画像に外接矩形を描く関数
from fix_angle import trimming_image        #icチップに着目した画像を作成する関数(第２引数は35前後で環境によって調整)
from threshold import thresh                #完成した画像の下処理をする関数(第２引数は200前後で環境によって調整)
from match import matching                  #正誤判定する関数
#from pixel import create_graph              #画像からグラフを作成する関数


capture()
img = trimming_image("image.jpg", 35)
cv2.imwrite("u.jpg", img)
img_comp = thresh("u.jpg", 210)
cv2.imwrite("image/two_value.jpg", img_comp)
diff = matching("image/two_value.jpg")
cv2.imwrite("image/img_sample/diff_false.jpg", diff)

os.remove("u.jpg")
os.remove("image.jpg")



