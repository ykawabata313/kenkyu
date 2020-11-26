import cv2
import numpy as np
import matplotlib.pyplot as plt

#画像の読み込み
#imgに三次元のnp.arrayの配列が格納される。
#画像の白い部分のみをグラフにプロットする関数です

def create_graph(file):
    img = plt.imread(file) 

    white = 255
    ans = np.where(img==white)
    x = []
    y = []
    for i in range(0,len(ans[0])):
        x.append(ans[0][i])
        y.append(ans[1][i])

    plt.plot(x, y, marker="o", color = "red", linestyle = "--")

    plt.show()