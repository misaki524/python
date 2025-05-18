#Pythonの標準モジュールであるmathの定数piを使い半径が3の円の面積を求めて出力してください

import math

r=3


#円の面積を計算。**で二乗を使っている
def area(r):
    return r**2*math.pi

area_ans=(area(r))
print(area_ans)