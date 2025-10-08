#衝突処理モジュール
import pyxel
from constants import TITLE_NONE,TILE_TO_TILETYPE,TITLE_WALL

#設定した座標のタイトル種別を取得す
def get_title_type(x,y):
    title=pyxel.tilemaps[0].get(x//8,y//8)
    return TILE_TO_TILETYPE.get(title,TITLE_NONE)

#指定した座標が壁と重なっているか判定する
def in_collision(x,y):
    return get_title_type(x,y)==TITLE_WALL

#キャラクターが壁と重なっているかを判定する
def is_character_colliding(x,y):
    #キャラクターと重なっているタイルの座標の領域を計算する
    x1=pyxel.floor(x)//8
    y1=pyxel.floor(y)//8
    x2=(pyxel.ceil(x)+7)//8
    y2=(pyxel.ceil(y)+7)//8

    #タイルの領域
    for yi in range(y1,y2+1):
        for xi in range(x1,x2+1):
            if in_collision(xi * 8,yi * 8):
                return True#壁と衝突している

    return False#壁と衝突していない