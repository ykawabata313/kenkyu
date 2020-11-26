import cv2
import numpy as np
import matplotlib.pyplot as plt

#画像の読み込み
#imgに三次元のnp.arrayの配列が格納される。
img = plt.imread('image/aaa.jpg') 

white = 255
ans = np.where(img==white)
x = []
y = []
for i in range(0,len(ans[0])):
    x.append(ans[0][i])
    y.append(ans[1][i])

plt.plot(x, y, marker="o", color = "red", linestyle = "--")

plt.show()