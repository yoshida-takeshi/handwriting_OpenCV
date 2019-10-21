#!/usr/bin/env python3
# coding: utf-8

# -*- coding: utf-8 -*-
import cv2
import numpy as np

#sx, syは線の始まりの位置
sx, sy = 0, 0
#ペンの色
color = (0, 0, 0)
#ペンの太さ
thickness = 10

#筆跡記憶配列
dtype_plot = [("x", "i2"), ("y", "i2")]
plot = np.zeros(1024, dtype=dtype_plot)
plot_size = 0

#筆跡記憶配列　３次元配列ver
#np.full(((線の本数、描画数、x・y)))
data = np.full(((100,1000,2)),-100)
n = 0

#マウスの操作があるとき呼ばれる関数
def callback(event, x, y, flags, param):
    global img, sx, sy, color, thickness, plot_size,data,n

    #(STATUS)
    #event
    #CV_EVENT_MOUSEMOVE (0):マウスカーソルが動いた
    #CV_EVENT_LBUTTONDOWN (1):左ボタンが押された
    #CV_EVENT_RBUTTONDOWN (2):右ボタンが押された
    #CV_EVENT_MBUTTONDOWN (3):中央ボタンが押された
    #CV_EVENT_LBUTTONUP (4):左ボタンが離された
    #CV_EVENT_RBUTTONUP (5):右ボタンが離された
    #CV_EVENT_MBUTTONUP (6):中央ボタンが離された
    #CV_EVENT_LBUTTONDBLCLK (7):左ボタンがダブルクリックされた
    #CV_EVENT_RBUTTONDBLCLK (8):右ボタンがダブルクリックされた
    #CV_EVENT_MBUTTONDBLCLK (9):中央ボタンがダブルクリックされた
    #flags
    #CV_EVENT_FLAG_LBUTTON (1):マウス左ボタンが押されているか
    #CV_EVENT_FLAG_RBUTTON (2):マウス右ボタンが押されているか
    #CV_EVENT_FLAG_MBUTTON (4):マウス中央ボタンが押されているか
    #CV_EVENT_FLAG_CTRLKEY (8):CTRLボタンが押されているか
    #CV_EVENT_FLAG_SHIFTKEY (16):Shiftボタンが押されているか
    #CV_EVENT_FLAG_ALTKEY (32):Altボタンが押されているか
    

    
    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
        data[n,plot_size] = (x*100/512,y*100/512)
        plot_size +=1
        

    #マウスの左ボタンがクリックされていて、マウスが動いたとき
    if (flags & cv2.EVENT_FLAG_LBUTTON) and event == cv2.EVENT_MOUSEMOVE:
        cv2.line(img, (sx, sy), (x, y), color, thickness)
        sx, sy = x, y
        data[n,plot_size] = (x*100/512,y*100/512)
        plot_size += 1
    
    #マウスの左ボタンがクリックされていて、マウスが離れたとき
    if (flags & cv2.EVENT_FLAG_LBUTTON) and event == cv2.EVENT_LBUTTONUP:
        n+=1
        plot_size = 0
        
#新しいウィンドウを開く
img = np.zeros((512, 512, 3), np.uint8)
img[:,:,:]=(255,255,255)
cv2.namedWindow("img")

#マウス操作のコールバック関数の設定
cv2.setMouseCallback("img", callback)

while(1):
    cv2.imshow("img", img)
    k = cv2.waitKey(1)

    #Escキーを押すと終了
    if k == 27:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        break

    #sを押すとデータを保存
    if k == ord("s"):
        path_w = input('filename=> ')
        #配列を軽くしてからnumpy形式で保存
        data0=data[0:n,:,:]
        np.save(path_w, data0)
        print ("write: ",path_w)

    #cを押すとデータクリア
    if k == ord("c"):
        img[:,:,:]=(255,255,255)
        data = np.full(((100,1000,2)),-100)
        plot_size=0
        n=0
        print ("clear")





