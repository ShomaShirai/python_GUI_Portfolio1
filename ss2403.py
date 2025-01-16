import csv
import os
import tkinter as tk
import tkinter.filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

import config
import module_cui


class GuiApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Which is Yoshida or Busquets")
        self.master.geometry(config.APP_SIZE)
        self.face_detector = None  # 顔検出器の初期化
        self.csv_writer = None
        self.csv_file = None
        self.image = None
        self.image_copy = None
        self.image2 = None
        self.processed_image = None
        self.blur_image = None
        self.sunburn_image = None
        self.grabcut_image = None
        self.blur_intensity = tk.DoubleVar(value=config.DEFAULT_INTENSITY)
        self.sunburn_intensity = tk.DoubleVar(value=config.DEFAULT_INTENSITY)
        self.create_widgets()

    def create_widgets(self):
        # Canvas
        self.canvas = tk.Canvas(self.master, bg="#000", width=512, height=512)
        self.canvas.place(x=0, y=0)

        # Label
        self.label1 = tk.Label(text='File name:')
        self.label1.place(x=5, y=520)

        # Textbox
        self.text_box1 = tk.Entry(width=45)
        self.text_box1.place(x=80, y=520)

        # Select Button
        self.btn1 = tk.Button(text="Select", command=self.select_file, width=5)
        self.btn1.place(x=445, y=520)

        # Save Button (非表示にしておく)
        self.btn2 = tk.Button(text="Save", command=self.save_file, width=5)
        self.btn2.place_forget()  # 初期状態では非表示
        self.btn3 = tk.Button(text="Blur", command=self.blur_file, width=5)
        self.btn3.place_forget()
        self.btn4 = tk.Button(text="Change", command=self.change_file, width=5)
        self.btn4.place_forget()
        self.btn5 = tk.Button(text="Sunburn", command=self.sunburn_file, width=5)
        self.btn5.place_forget()
        self.btn6 = tk.Button(text="Grabcut", command=self.grabcut_file, width=5)
        self.btn6.place_forget()
        self.btn7 = tk.Button(text="Close", command=self.close_app, width=5)
        self.btn7.place(x=220, y=650)
        self.btn8 = tk.Button(text="Back", command=self.back_file, width=5)
        self.btn8.place_forget()

        self.blur_label = tk.Label(text="Blur Intensity:")
        self.blur_label.place_forget()
        self.blur_slider = tk.Scale(self.master, from_=0.01, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=self.blur_intensity)
        self.blur_slider.place_forget()

        self.sunburn_label = tk.Label(text="Sunburn Intensity:")
        self.sunburn_label.place_forget()
        self.sunburn_slider = tk.Scale(self.master, from_=0.5, to=1.5, resolution=0.01, orient=tk.HORIZONTAL, variable=self.sunburn_intensity)
        self.sunburn_slider.place_forget()

    def close_app(self):
        if tk.messagebox.askquestion(title='Confirm', message='Will you finish this application?') == 'yes' :
            self.master.destroy()

    def back_file(self):
        if self.image_copy is not None:
            self.image = self.image_copy.copy()
            self.display_image(self.image)
            tk.messagebox.showinfo("Info", "Back to original image.")
        self.enable_button()

    def select_file(self):
        file_name = tk.filedialog.askopenfilename()
        self.text_box1.delete(0, tk.END)
        self.text_box1.insert(0, file_name)

        if os.path.isfile(file_name):
            self.open_image_file(file_name)
        else:
            tk.messagebox.showinfo("Error", f"File ({file_name}) is not found.")
        self.enable_button()

    def select_second_file(self):
        file_name = tk.filedialog.askopenfilename()
        if os.path.isfile(file_name):
            self.image2 = cv2.imread(file_name)
            self.display_image(self.image2)
        else:
            tk.messagebox.showinfo("Error", f"File ({file_name}) is not found.")

    def open_image_file(self, file_name):
        # Load image data using OpenCV and PIL
        self.image = cv2.imread(file_name)
        self.image_copy = self.image.copy()

        # 顔検出器をロード (最初にのみロード)
        directory = os.path.dirname(__file__)
        if self.face_detector is None:
            self.face_detector = module_cui.load_face_detector(directory)

        # 画像をキャンバスに表示
        self.display_image(self.image)

        self.btn2.place(x=60, y=560)
        self.btn3.place(x=140, y=560)
        self.btn4.place(x=220, y=560)
        self.btn5.place(x=300, y=560)
        self.btn6.place(x=380, y=560)
        self.btn7.place(x=220, y=650)
        self.btn8.place(x=30, y=650)

        self.blur_label.place(x=10, y=600)
        self.blur_slider.place(x=100, y=600)

        self.sunburn_label.place(x=230, y=600)
        self.sunburn_slider.place(x=350, y=600)

    def enable_button(self):
        self.btn2.config(state="normal")
        self.btn3.config(state="normal")
        self.btn4.config(state="normal")
        self.btn5.config(state="normal")
        self.btn6.config(state="normal")

    def disable_button(self):
        self.btn2.config(state="disabled")
        self.btn3.config(state="disabled")
        self.btn4.config(state="disabled")
        self.btn5.config(state="disabled")
        self.btn6.config(state="disabled")

    def display_image(self, cv2_image):
        pil_image = Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.canvas.create_image(self.canvas.winfo_width() // 2,
                                 self.canvas.winfo_height() // 2,
                                 image=self.photo_image)

    def save_file(self):
        directory = os.path.dirname(__file__)
        self.csv_writer, self.csv_file = module_cui.create_csv(directory)

        # 顔検出
        self.processed_image = module_cui.process_image(self.face_detector, self.image, self.csv_writer, is_blur_face=None, is_write_csv=True, is_sunburn=None, is_grabcut=None)
        cv2.imwrite("face_detection_output.png", self.processed_image)
        self.display_image(self.processed_image)
        self.csv_file.close()
        tk.messagebox.showinfo("Info", "Complete face detect and preserve csv file")
        self.disable_button()

    def blur_file(self):
        blur_level = self.blur_intensity.get()
        self.blur_image = module_cui.process_image(self.face_detector, self.image, self.csv_writer, is_blur_face=True, blur_intensity=blur_level, is_write_csv=None, is_sunburn=None, is_grabcut=None)
        cv2.imwrite("face_blur_output.png", self.blur_image)
        self.display_image(self.blur_image)
        tk.messagebox.showinfo("Info", "Complete blur face")
        self.disable_button()

    def sunburn_file(self):
        sunburn_level = self.sunburn_intensity.get()
        self.sunburn_image = module_cui.process_image(self.face_detector, self.image, self.csv_writer, is_blur_face=None,
                                            is_write_csv=None, is_sunburn=True, sunburn_intensity=sunburn_level, is_grabcut=None)
        cv2.imwrite("face_sunburn_output.png", self.sunburn_image)
        self.display_image(self.sunburn_image)
        tk.messagebox.showinfo("Info", "Complete sunburn face")
        self.disable_button()

    def grabcut_file(self):
        self.grabcut_image = module_cui.process_image(self.face_detector, self.image, self.csv_writer, is_blur_face=None, is_write_csv=None, is_sunburn=None, is_grabcut=True)
        cv2.imwrite("face_grabcut_output.png", self.grabcut_image)
        self.display_image(self.grabcut_image)
        tk.messagebox.showinfo("Info", "Complete grabcut face")
        self.disable_button()

    def change_file(self):
        # 画像を選択するためのダイアログを開く
        self.select_second_file()

        try:
            swapped_image1, swapped_image2 = module_cui.change_face(self.face_detector, self.image, self.image2)
            cv2.imwrite("face_changed_image1.png", swapped_image1)
            cv2.imwrite("face_changed_image2.png", swapped_image2)

            # 顔を入れ替えた結果を表示
            self.display_image(swapped_image1)
            tk.messagebox.showinfo("Info", "Complete change face")
        except Exception as e:
            tk.messagebox.showinfo("Error", f"Face swapping failed: {e}")

        self.disable_button()


def main():
    root = tk.Tk()
    app = GuiApplication(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
