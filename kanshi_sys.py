import cv2
import time
import tkinter
import numpy as np
from moviepy.editor import *
import os

camera = cv2.VideoCapture(0)

#clickイベント
def btn_click():

    #入力された数値をcountに代入
    global count_mae
    count_mae = int(txt1.get())
    global count_ato
    count_ato = int(txt2.get()) 
    global fps
    buffer = []

    #-----------------------------------------------------------
    # 動画ファイル保存用の設定
    fps = int(camera.get(cv2.CAP_PROP_FPS))                                     # カメラのFPSを取得
    w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))                               # カメラの横幅を取得
    h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))                              #　カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                         # 動画保存時のfourcc設定（mp4用）
    video1 = cv2.VideoWriter('video1.mp4', fourcc, 15, (w, h))                  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    video2 = cv2.VideoWriter('video/after_video.mp4', fourcc, fps, (w, h))      # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    #-----------------------------------------------------------

    #動画の秒数を計算(FPS ×　入力値　＝　描画枚数)
    movie_second_mae = fps * count_mae  
    movie_second_ato = fps * count_ato
    
    #現在撮影中の動画表示プログラム
    while True:
        ret, frame1 = camera.read()
        buffer.append(frame1)
        cv2.imshow("1", frame1)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):                 #qキーを押したところから前と後の動画を保存します
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

#-------------------------------------------------
#UIの設定です。

#画面の設定
root = tkinter.Tk()             # Tkクラス生成
root.geometry('300x200')        # 画面サイズ
root.title('テキストボックス')     #画面タイトル
root.configure(bg='white')

#ラベル
lbl = tkinter.Label(text='movie time setting...')
lbl.place(x=30,y=70)
lbl = tkinter.Label(text='何秒前の動画を残しますか？')
lbl.place(x=30,y=100)
lbl = tkinter.Label(text='何秒後の動画を残しますか？')
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
file_path = 'video1.mp4'
start = 0
end = count_mae
save_path = 'video/before_video.mp4'
video = VideoFileClip(file_path).subclip(start, end)
video.write_videofile(save_path, fps)

# Video1の元動画を削除
os.unlink('video1.mp4')