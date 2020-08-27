#! python3
# coding: UTF-8

import cv2
import time
import os
import sys
 
camera = cv2.VideoCapture(0)                               # カメラCh.(ここでは0)を指定

#-----保存する動画についての設定-----
# 残しておきたいファイル数を設定する
file_num = 3
#撮影したい回数を設定する
num = 5
# １つの動画の秒数を設定する
set_time = 3

#例外の処理です
if num < file_num:
    print("設定を変更してください。")
    sys.exit()

for i in range(num):
    # 現在時刻を取得
    time_start = time.time()
    # 動画ファイル保存用の設定
    fps = int(camera.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
    w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
    h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
    video = cv2.VideoWriter('video/douga{i}.mp4'.format(i=i), fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

    # 撮影＝ループ中にフレームを1枚ずつ取得
    while True:
        ret, frame = camera.read()                             # フレームを取得
        video.write(frame)                                     # 動画を1フレームずつ保存する
        cv2.imshow('camera', frame)                            # フレームを画面に表示                

        # 設定時刻になればwhileループを抜ける(qキーを押せば強制終了)
        time_finish = time.time()
        passed_time = time_finish - time_start
        if int(passed_time) == int(set_time) or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if i >= file_num:
        os.unlink('video/douga{i}.mp4'.format(i=i-file_num))
    
# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()

#動画の情報を表示
print(fps)
print(w)
print(h)