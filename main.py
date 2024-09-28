"""
time:2024.4.22
author:wisdom
intruduction:
这里是垃圾分类的主程序，主要完成图形界面
"""
import tkinter as tk
import serial
import time
from PIL import Image, ImageTk
from cappredict import main,update_transh_num,rubbish2Classification
from cap import cap_transh,get_img
from new_cum import initConnection,sendData,control_dirction


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("登录")
        self.root.geometry("400x200")  # 设置窗口大小

        self.label_username = tk.Label(root, text="用户名：")
        self.label_password = tk.Label(root, text="密码：")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.button_login = tk.Button(root, text="登录", command=self.login)

        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)


    def login(self):
        # 假设用户名为 "admin"，密码为 "password" 才能登录成功
        if self.entry_username.get() == "hnnu" and self.entry_password.get() == "123":
            self.root.destroy()  # 关闭登录窗口
            app = ClassificationApp()  # 进入分类界面
            app.mainloop()
        else:
            print("登录失败")

class ClassificationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("垃圾分类")
        self.geometry("500x400")  # 设置窗口大小

        self.labels = []
        self.entries = []

        trash_types = ["可回收垃圾", "厨余垃圾", "其他垃圾", "有害垃圾"]

        # 添加6个文本框和标签
        for i, trash_type in enumerate(trash_types):
            label = tk.Label(self, text=f"{trash_type}：")
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.E)
            entry = tk.Entry(self, width=10)
            entry.insert(tk.END, "0")
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.labels.append(label)
            self.entries.append(entry)

        # 添加分类按钮和退出按钮
        self.button_classify = tk.Button(self, text="分类", command=self.classify)
        self.button_classify.grid(row=7, column=0, padx=10, pady=10)
        self.button_exit = tk.Button(self, text="退出", command=self.quit)
        self.button_exit.grid(row=7, column=1, padx=10, pady=10)

        # 加载初始图片
        self.image_path = r"D:\pyc_workspace\TF2.11\test\hnnu.jpg"
        self.load_image(self.image_path)
        with open('update_transh_num.txt', 'w') as f:
            print("分类信息清零！")

    def classify(self):

        cap_transh(r"D:\pyc_workspace\TF2.11\cap_photos", 1)
        file_name = get_img()
        transh = main(file_name)
        update_transh_num(rubbish2Classification(transh[1]))
        print(transh)

        ser = initConnection("COM4", 9600)  # windows
        time.sleep(1.8)
        sendData(ser, [666, 666], 3)
        #time.sleep(2)

        # 这里假设分类结果为一个列表，包含了每种垃圾的数量，例如 [3, 5, 2, 0, 1, 4]
        classification_result=[]
        with open('update_transh_num.txt', 'r') as f:
            for each_line in f:
                classification_result.append(int(each_line))
        #classification_result = [3, 5, 2, 0, 1, 4]

        # 更新文本框后面的数量
        for i, value in enumerate(classification_result):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(tk.END, str(value))

        # 更新图片
        self.image_path = get_img()
        self.load_image(self.image_path)

        control_dirction(ser, rubbish2Classification(transh[1]))
        ser.close()

    def load_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img = img.resize((300, 300))  # 调整图像大小以适应标签
                photo = ImageTk.PhotoImage(img)
                self.image_label = tk.Label(self, image=photo)
                self.image_label.image = photo
                self.image_label.grid(row=0, column=2, rowspan=7, padx=10, pady=10)
        except Exception as e:
            print("Error loading image:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
