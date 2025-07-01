import pyxel


#ウサギを書く関数(X座標、Y座標系、番号)
def draw_rabbit(x,y,color):
    #体を描く
    pyxel.line(x+2,y,x+2,y+2,color)
    pyxel.line(x+4,y,x+4,y+4,color)
    pyxel.rect(x+2,y+3,4,3,color)
    pyxel.rect(x+1,y+6,4,3,color)
    pyxel.line(x,y+9,x+2,y+9,color)
    pyxel.line(x+4,y+9,x+5,y+9,color)
    #目を描く
    pyxel.pset(x+3,y+4,8)
    pyxel.pset(x+5,y+4,8)

pyxel.init(80,60,title="animation")

rabbit_x=37 #ウサギのx座標
rabbit_y=10 #ウサギのY座標
rabbit_vy=0 #ウサギのY方向の速度
rabbit_height=10 #ウサギの高さ
rabbit_color=15 #ウサギの色

while True:  #無限ループ
    rabbit_y+=rabbit_vy
    rabbit_vy+=0.1 #速度を0.1増やす

    rabbit_bounce_y=pyxel.height-rabbit_height #Y座標の上限を決める
    if rabbit_y>=rabbit_bounce_y: #もし画面の下端まで来たら
        rabbit_y=rabbit_bounce_y #ウサギのY座標をY座標の上限に補正
        rabbit_vy*=-0.95 #Y方向の移動速度を少し減らしつつ反転する

    pyxel.cls(1)  #①画面を青背景にする
    draw_rabbit(rabbit_x,rabbit_y,rabbit_color)  #②ウサギを描く
    pyxel.flip() #③画面を更新する

