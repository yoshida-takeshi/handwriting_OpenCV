import numpy as np
np.set_printoptions(threshold=np.inf)
s = input("読み込むデータは？：")
data = np.load(s+".npy")

###data準備###
#元データにフラグ情報がない場合、0を追加#
kaku_all = data.shape
if kaku_all[2]==2:
    z = np.full(((kaku_all[0], 1000, 1)), 0)
    data_z_add = np.append(data,z,axis=2)

###フラグ変更プログラム###
print("*****************\n"
      "＜フラグ番号参考＞\n"
      "0〜9：処理なし\n"
      "10〜19：始点関係\n"
      "20〜29：はらい関係\n"
      "30〜39：とめ関係\n"
      "40〜49：はね関係\n"
      "50〜59：点関係\n"
      "*****************")

for line in range(kaku_all[0]):
    #lineのデータ数を取得
    c=0
    for i in range(1000):
        if data_z_add[line][i][0] != -100:
            c+=1

    kind_line = input(str(line+1)+"画目に追加するフラグ番号は：")
    k_line = int(kind_line)
    #0〜9：処理なし
    if 0 <= k_line <=9:
        for i in range(c):
            data_z_add[line][i][2] = k_line
    #10〜19：始点関係
    elif 10 <= k_line <=19:
        for i in range(10):
            data_z_add[line][i][2] = k_line
    #20〜29：はらい関係
    elif 20 <= k_line <=29:
        change_pt = int(2 / 3 * c)
        for i in range(change_pt,c):
            data_z_add[line][i][2] = k_line
    #30〜39：とめ関係
    elif 30 <= k_line <= 39:
        end_pt = c-20
        for i in range(end_pt,c):
            data_z_add[line][i][2] = k_line
        for i in range(end_pt*(-1)+c):
            data_z_add[line][c+i][0] = data_z_add[line][c-i-1][0]
            data_z_add[line][c+i][1] = data_z_add[line][c-i-1][1]
            data_z_add[line][c+i][2] = k_line
    #40〜49：はね関係
    #50〜59：点関係
ans = s+"_plus_flag"
print(data_z_add)
#np.save(ans,data_z_add)