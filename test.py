import cv2
import time
import tkinter
import numpy as np

camera = cv2.VideoCapture(0)

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,127,0])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,127,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    
    return mask1 + mask2

#clickイベント
def btn_click():

    #入力された数値をcountに代入
    count = txt.get()
    #動画の秒数を計算(30FPS ×　入力値　＝　描画枚数)
    movie_second = 30 * int(count)  

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
        if not ret:
            break

        cv2.imshow("1", frame1)
        buffer.append(frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    

    #数秒前の描写を保存しておくためのプログラム
    for i in range(len(buffer) - movie_second ,len(buffer)):
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

        if int(passed_time) == int(count):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    

    #カメラを開放
    camera.release()
    cv2.destroyAllWindows()

    #ウィンドウを削除
    root.destroy()

def main():
    videofile_path = "video1.mp4"

    # カメラのキャプチャ
    cap = cv2.VideoCapture(videofile_path)
    
    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        # 赤色検出
        mask = red_detect(frame)

        # 結果表示
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    btn_click()
    main()

#画面の設定
root = tkinter.Tk()             # Tkクラス生成
root.geometry('300x200')        # 画面サイズ
root.title('テキストボックス')     #画面タイトル
root.configure(bg='red')

#ラベル
lbl = tkinter.Label(text='time setting...')
lbl.place(x=30,y=70)

#テキストボックス
txt = tkinter.Entry(width=20)
txt.place(x=90,y=100)

# ボタン
btn = tkinter.Button(root, text='start!', command=btn_click)
btn.place(x=130, y=140)

# 表示
root.mainloop()