import tkinter as tk
from tkinter import ttk
from tkinter import font

from PIL import Image, ImageTk


import cv2
import numpy as np


class Model:
    """Webcam関連
    1. カメライメージの取得
    2. QRコードをハイライト
    3. QRコードの値を取得
    4. カメラ解放
    """

    def __init__(self):
        """load webcams's config which is setting.json.
        1. load setting.json.
        2. create instance variables.
        """

        # カメラ起動
        self.aruco = cv2.aruco
        self.dictionary = self.aruco.getPredefinedDictionary(self.aruco.DICT_4X4_50)

        # CAP_DSHOWを設定すると、終了時のterminating async callbackのエラーは出なくなる
        # ただし場合によっては、フレームレートが劇遅になる可能性あり
        # self.cap = cv2.VideoCapture(self.camera_setting["CAM"]["ID"], cv2.CAP_DSHOW)
        self.cap = cv2.VideoCapture(0)

        # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

        # 表示内容の初期化
        self.qr_text = [self.cap.get(i) for i in range(20)]


class View:
    """tkinter関連
    """

    def __init__(self, master, model):
        """create widget objects
        1. setiing of font
        2. create menu objects
        3. create frames objects and others
        4. use grid()
        Args:
            master (class): main window
            model (class): Webcam related
        """
        # インスタンス化
        self.master = master
        self.model = model

        style = ttk.Style()
        style.theme_use("vista")

        # フォントの設定
        # ラベルフレーム用
        style.configure("font.TLabelframe", font=30)
        # ボタン用
        style.configure("font.TButton", font=80)

        # フレーム設定
        self.frame1 = ttk.LabelFrame(self.master, text="カメラ画像", style="font.TLabelframe", relief=tk.GROOVE)
        self.frame2 = ttk.LabelFrame(self.master, text="コマンド", style="font.TLabelframe", relief=tk.GROOVE)

        self.frame1.grid(column=0, row=0, padx=10, pady=10)
        self.frame2.grid(column=0, row=1, sticky=tk.W + tk.E + tk.S + tk.N, padx=10)

         # フレーム1：オリジナル画像
        self.canvas1 = tk.Canvas(self.frame1, width=500, height=300)
        self.canvas1.grid(sticky=tk.W + tk.E + tk.S + tk.N, padx=10, pady=10)

        self.label21 = ttk.Label(self.frame2, text=self.model.qr_text, wraplength=250, anchor="w", justify="left")
        self.button22 = ttk.Button(self.frame2, text="開始", padding=[5,15], style="font.TButton")
        self.button23 = ttk.Button(self.frame2, text="終了", padding=[5,15], style="font.TButton")
        
        self.label21.grid(column=0, row=0, columnspan=3, padx=10, pady=10)
        self.button22.grid(column=3, row=0, padx=10, pady=10)
        self.button23.grid(column=4, row=0, padx=10, pady=10)
        

        self.frame2.grid_columnconfigure(1, weight=1)


class Controller():
    """制御関連
    """
    def __init__(self, master, model, view):
        """create instances
        Args:
            master (class): main window
            model (class): Webcam related
            view (class): tkinter related
        """
        # インスタンス化
        self.master = master
        self.model = model
        self.view = view

    def press_start_button(self):
        print(self.model.qr_text)

    def press_close_button(self):
        # 終了処理
        # ウイジェットの終了
        self.master.destroy()


class Application(tk.Frame):
    """メイン
    1. tkinterを生成
    2. ウインドウを設定
    3. クラスオブジェクトを生成
    4. ボタンコマンドを設定
    Args:
        tk (class): root of tkinter
    """
    def __init__(self, master):
        """start instance
        Args:
            master  (class): main
        """
        # tkinterの定型文
        super().__init__(master)
        self.grid()
        
        # インスタンス化
        self.model = Model()
        
        master.geometry("550x480")
        master.title("QRコード2クリップボード")

        # ウインドウサイズの変更不可
        master.resizable(width=False, height=False)

        # インスタンス化
        self.view = View(master, self.model)
        self.controller = Controller(master, self.model, self.view)

        # ボタンのコマンド設定
        self.view.button22["command"] = self.controller.press_start_button
        self.view.button23["command"] = self.controller.press_close_button


def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()

