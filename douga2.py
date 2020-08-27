import cv2
import time
import tkinter
import douga_time

camera = cv2.VideoCapture(0)

if __name__ == '__main__':
    # 動画ファイル保存用の設定
    fps = int(camera.get(cv2.CAP_PROP_FPS))                         # カメラのFPSを取得
    w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))                   # カメラの横幅を取得
    h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))                  # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')             # 動画保存時のfourcc設定（mp4用）
    video1 = cv2.VideoWriter('video1.mp4', fourcc, 15, (w, h))      # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    video2 = cv2.VideoWriter('video2.mp4', fourcc, fps, (w, h))     # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

    buffer = []
    while True:
        ret, frame1 = camera.read()
        if not ret:
            break

        cv2.imshow("1", frame1)
        buffer.append(frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    for i in range(len(buffer)-300 ,len(buffer)):
        frame2 = buffer.pop(i)    
        cv2.imshow("0", frame2)
        buffer.append(frame1)    
        video1.write(frame2)

    start_time = time.time()

    while True:
        ret, frame = camera.read()                             # フレームを取得
        video2.write(frame)                                    # 動画を1フレームずつ保存する
        cv2.imshow('2', frame)                                 # フレームを画面に表示

        finish_time = time.time()
        passed_time = finish_time - start_time                
        if int(passed_time) == 10:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    
    camera.release()
    cv2.destroyAllWindows()

