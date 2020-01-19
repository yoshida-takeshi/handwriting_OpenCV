#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np


class writing_flag_add:
    ########################################
    #INIT
    def __init__(self,args):
        CmdFile = args[1]

        self.main_loop(CmdFile)

    ########################################
    #メイン処理
    def main_loop(self,CmdFile):
        f = open(CmdFile)
        CmdLineAll = f.readlines()
        f.close()

        for CmdLine in CmdLineAll:
            CmdLine=CmdLine.rstrip()
            CmdWord=CmdLine.split()

            if len(CmdWord)==0: continue
            if re.search("^#",CmdLine): continue
            print("CMD:"+CmdLine)
                
            if CmdWord[0]=="read":
                self.cmd_read(CmdWord)
            elif CmdWord[0]=="write":
                self.cmd_write(CmdWord)
            elif CmdWord[0]=="addflg_range":
                self.cmd_addflg_range(CmdWord)
            elif CmdWord[0]=="addflg_start":
                self.cmd_addflg_start(CmdWord)
            elif CmdWord[0]=="addflg_end":
                self.cmd_addflg_end(CmdWord)
            elif CmdWord[0]=="addflg_per":
                self.cmd_addflg_per(CmdWord)
            else:
                print("Error: Unknown command => %s" % CmdLine)
        exit()

    ########################################
    #CMD:筆跡データ読み込み
    def cmd_read(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: read <input_fondfile>)")
            return
        infile=CmdWord[1]
        self.data = np.load(infile)

        #元データにフラグ情報がない場合、0を追加
        shp = self.data.shape
        if shp[2]==2:
            print("information: Added zero flag")
            z = np.full(((shp[0], shp[1], 1)), 0)
            self.data = np.append(self.data,z,axis=2)

    ########################################
    #CMD:筆跡データ保存
    def cmd_write(self,CmdWord):
        if len(CmdWord)!=2:
            print("Error: Invalid args (usage: write <output_fondfile>)")
            return
        outfile=CmdWord[1]
        np.save(outfile,self.data)

    ########################################
    #CMD:フラグ付加(範囲指定版)
    def cmd_addflg_range(self,CmdWord):
        if len(CmdWord)!=5:
            print("Error: Invalid args (usage: addflg_range <flag> <line> <start_point> <end_point>)")
            return
        Flag=int(CmdWord[1])
        Line=int(CmdWord[2])
        Start=int(CmdWord[3])
        End=int(CmdWord[4])
        for i in range(Start,End+1):
            self.add_flag(Flag,Line,i)

    ########################################
    #CMD:フラグ付加(Startからの範囲指定版)
    def cmd_addflg_start(self,CmdWord):
        if len(CmdWord)!=4:
            print("Error: Invalid args (usage: addflg_start <flag> <line> <end_point>)")
            return
        Flag=int(CmdWord[1])
        Line=int(CmdWord[2])
        Start=0
        End=int(CmdWord[3])
        for i in range(Start,End+1):
            self.add_flag(Flag,Line,i)

    ########################################
    #CMD:フラグ付加(Endからの範囲指定版)
    def cmd_addflg_end(self,CmdWord):
        if len(CmdWord)!=4:
            print("Error: Invalid args (usage: addflg_end <flag> <line> <start_point>)")
            return
        Flag=int(CmdWord[1])
        Line=int(CmdWord[2])
        EP=self.get_endpoint(Line)
        Start=EP-int(CmdWord[3])
        End=EP
        for i in range(Start,End+1):
            self.add_flag(Flag,Line,i)

    ########################################
    #CMD:フラグ付加(パーセント指定版)
    def cmd_addflg_per(self,CmdWord):
        if len(CmdWord)!=5:
            print("Error: Invalid args (usage: addflg_per <flag> <line> <start_per> <end_per>)")
            return
        Flag=int(CmdWord[1])
        Line=int(CmdWord[2])
        EP=self.get_endpoint(Line)
        Start=int(EP*int(CmdWord[3])/100)
        End=int(EP*int(CmdWord[4])/100)
        for i in range(Start,End+1):
            self.add_flag(Flag,Line,i)




    ########################################
    #フラグ付加処理
    def add_flag(self,Flag,Line,Point):
        self.data[Line,Point,2]=Flag
        print(" Flaged %d : (%d,%d)" % (Flag,Line,Point))

    ########################################
    #エンドポイント取得
    def get_endpoint(self,Line):
        shp = self.data.shape
        p=-1
        for i in range(shp[1]):
            if self.data[Line][i][0] != -100:
                p+=1
        return p



if __name__ == '__main__':
    args = sys.argv
    if len(args)==2:
        m = writing_flag_add(args)
    else:
        print("usage: %s <command_file>" % args[0])





####フラグ変更プログラム###
#print("*****************\n"
#      "＜フラグ番号参考＞\n"
#      "0〜9：処理なし\n"
#      "10〜19：始点関係\n"
#      "20〜29：はらい関係\n"
#      "30〜39：とめ関係\n"
#      "40〜49：はね関係\n"
#      "50〜59：点関係\n"
#      "*****************")
#
#for line in range(kaku_all[0]):
#    #lineのデータ数を取得
#    c=0
#    for i in range(1000):
#        if data_z_add[line][i][0] != -100:
#            c+=1
#
#    kind_line = input(str(line+1)+"画目に追加するフラグ番号は：")
#    k_line = int(kind_line)
#    #0〜9：処理なし
#    if 0 <= k_line <=9:
#        for i in range(c):
#            data_z_add[line][i][2] = k_line
#    #10〜19：始点関係
#    elif 10 <= k_line <=19:
#        for i in range(10):
#            data_z_add[line][i][2] = k_line
#    #20〜29：はらい関係
#    elif 20 <= k_line <=29:
#        change_pt = int(2 / 3 * c)
#        for i in range(change_pt,c):
#            data_z_add[line][i][2] = k_line
#    #30〜39：とめ関係
#    elif 30 <= k_line <= 39:
#        end_pt = c-20
#        for i in range(end_pt,c):
#            data_z_add[line][i][2] = k_line
#        for i in range(end_pt*(-1)+c):
#            data_z_add[line][c+i][0] = data_z_add[line][c-i-1][0]
#            data_z_add[line][c+i][1] = data_z_add[line][c-i-1][1]
#            data_z_add[line][c+i][2] = k_line
#    #40〜49：はね関係
#    #50〜59：点関係
