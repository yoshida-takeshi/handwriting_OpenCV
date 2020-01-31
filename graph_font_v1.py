#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cv2
import numpy as np

args = sys.argv
if len(args)==2:
    FontData=args[1]
else:
    print("usage: %s <font_data>" % args[0])
    exit()

#ペンの色
Color = (0, 0, 0)
#ペンの太さ
Thickness = 10

#新しいウィンドウを開く
CampusSize=512
Ratio = CampusSize / 100
Img = np.zeros((CampusSize, CampusSize, 3), np.uint8)
Img[:,:,:]=(255,255,255)
cv2.namedWindow("Img")

VectData = np.load(FontData)
x0=0
y0=0

####################
#一筆分ずつデータ取得
n0=-1
for VectData0 in VectData:
    n0+=1
    z=1
    #NULLデータの場合は処理スキップ
    if VectData0[0][0]==-100: continue

    ####################
    #サンプリング単位のデータ取得
    n1=-1
    for VectData1 in VectData0:
        n1+=1
        #NULLデータの場合は処理スキップ
        if VectData1[0]==-100: continue

        #x,y,fデータ取得
        x=VectData1[0]
        y=VectData1[1]
        #FLAG拡張データかどうかチェック
        if len(VectData1)>2:
            f=VectData1[2]
        else:
            f=-1
        if (x==x0 and y==y0): continue

        #フラグによって色を決める
        (b,g,r)=(0,0,0)
        f0=int(f/10)
        #if (f0 & 0b001): r=255
        #if (f0 & 0b010): b=255
        #if (f0 & 0b100): g=255
        if (f==-1): (r,g,b)=(127,127,127)
        if (f==10): (r,g,b)=(255,  0,  0)
        if (f==11): (r,g,b)=(255, 15, 15)
        if (f==12): (r,g,b)=(255, 31, 31)
        if (f==13): (r,g,b)=(255, 47, 47)
        if (f==20): (r,g,b)=(  0,255,  0)
        if (f==21): (r,g,b)=( 15,255, 15)
        if (f==22): (r,g,b)=( 31,255, 31)
        if (f==23): (r,g,b)=( 47,255, 47)
        if (f==30): (r,g,b)=(  0,  0,255)
        if (f==31): (r,g,b)=( 15, 15,255)
        if (f==32): (r,g,b)=( 31, 31,255)
        if (f==33): (r,g,b)=( 47, 47,255)
        if (f==40): (r,g,b)=(255,255,  0)
        if (f==41): (r,g,b)=(255,255, 15)
        if (f==42): (r,g,b)=(255,255, 31)
        if (f==43): (r,g,b)=(255,255, 47)
        if (f==50): (r,g,b)=(255,  0,255)
        if (f==51): (r,g,b)=(255, 15,255)
        if (f==52): (r,g,b)=(255, 31,255)
        if (f==53): (r,g,b)=(255, 47,255)
        if (f==60): (r,g,b)=(  0,255,255)
        if (f==61): (r,g,b)=( 15,255,255)
        if (f==62): (r,g,b)=( 31,255,255)
        if (f==63): (r,g,b)=( 47,255,255)
        Color=(b, g, r)
        print((n0,n1),(x,y),f)

        #描画用座標算出してラインを引く
        if z==0:
            lx0=int(x0 * Ratio)
            lx =int(x  * Ratio)
            ly0=int(y0 * Ratio)
            ly =int(y  * Ratio)
            cv2.line(Img, (lx0,ly0), (lx,ly), Color, Thickness)

        cv2.imshow("Img", Img)
        cv2.waitKey(1)

        #次回参照用のx,y座標を退避
        x0=x
        y0=y
        z=0


#プログラム終了
key = raw_input('Please enter to finish.')
#python3# key = input('Please enter to finish.')

exit()

