import cv2
import time
import datetime
import tkinter
import numpy as np
from moviepy.editor import *
import os
import datetime
import math
##import RPi.GPIO as GPIO

camera = cv2.VideoCapture(0)
#エラー検出をするピンの設定
##GPIO.setmode(GPIO.BCM)
##GPIO.setup(3, GPIO.IN)
now = datetime.datetime.now()
file_name = 'video/' + now.strftime('%Y%m%d_%H%M%S') + '_ato' + '.mp4'
#clickイベント
def btn_click():
    
    #入力された数値をcountに代入
    global count_mae
    count_mae = int(txt1.get())
    global count_ato
    count_ato = int(txt2.get()) 
    global fps
    global movie_scale
    global video_num
    movie_scale = 1

    #-----------------------------------------------------------
    # 動画ファイル保存用の設定
    fps = int(camera.get(cv2.CAP_PROP_FPS))                                     # カメラのFPSを取得
    w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))                               # カメラの横幅を取得
    h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))                              #　カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                         # 動画保存時のfourcc設定（mp4用）
    #video1 = cv2.VideoWriter('video1.mp4', fourcc, fps/movie_scale, (w, h))     # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    video2 = cv2.VideoWriter(file_name, fourcc, fps/movie_scale, (w, h))        # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    #-----------------------------------------------------------

    #動画の秒数を計算(FPS ×　入力値　＝　描画枚数)
    frame_num = fps * count_mae

    flg = False
    
    #現在撮影中の動画表示プログラム
    for i in range(1,99999999):
        start_time = datetime.datetime.now().second
        video1 = cv2.VideoWriter('video{}.mp4'.format(i), fourcc, fps/movie_scale, (w, h))
        video_num = i
        while True:
            ret, frame1 = camera.read()
            cv2.imshow("1", frame1)
            video1.write(frame1)
            now_time = datetime.datetime.now().second
            time1 = now_time-start_time
            time2 = start_time-now_time
            if time1 == 30 or time2 == 30:
                os.unlink("video{}.mp4".format(i))
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):                 #qキーを押したところから前と後の動画を保存します
                flg = True
                break
        if flg:
            break
        
        #if GPIO.input(3) == GPIO.LOW:
            #break
        
        
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
    
    #GPIO.cleanup()
    
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
lbl = tkinter.Label(text='何秒前の動画？')
lbl.place(x=30,y=100)
lbl = tkinter.Label(text='何秒後の動画？')
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

file_name = 'video/' + now.strftime('%Y%m%d_%H%M%S') + '_mae' + '.mp4'

# Vieo1の動画時間をカットして修正
cap = cv2.VideoCapture("video{}.mp4".format(video_num))
video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
video_len_sec = movie_scale * video_frame_count / fps
start = video_len_sec - count_mae
end = video_len_sec
video = VideoFileClip('video{}.mp4'.format(video_num)).subclip(start, end)
video.write_videofile(file_name, fps)

# Video1の元動画を削除
os.unlink('video{}.mp4'.format(video_num))