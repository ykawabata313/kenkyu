import cv2
import time
import tkinter
import numpy as np
from moviepy.editor import *
import os
import openpyxl

'''
画像を撮影するための関数(sキーで撮影、qキーで強制終了)
戻り値はsキーが押された時に撮影していた画像
'''
def capture():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        # 画面に表示する
        cv2.imshow('frame',frame)

        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            #path = "image.jpg"
            #cv2.imwrite(path,frame)
            image = frame
            break

    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()

    return image

'''
撮影した画像の向きと大きさを揃える関数(第１引数は処理したい画像で、第２引数は２値化の閥値)
戻り値はトリミングした画像
'''
def trimming_image(file,thresh=35):

    # 画像によっていい感じの値に変えてください(光の加減などによっていろいろ変わってしまいます)
    ksize = 5

    img = cv2.imread(file)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _thre, img_ic = cv2.threshold(img_HSV, thresh, 255, cv2.THRESH_BINARY_INV)
    img_ic = cv2.medianBlur(img_ic, ksize)
    contours, hierarchy = cv2.findContours(img_ic, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:

            # ゴミを取り除く
            if cv2.contourArea(contours[i]) < 50000:
                    continue
            
            # 回転を考慮した外接矩形を描く
            rect = cv2.minAreaRect(contours[i])
            angle = rect[2]                                         #ICの傾きの角度
            box = cv2.boxPoints(rect)
            box = np.int0(box)         

            # 最小外接円を描く
            (x,y),radius = cv2.minEnclosingCircle(contours[i])
            circle_center = (int(x),int(y))                         #外接円の中心座標(x,y)
            radius = int(radius)                                    #外接円の半径

            #画像内に輪郭を付けたいときはこの処理をする
            #img = cv2.circle(img,circle_center,radius,(0,255,0),4)
            #cv2.drawContours(img, [box],0,(0,0,255),4) 
    
    if angle >= 45 or angle <= -45:
        angle += 90

    center_x = circle_center[0] 
    center_y = circle_center[1]

    # ICを中心に画像をトリミング
    img_trim = img[center_y-radius : center_y+radius, center_x-radius : center_x+radius]

    # トリミング後、画像を回転
    center_height = int(img_trim.shape[0]/2)
    center_width = int(img_trim.shape[1]/2)
    center = (center_width, center_height)
    scale = 1.0
    trans = cv2.getRotationMatrix2D(center, angle, scale)
    img = cv2.warpAffine(img_trim, trans, (2*center_width,2*center_height))

    # 画像を回転後、もう一度トリミング
    img = img[center_height-int(radius) : center_height+int(radius), center_width-int(radius) : center_width+int(radius)]

    return img

'''
画像を２値化する関数(第１引数は処理したい画像で、第２引数は２値化の閥値)
戻り値は2値化された画像
'''
def thresh(file, thresh):
    img = cv2.imread(file, 0)
    # 閾値の設定
    ksize = 9

    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    img_thresh = cv2.medianBlur(img_thresh, ksize)

    return img_thresh

'''
画像の足の曲がりを評価する関数(引数は評価したい画像)
戻り値は差分の画像と評価値
'''
def matching(file):
    img1 = cv2.imread("image/比較元画像/true_two_value.jpg")                      #足の曲がりがない比較元の画像
    img2 = cv2.imread(file)                                                     #比較対象の画像
    x = []                                                                      

    #画像の処理をするために２つの画像サイズを一緒にする
    x_trim = (img1.shape[0]+img2.shape[0])/2
    y_trim = (img1.shape[1]+img2.shape[1])/2
    img1 = cv2.resize(img1, dsize=(int(x_trim), int(y_trim)))
    img2 = cv2.resize(img2, dsize=(int(x_trim), int(y_trim)))

    #img2をx,y方向に1pixずつずらしていき、２枚の画像の差分が最小になる場所を探索する
    for m in range(-5,5):
        img2_shift1 = img2
        img2_shift1 = np.roll(img2_shift1,m,axis=1)
        for n in range(-5,5):
            img2_shift2 = img2_shift1
            img2_shift2 = np.roll(img2_shift2,n,axis=0)
            dst = np.where(img1 >= img2_shift2, img1 - img2_shift2, 0)
            x.append(np.count_nonzero(dst==255))

    #差分の画像を出力する処理
    x_index = x.index(min(x))
    x_shift = int(x_index/10)-5
    y_shift = int(str(x_index)[-1])-5
    img2 = np.roll(img2,x_shift,axis=1)     #x軸方向にシフト
    img2 = np.roll(img2,y_shift,axis=0)     #y軸方向にシフト
    dst = np.where(img1 >= img2, img1 - img2, 0)    #差分の画像(2値)

    judge_num = min(x)

    return dst, judge_num

'''
ICを評価する関数
'''
def judgement(file,num):
    img = cv2.imread(file)
    #足が折れていない時の処理
    if num < 3800:
        return True,num
    #足が折れている時の処理
    elif num >= 3800:
        return False,num

def main():
    camera = cv2.VideoCapture(1)
    def btn_click():

        #入力された数値をcountに代入
        global count_mae
        count_mae = int(txt1.get())
        global count_ato
        count_ato = int(txt2.get())
        #動画の秒数を計算(29FPS ×　入力値　＝　描画枚数)
        movie_second_mae = 29 * count_mae  
        movie_second_ato = 29 * count_ato

        buffer = []

        #-----------------------------------------------------------
        # 動画ファイル保存用の設定
        fps = int(camera.get(cv2.CAP_PROP_FPS))                         # カメラのFPSを取得
        w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))                   # カメラの横幅を取得
        h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))                  # カメラの縦幅を取得
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')             # 動画保存時のfourcc設定（mp4用）
        video1 = cv2.VideoWriter('video/video1.mp4', fourcc, 15, (w, h))      # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
        video2 = cv2.VideoWriter('video/video2.mp4', fourcc, fps, (w, h))     # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
        #-----------------------------------------------------------

        
        #現在撮影中の動画表示プログラム
        while True:
            ret, frame1 = camera.read()
            buffer.append(frame1)
            cv2.imshow("1", frame1)    
            if cv2.waitKey(1) & 0xFF == ord('s'): 
                ic_img = frame1
                cv2.imwrite("cap.jpg", ic_img)
                img_trim = trimming_image("cap.jpg", 35)
                os.remove("cap.jpg")#
                cv2.imwrite("trim.jpg", img_trim)
                img_thresh = thresh("trim.jpg", 210)
                os.remove("trim.jpg")#
                cv2.imwrite("thresh.jpg", img_thresh)
                judge = matching("thresh.jpg")
                os.remove("thresh.jpg")#
                cv2.imwrite("judge.jpg", judge[0])
                point = judgement("judge.jpg", judge[1])
                if point[0]:
                    print(point[1])
                    print("足は曲がっていないです")
                    os.remove("judge.jpg")

                else:
                    print(point[1])
                    print("足が曲がっています")
                    break
                
        #数秒前の描写を保存しておくためのプログラム
        for i in range(len(buffer) - movie_second_mae ,len(buffer)):
            frame2 = buffer.pop(i)    
            cv2.imshow("0", frame2)                
            buffer.append(frame1)                                     
            video1.write(frame2)                                   #動画１を保存 

        start_time = time.time()

            #動画２の撮影と保存用プログラム
        while True:
            ret, frame = camera.read()                             # フレームを取得
            video2.write(frame)                                    # 動画2を1フレームずつ保存する
            cv2.imshow('2', frame)                                 # フレームを画面に表示

            finish_time = time.time()
            passed_time = finish_time - start_time

            if int(passed_time) == int(count_ato):
                break
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
        

        #カメラを開放
        camera.release()
        cv2.destroyAllWindows()

        #ウィンドウを削除
        root.destroy()

    #画面の設定
    root = tkinter.Tk()             # Tkクラス生成
    root.geometry('300x200')        # 画面サイズ
    root.title('テキストボックス')     #画面タイトル
    root.configure(bg='red')

    #ラベル
    lbl = tkinter.Label(text='movie time setting...')
    lbl.place(x=30,y=70)
    lbl = tkinter.Label(text='何秒前の動画が欲しい？')
    lbl.place(x=30,y=100)
    lbl = tkinter.Label(text='何秒後の動画が欲しい？')
    lbl.place(x=30,y=130)

    #テキストボックス
    txt1 = tkinter.Entry(width=5)
    txt1.place(x=180,y=100)
    txt2 = tkinter.Entry(width=5)
    txt2.place(x=180,y=130)

    # ボタン
    btn = tkinter.Button(root, text='start!', command=btn_click)
    btn.place(x=130, y=160)

    # 表示
    root.mainloop()
    #-------------------------------------------------


    # Vieo1の動画時間をカットして修正
    file_path = 'video/video1.mp4'
    start = 0
    end = count_mae
    save_path = 'video/video1_re.mp4'
    video = VideoFileClip(file_path).subclip(start, end)
    video.write_videofile(save_path, fps=29)

    # Video1の元動画を削除
    os.unlink('video/video1.mp4')

if __name__ == "__main__":
    main()