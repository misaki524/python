import pyxel


class Animation:
    def __init__(self):
        pyxel.init(80,60,title="animation")

        self.rabbit_x=37 #ウサギのx座標
        self.rabbit_y=10 #ウサギのY座標
        self.rabbit_vy=0 #ウサギのY方向の速度
        self.rabbit_height=10 #ウサギの高さ
        self.rabbit_color=15 #ウサギの色

        pyxel.run(self.update,self.draw)

    #ウサギを書く関数(X座標、Y座標系、番号)
    def draw_rabbit(self,x,y,color):
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


    def update(self):
        self.rabbit_y+=self.rabbit_vy
        self.rabbit_vy+=0.1
        rabbit_bounce_y=pyxel.height-self.rabbit_height

        if self.rabbit_y>=rabbit_bounce_y:
            self.rabbit_y=rabbit_bounce_y
            self.rabbit_vy=self.rabbit_vy*-0.95

    def draw(self):
        pyxel.cls(1)  #①画面を青背景にする
        self.draw_rabbit(self.rabbit_x,self.rabbit_y,self.rabbit_color)  #②ウサギを描く

Animation()