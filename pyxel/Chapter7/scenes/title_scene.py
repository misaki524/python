import pyxel

#タイトル画面クラス
class TitleScene:
    #タイトル画面を初期化する
    def __init__(self,game):
        self.game=game#ゲームクラス
        self.alpha=0.0#画面の透明度(0.0:透明,1.0:不透明)
    def update(self):
        #画面の透明度を変更須知
        if self.alpha<1.0:
            self.alpha+=0.015

        #キー入力をチェックする
        if pyxel.btnp(pyxel.KEY_RETURN)or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_B
        ):#EnterキーまたはゲームパッドボタンのBボタンが押された時
          #画面の透明度を不透明にする
          pyxel.dither(1.0)

          #プレイ画面に切り替える
          self.game.change_scene("play")
    def draw(self):
        #画面をクリアにする
        pyxel.cls(0)

        #タイトル画面を描画する
        pyxel.dither(self.alpha)#描画の透明度を設定
        pyxel.bltm(0,0,1,0,0,128,128)#タイルマップを描画する
        pyxel.blt(0,0,1,0,0,128,128,0)
        #テキストを描画する
        pyxel.rect(30,97,67,11,0)
        pyxel.text(34,100,"PRESS ENTER KEY",7)