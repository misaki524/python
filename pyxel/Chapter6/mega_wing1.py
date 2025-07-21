import pyxel


#背景クラス
class Background:
    NUM_STARS=100 #星の数

    #背景を初期化してゲームに登録する
    def __init__(self,game):
        self.game=game #ゲームへの参照
        self.stars=[] #星の座標と速度のリスト

        #星の座標と速度を初期化してリストに登録する
        for i in range(Background.NUM_STARS):
            x=pyxel.rndi(0,pyxel.width-1) #X座標
            y=pyxel.rndi(0,pyxel.height-1) #Y座標
            vy=pyxel.rndf(1,2.5) #Y方向の速度
            self.stars.append((x,y,vy)) #タプルとしてリストに登録