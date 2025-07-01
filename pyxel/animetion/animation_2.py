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

rabbit_x=0 #ウサギのx座標

while True:  #無限ループ
    pyxel.cls(1)  #①画面を青背景にする
    draw_rabbit(rabbit_x,25,15)  #②ウサギを描く
    pyxel.flip() #③画面を更新する
    rabbit_x+=1 #④ウサギのX座標を1増やす

    if rabbit_x>=pyxel.width:
        rabbit_x=-6