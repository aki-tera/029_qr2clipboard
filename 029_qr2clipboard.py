import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font

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

        # フォントの設定
        # ラベルフレーム用
        self.font_frame = font.Font(family="Meiryo UI", size=15, weight="normal")
        # ボタン用
        self.font_buttom = font.Font(family="Meiryo UI", size=20, weight="bold")

        # フレーム設定
        self.frame1 = tk.LabelFrame(self.master, text="元画像", font=self.font_frame, padx=10, pady=10)
        self.frame2 = tk.LabelFrame(self.master, text="計測距離", font=self.font_frame, padx=10, pady=10)

        self.frame1.grid(column=0, row=0)
        self.frame2.grid(column=0, row=1)
        
        self.button1 = tk.Button(self.frame1, text="開始", font=self.font_buttom)
        self.button2 = tk.Button(self.frame2, text="終了", font=self.font_buttom)

        self.button1.grid(column=0, row=0)
        self.button2.grid(column=0, row=0)


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
        print("Start")

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
        
        master.geometry("500x500")
        master.title("QRコード2クリップボード")

        # ウインドウサイズの変更不可
        master.resizable(width=False, height=False)

        # インスタンス化
        self.view = View(master, self.model)
        self.controller = Controller(master, self.model, self.view)

        # ボタンのコマンド設定
        self.view.button1["command"] = self.controller.press_start_button
        self.view.button2["command"] = self.controller.press_close_button


def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()

