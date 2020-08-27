import cv2
import time
import tkinter
import numpy as np

camera = cv2.VideoCapture(0)

#clickイベント
def btn_click():

    #入力された数値をcountに代入
    count_mae = txt1.get()
    count_ato = txt2.get()
    #動画の秒数を計算(30FPS ×　入力値　＝　描画枚数)
    movie_second_mae = 30 * int(count_mae)  
    movie_second_ato = 30 * int(count_ato)

    buffer = []

    #-----------------------------------------------------------
    # 動画ファイル保存用の設定
    fps = int(camera.get(cv2.CAP_PROP_FPS))                         # カメラのFPSを取得
    w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))                   # カメラの横幅を取得
    h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))                  # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')             # 動画保存時のfourcc設定（mp4用）
    video1 = cv2.VideoWriter('video1.mp4', fourcc, 15, (w, h))      # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    video2 = cv2.VideoWriter('video2.mp4', fourcc, fps, (w, h))     # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    #-----------------------------------------------------------

    
    #現在撮影中の動画表示プログラム
    while True:
        ret, frame1 = camera.read()

        # フレームをHSVに変換
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        # 取得する色の範囲を指定する
        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([100, 255, 255])
        # 指定した色に基づいたマスク画像の生成
        img_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # フレーム画像とマスク画像の共通の領域を抽出する。
        img_color = cv2.bitwise_and(frame1, frame1, mask=img_mask)

        cv2.imshow("1", frame1)
        cv2.imshow("Color Image", img_color)

        buffer.append(frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
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
        video2.write(frame)                                    # 動画を1フレームずつ保存する
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