import pyxel
import collision import get_title_type
from constans import(
    SCROLL_BORDER_X,
    TITLE_FLOWER_POINT,
    TITLE_MUMMY_POINT,
    TITLE_SLIME1_POINT,
    TITLE_SLIME2_POINT
)
from entitle import Flower,Mummy,Player,Slime

#プレイ画面を更新する
class PlayScene:
    #プレイ画面を更新する
    def update(self):
        game=self.game
        player=game.player
        enemies=game.enemies

        #プレイヤーを更新する
        if player is not None:
            player.update()

            #プレイヤーの移動範囲を制限す流
            player.x=min(max(player.x,game.screen_x),2040)#移動範囲を制限
            player.y=max(player.y,0)

            #プレイヤーがスクロール境界を超えたら画面スクロールする
            if player.x>game.screen_x+SCROLL_BORDER_X:
                last_screen_x=game.screen_x
                game.screen_x=min(player.x-SCROLL_BORDER_X,240*8)
                #240タイル分以上は右にスクロールさせない

                #スクロールした幅に応じて敵を出現させる
                self.spawn_enemy(last_screen_x+128,game.screen_x+127)

    #プレイ画面を描画する
    def draw(self):
        #画面をクリアする
        pyxel.cls(0)

        #フィールドを描画する
        self.game.draw_player()

        #敵を描画する
