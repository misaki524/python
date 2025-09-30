import pyxel
from collision import get_tile_type,in_coollision,push_back
from constants import TILE_EXIT,TILE_GEN,TILE_LAVA,TILE_MUSHROOM,TILE_SPIKE

#プレイヤークラス
class Player:
    #プレイヤーを初期化する
    def __init__(self,game,x,y):
        self.game=game#ゲームクラス
        self.x=x#X座標
        self.y=y#Y座標
        self.dx=0#X軸方向の移動距離
        self.dy=0#Y軸方向の移動距離
        self.direction=1#左右の移動方向
        self.jump_counter=0#ジャンプ時間

    #プレイヤーを更新する
    def update(self):
        