# @Author: Xiangxin Kong
# @Date: 2020.5.30
from downloader import *
import tkinter as tk
from tkinter import *


class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        super().title('Manhuagui Downloader')
        super().geometry('400x160')
        baseY = 30
        tk.Label(self, text='Url:', font=('Arial', 16,)).place(x=10, y=baseY)
        tk.Label(self, text='To:', font=('Arial', 16,)).place(x=10, y=baseY + 40)
        self.var_address = tk.StringVar()
        self.var_url = tk.StringVar()
        self.var_address.set('manga/')
        self.var_url.set('https://www.manhuagui.com/comic/3047/')
        tk.Entry(self, textvariable=self.var_url, font=('Arial', 14), width=28).place(x=60, y=baseY)
        tk.Entry(self, textvariable=self.var_address, font=('Arial', 14), width=28).place(x=60, y=baseY + 40)
        tk.Button(self, text='Download', font=('Arial', 12), command=self.download).place(x=290, y=baseY + 80)
        self.mainloop()

    def download(self):
        try:
            s = MangaDownloader(self.var_url.get(), self.var_address.get())
        except:
            print("Manga not Found")
            self.var_url.set("")
            return
        downloadPanel(s)


class downloadPanel(Toplevel):
    def __init__(self, s):
        super().__init__()
        super().title('Manhuagui Downloader')
        super().geometry('900x600')

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(canvas))

        self.place_label(s)
        self.place_buttons(s)

        var = IntVar()

        def checkAll():
            for i in self.buttons:
                if var.get() == 1:
                    i.select()
                elif i.cget("state") == 'normal':
                    i.deselect()

        tk.Checkbutton(self.frame, text='Select All', font=('Arial', 18), variable=var, command=checkAll).pack()
        tk.Button(self.frame, text='Download', font=('Arial', 16), command=lambda: self.downloadChapters(s)).pack()

    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def place_label(self, s):
        tk.Label(self.frame, text=s.title, font=('Arial', 33,)).pack()
        tk.Label(self.frame, text="作者: " + s.author, font=('Arial', 12,)).pack()
        tk.Label(self.frame, text="年代: " + s.year, font=('Arial', 12,)).pack()
        tk.Label(self.frame, text="地区: " + s.region, font=('Arial', 12,)).pack()
        tk.Label(self.frame, text="类型: " + s.plot, font=('Arial', 12,)).pack()
        self.baseY = 120

    def place_buttons(self, s):
        self.buttons = []
        for i in range(len(s.chapters)):
            s.chapters[i][2] = IntVar()
            cha = tk.Checkbutton(self.frame, text=s.chapters[i][0], font=('Arial', 14), variable=s.chapters[i][2])
            cha.pack()
            if s.chapters[i][0] in s.existedChapters():
                cha.select()
                cha.config(state='disabled')
            self.buttons.append(cha)

    def downloadChapters(self, s):
        for i in range(s.length):
            if self.buttons[i].cget("state") == 'normal' and s.chapters[i][2].get():
                s.downloadChapter(s.chapters[i][1])


if __name__ == '__main__':
    mainWindow()
