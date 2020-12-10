import cv2

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
            path = "image.jpg"
            cv2.imwrite(path,frame)
            break

    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()

