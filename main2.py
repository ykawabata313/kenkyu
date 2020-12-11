import cv2
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import os
import openpyxl

from cap import capture
from fix_angle import trimming_image        #icチップに着目した画像を作成する関数(第２引数は35前後で環境によって調整)
from threshold import thresh                #完成した画像の下処理をする関数(第２引数は200前後で環境によって調整)
from match import matching                  #正誤判定する関数

def main():
    book = openpyxl.load_workbook("judge_chart.xlsx")
    sheet = book['Sheet1']

    capture()
    img = trimming_image("image.jpg", 35)
    cv2.imwrite("u.jpg", img)
    img_comp = thresh("u.jpg", 210)
    cv2.imwrite("image/two_value.jpg", img_comp)
    diff = matching("image/two_value.jpg")
    cv2.imwrite("image/img_sample/true8.jpg", diff[0])
    judge = diff[1]

    #sheet['A{}'.format(i+1)] = i
    sheet['b9'] = judge
    book.save('judge_chart.xlsx')

    os.remove("u.jpg")
    os.remove("image.jpg")

if __name__ == "__main__":
    main()



