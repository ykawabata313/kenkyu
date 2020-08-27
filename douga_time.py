import tkinter

#clickイベント
def btn_click():
    count = txt.get()
    print(count)

#画面の設定
root = tkinter.Tk()             # Tkクラス生成
root.geometry('300x200')        # 画面サイズ
root.title('テキストボックス')     #画面タイトル

#ラベル
lbl = tkinter.Label(text='動画の時間を数値で入力してください')
lbl.place(x=30,y=70)

#テキストボックス
txt = tkinter.Entry(width=20)
txt.place(x=90,y=100)

# ボタン
btn = tkinter.Button(root, text='スタート', command=btn_click)
btn.place(x=130, y=140)

# 表示
root.mainloop()