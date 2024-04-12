import unicodedata
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode, ZBarSymbol
import numpy as np


def cut_text(original_text, max_height, max_length):
    """Reduces the input string to the specified number of characters

    Args:
        original_text (str): the string to decrement
        max_height (int): maximum number of line to output
        max_length (int): maximum number of characters to output

    Returns:
        str: the processed string
    """
    new_text = []
    height_counter = 0
    length_counter = 0

    for i in original_text:
        new_text.append(i)
        length_counter += (2 if unicodedata.east_asian_width(i) in "FWA" else 1)
        if length_counter >= max_length or i == "\n":
            height_counter += 1
            length_counter = 0
            if height_counter > max_height:
                break
    return ''.join(new_text)


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

        # QRコードの内容を保存する
        self.qr_text = "Please shoot QR Code on camera."
        self.is_qr_detected = False

        # インスタンス変数の設定
        self.qr_text_short = tk.StringVar()
        self.qr_text_short.set(self.qr_text)

        # カメラ起動
        self.start_camera()

    def start_camera(self):
        # カメラ起動
        self.aruco = cv2.aruco
        self.dictionary = self.aruco.getPredefinedDictionary(self.aruco.DICT_4X4_50)

        # CAP_DSHOWを設定すると、終了時のterminating async callbackのエラーは出なくなる
        # ただし場合によっては、フレームレートが劇遅になる可能性あり
        # self.cap = cv2.VideoCapture(self.camera_setting["CAM"]["ID"], cv2.CAP_DSHOW)
        self.cap = cv2.VideoCapture(0)

        # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    
    def stop_camera(self):
        """release webcam resource.
        """
        # カメラリソース解放
        self.cap.release()

    def get_camera_frame(self):
        # cv2の処理をすべて実施

        # ビデオキャプチャから画像を取得
        ret, frame = self.cap.read()

        if ret:
            # QRコードのでコード
            values = decode(frame, symbols=[ZBarSymbol.QRCODE])

            if values != []:
                retval, decoded_info, size_info, points, _, _ = values[0]

                # QRコードの内容を代入
                self.qr_text = retval.decode('utf-8')
                self.qr_text_short.set(cut_text(self.qr_text, 2, 35))
                self.is_qr_detected = True

                # ポジションデータを取得
                self.np_points = np.array(points)

                # QRコードを枠で囲む
                frame = cv2.polylines(frame, [self.np_points], True, (255, 55, 0), thickness=5, lineType=cv2.LINE_AA)

        # sizeを取得
        # (縦、横、色)
        height, width = frame.shape[:2]

        # 処理できる形に変換
        img1 = cv2.resize(frame, (500, int(height * (500 / width))))

        return img1


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
        style.configure("font.TButton", font=20)

        # フレーム設定
        self.camera_frame = ttk.LabelFrame(self.master, text="Camera image", style="font.TLabelframe", relief=tk.GROOVE)
        self.qrcode_frame = ttk.LabelFrame(self.master, text="QR Code Contents", style="font.TLabelframe", relief=tk.GROOVE)

        self.camera_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.qrcode_frame.grid(column=0, row=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=10)

        # フレーム1：オリジナル画像
        self.camera_canvas = tk.Canvas(self.camera_frame, width=500, height=300)
        self.camera_canvas.grid(sticky=tk.W + tk.E + tk.S + tk.N, padx=10, pady=10)

        # Labelはウイジェット変数で表示内容を制御する
        self.qrcode_label = ttk.Label(self.qrcode_frame, wraplength=220, anchor="w", justify="left")
        self.clipboard_button = ttk.Button(self.qrcode_frame, text="Clipboard", padding=[5, 15], style="font.TButton")
        self.close_button = ttk.Button(self.qrcode_frame, text="Quit", padding=[5, 15], style="font.TButton")
        
        self.qrcode_label.grid(column=0, row=0, columnspan=3, padx=10, pady=10)
        self.clipboard_button.grid(column=3, row=0, padx=10, pady=10)
        self.close_button.grid(column=4, row=0, padx=10, pady=10)
        
        self.qrcode_frame.grid_columnconfigure(1, weight=1)

        # ディスプレイ表示
        self.display_image()
        
    def display_image(self):
        # カメラ画像を表示するため、RGBの入れ替えを行う
        self.img1 = cv2.cvtColor(self.model.get_camera_frame(), cv2.COLOR_BGR2RGB)
        # 複数のインスタンスがある場合、インスタンスをmasterで指示しないとエラーが発生する場合がある
        # エラー内容：image "pyimage##" doesn't exist
        self.img2 = ImageTk.PhotoImage(image=Image.fromarray(self.img1), master=self.camera_frame)
        self.camera_canvas.create_image(0, 0, anchor='nw', image=self.img2)

        # QRコードの読み取り更新
        self.master.after(50, self.display_image)


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

        # Labelで表示する内容のウイジェット変数の設定
        self.view.qrcode_label.config(textvariable=self.model.qr_text_short)

    def press_clipboard_button(self):
        # クリップボードの内容をクリア
        self.master.clipboard_clear()

        if self.model.is_qr_detected is True:
            # クリップボードへ内容登録
            self.master.clipboard_append(self.model.qr_text)

    def press_close_button(self):
        # 終了処理
        # カメラリソース解放
        self.model.stop_camera()
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
        master.title("QR code to clipboard")

        # ウインドウサイズの変更不可
        master.resizable(width=False, height=False)

        # インスタンス化
        self.view = View(master, self.model)
        self.controller = Controller(master, self.model, self.view)

        # ボタンのコマンド設定
        self.view.clipboard_button["command"] = self.controller.press_clipboard_button
        self.view.close_button["command"] = self.controller.press_close_button


def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()
