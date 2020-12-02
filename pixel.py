import cv2
import numpy as np
import matplotlib.pyplot as plt

#画像の読み込み
#imgに三次元のnp.arrayの配列が格納される。

def create_graph(file):
    img = plt.imread(file) 

    white = 255
    point = np.where(img==white)                #ICの足の部分の画素値の座標をタプルpoint((x),(y))にいれる
    x = point[0]
    y = point[1]
    x_min = []
    x_max = []
    y_min = np.where(y == y.min()+20)           #Y座標の最小値から20上の場所の配列yのインデックス値をy_minにいれる
    y_max = np.where(y == y.max()-20)           #Y座標の最大値から20下の場所の配列yのインデックス値をy_maxにいれる

    for i in y_min:
        x_min.append(x[i])
    
    for i in y_max:
        x_max.append(x[i])

    #plt.scatter(x, y, c="green")
    #plt.ylim(20,min(y)+50)
    #plt.savefig("image/t")

    l = [-1] * len(x_min[0])
    m = [1] * len(x_max[0])
    plt.scatter(x_min, l, c="red")
    plt.scatter(x_max, m,  c="yellow")
    plt.show()