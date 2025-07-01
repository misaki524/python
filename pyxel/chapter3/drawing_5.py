import pyxel

pyxel.init(160,120,title="sample drawing")

x=45 #基準位置のx座標
y=40 #基準値のy座標
body_color=3 #体の色
edge_color=7 #輪郭線の色
face_color=0 #顔パーツの色

pyxel.circ(x,y,8,body_color)
pyxel.circb(x,y,8,edge_color)
pyxel.line(x-4,y-3,x-4,y,face_color)
pyxel.line(x+2,y-3,x+2,y,face_color)
pyxel.line(x-4,y+3,x+2,y+3,face_color)
pyxel.pset(x-5,y+2,face_color)
pyxel.pset(x+3,y+2,face_color)

#キャラクター2を書く
x=115
y=80
body_color=8
edge_color=15
face_color=0

pyxel.circ(x,y,8,body_color)
pyxel.circb(x,y,8,edge_color)
pyxel.line(x-4,y-3,x-4,y,face_color)
pyxel.line(x+2,y-3,x+2,y,face_color)
pyxel.line(x-4,y+3,x+2,y+3,face_color)
pyxel.pset(x-5,y+2,face_color)
pyxel.pset(x+3,y+2,face_color)

pyxel.show() #画面を表示する
