#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 22:54:17 2019

@author: moritote
"""

import os, tkinter, tkinter.filedialog
import numpy as np

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('csv出力・結合ツール')
        self.master.minsize(280,100)
        #self.master.configure(bg='black')
        self.pack()
        self.create_widgets()
        self.setup()

    def create_widgets(self):
        #ファイル選択ボタンの配置、設定
        self.file_button = tkinter.Button(self, text='ファイル選択', command=self.file_select)
        self.file_button.grid(row=0, column=0)

        #選択されたファイル名の配置、設定
        self.file_label = tkinter.Label(self)
        self.file_label.grid(row=1, column=0)

        #csv作成ボタンの配置、設定
        self.make_button = tkinter.Button(self, text='csv作成', command=self.make_csv)
        self.make_button.grid(row=2, column=0)
        
        #csv結合ボタンの配置、設定
        self.merge_button = tkinter.Button(self, text='csv結合', command=self.merge_csv)
        self.merge_button.grid(row=3, column=0)

    def setup(self):
        #筆跡記憶配列　３次元配列ver
        #np.full(((線の本数、描画数、x・y)))
        self.data = np.full(((100,1000,2)),-100)
        self.n = 0
        self.plot_size = 0

    def file_select(self):
        #ファイル選択ボタン押下時呼び出し関数
        
        #ファイル選択画面表示
        fTyp = [("NPY","*.npy")]
        self.iDir = os.path.abspath(os.path.dirname(__file__))
        self.filename = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = self.iDir)
        #ファイル名取得
        self.dir = os.path.dirname(self.filename)
        self.file_label["text"] = self.filename
    
    def make_csv(self):
        #csv作成関数
        
        #csvファイル保存用フォルダ作成
        new_csv_foler = self.dir + "/csv/"
        if not os.path.isdir(new_csv_foler):
            os.makedirs(new_csv_foler)
        #線毎にcsvファイル作成
        csv_name_cnt = 1
        vect_data = np.load(self.filename)
        for vect_data0 in vect_data:
            csv_file_name = self.dir + "/csv/" + str(csv_name_cnt) + ".csv"
            np.savetxt(csv_file_name, vect_data0, delimiter=',', fmt='%d')
            csv_name_cnt+=1
            
        print("csvファイル作成完了！")

    def merge_csv(self):
        #csv結合関数
        
        #結合用npyファイル準備
        vect_list = []
        csv_dir = self.dir + "/csv/"
        csv_list = os.listdir(csv_dir)
        for csv_list_0 in csv_list:
            csv_file_name = csv_dir + csv_list_0
            vect_list.append(np.loadtxt(csv_file_name, delimiter=',', dtype='int'))
        #結合用npyファイル保存
        new_file_name = self.dir + "/merge.npy"
        if os.path.isfile(new_file_name):
            os.remove(new_file_name)
        np.save(new_file_name, vect_list)
        
        print("csvファイル結合完了！")

#メイン処理
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()