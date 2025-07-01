import pyxel

#キャラクターを描く関数(X座標、Y座標,体の色、輪郭線の色、顔の色)
def draw_character(x,y,body_color,outline_color,face_color):
    pyxel.circ(x,y,8,body_color)
    pyxel.circb(x,y,8,outline_color)
    pyxel.line(x-4,y-3,x-4,y,face_color)
    pyxel.line(x+2,y-3,x+2,y,face_color)
    pyxel.line(x-4,y+3,x+2,y+3,face_color)
    pyxel.pset(x-5,y+2,face_color)
    pyxel.pset(x+3,y+2,face_color)

pyxel.init(160,120,title="test")
draw_character(45,40,3,7,0) #キャラクター1
draw_character(115,80,8,15,0) #キャラクター2

pyxel.show() #画面を表示する
