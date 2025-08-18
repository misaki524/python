import pyxel


#背景クラス
class Background:
    NUM_STARS=100 #星の数

    #背景を初期化してゲームに登録する
    'インスタンスオブジェクトを作成する時に最初に自動的に呼ばれるメソッド(そのオブジェクトをどういう状態で作るか)'
    'self.〇〇と書くとオブジェクトにデータを持たせられる'
    def __init__(self,game):
        'gameには「ゲーム前たいを管理するクラスのインスタンス」が入っている'
        self.game=game #ゲームへの参照
        '「星」を管理するリスト'
        self.stars=[] #星の座標と速度のリスト

        #星の座標と速度を初期化してリストに登録する
        'for i in range(...)は繰り返し処理。Background.NUM_STARSが100なら0~99を順番に100回繰り返す'
        'その繰り返しの中で毎回ランダムな(x,v,vy)を作ってself.startに追加している'
        for i in range(Background.NUM_STARS):
            x=pyxel.rndi(0,pyxel.width-1) #X座標
            y=pyxel.rndi(0,pyxel.height-1) #Y座標
            vy=pyxel.rndf(1,2.5) #Y方向の速度
            self.stars.append((x,y,vy)) #タプルとしてリストに登録
        #ゲームに背景を登録する
        self.game.background=self

    #背景を更新する
    def update(self):
        for i ,(x,y,vy) in enumerate(self.stars):
            y+=vy
            if y>=pyxel.height:#画面下から出たか
                y-=pyxel.height#画面上に戻す
            self.stars[i]=(x,y,vy)

    #背景を描画する
    def draw(self):
        #タイトル画面以外で銀河を描画する
        if self.game.scene!=self.game.SCENE_TITLE:#★条件の分岐を追加
          pyxel.blt(0,0,1,0,0,120,160)

        #星を描画する
        for x,y,speed in self.stars:
            color=12 if speed>1.8 else 5 #速度に応じて色を変える
            pyxel.pset(x,y,color)

#自機クラス
class Player:
    MOVE_SPEED=2#移動速度
    SHOT_INTERVAL = 6  # 弾の発射間隔（★定数を追加）

    #自機を初期化してゲームに登録する
    def __init__(self,game,x,y):
        self.game=game#ゲームへの残照
        self.x=x#X座標
        self.y=y#Y座標
        self.shot_timer=0#弾発射までの残り時間(変数の追加)

        #ゲームに自機を登録する
        self.game.player=self

    # 自機を更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += Player.MOVE_SPEED

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - 8)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - 8)

        #弾を発射する
        if self.shot_timer>0:#弾発射までの残り時間を減らす
            self.shot_timer-=1

        if pyxel.btn(pyxel.KEY_SPACE) and self.shot_timer==0:
            #自機の弾の生成をする
            Bullet(self.game,Bullet.SIDE_PLAYER,self.x,self.y-3,-90,5)
            #弾発射音を再生する
            pyxel.play(3,0)
            #次の球発射までの残り時間を設定する
            self.shot_timer=Player.SHOT_INTERVAL

    # 自機を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)

#敵クラス
class Enemy:
    KIND_A=0#敵A
    KIND_B=1#敵B
    KIND_C=2#敵C

    #敵を初期化してゲームに登録する
    def __init__(self,game,kind,level,x,y):
        self.game=game
        self.kind=kind#敵の種類
        self.leve=level#強さ
        self.x=x
        self.y=y
        self.life_time=0#生存期間
        #ゲームの敵リストに登録する
        self.game.enemies.append(self)

    #自機の方向の角度を計算する
    def calc_player_angle(self):
        player=self.game.player
        if player is None:#自機が存在しない時
            return 90
        else:#自機が存在する時
            return pyxel.atan2(player.y-self.y,player.x-self.x)

    #敵を更新する
    def update(self):
        #生存時間をカウントする
        self.life_time+=1

        #敵Aを更新する
        if self.kind==Enemy.KIND_A:
            #前方に移動させる
            self.y+=1.2
            #一定時間に毎に自機の方向に向けて発射する
            if self.life_time%50==0:
                player_angle=self.calc_player_angle()
                Bullet(self.game,Bullet.SIDE_ENEY,self.x,self.y,player_angle,2)

        #敵Bを更新する
        elif self.kind==Enemy.KIND_B:
            #前方に移動させる
            self.y+=1

            #経過時間に応じて左右に移動する
            if self.life_time//30%2==0:
                self.x+=1.2
            else:
                self.x-=1.2

        #敵Cを更新する
        elif self.kind==Enemy.KIND_C:
            #前方に移動させる
            self.y+=0.8

            #一定時間毎に4方向に弾を発射する
            if self.life_time%40==0:
                for i in range(4):
                    Bullet(self.game,Bullet.SIDE_ENEY,self.x,self.y,i*45+22,2)


        #敵が画面下から出たら敵リストから登録を削除する
        if self.y>=pyxel.height:#画面したから出たか
            if self in self.game.enemies:
                self.game.enemies.remove(self)#敵をリストから削除する

    #敵を描画する
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.kind*8+8,0,8,8,0)

#弾クラス
class Bullet:
    SIDE_PLAYER=0#自機の弾
    SIDE_ENEY=1#敵の弾

    #弾を初期化してゲームに登録する
    def __init__(self,game,side,x,y,angle,speed):
        self.game=game
        self.side=side
        self.x=x
        self.y=y
        self.vx=pyxel.cos(angle)*speed
        self.vy=pyxel.sin(angle)*speed

        #弾の種類に応じた初期化とリストへの登録を行う
        if self.side==Bullet.SIDE_PLAYER:
            game.player_bullets.append(self)
        else:
            game.enemy_bullets.append(self)
    #弾を更新する
    def update(self):
        #弾の座標を更新する
        self.x+=self.vx
        self.y+=self.vy

        #弾が画面外に出たらリストから登録を削除する
        if (
            self.x<=-8
            or self.x>=pyxel.width
            or self.y<=-8
            or self.y>=pyxel.height
        ):
            if self.side==Bullet.SIDE_PLAYER:
                self.game.player_bullets.remove(self)
            else:
                self.game.enemy_bullets.remove(self)
    #弾を描画する
    def draw(self):
        src_x=0 if self.side==Bullet.SIDE_PLAYER else 8
        pyxel.blt(self.x,self.y,0,src_x,8,8,8,0)

#ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    SCENE_TITLE=0#タイトル画面
    SCENE_PLAY=1#プレイ画面
    SCENE_GAMEOVER=2#ゲームオーバー画面


    def __init__(self):
        #pyxelを初期化する
        pyxel.init(120,160,title="Mega Wing")

        #リソースファイルを読み込む
        pyxel.load("mega_wing.pyxres")

        #ゲームの状態を初期化する
        self.score=0#スコア
        self.scene=None#現在のシーンを追加
        self.background=None#背景
        self.player=None#自機
        self.enemies=[]#敵のリスト
        self.player_bullets=[]#自機の弾のリスト＃リストを追加
        self.enemy_bullets=[]#敵の弾のリスト＃リストを追加


        #背景を生成する(背景はシーンによらず常に存在する)
        Background(self)

        #シーンをタイトル画面に変更する
        self.change_scene(Game.SCENE_TITLE)

        #ゲームの実行を開始する
        pyxel.run(self.update,self.draw)

    #シーンを変更する
    def change_scene(self,scene):
        self.scene=scene

        #タイトル画面
        if self.scene==Game.SCENE_TITLE:
            #自機を削除する
            self.player=None#プレーヤーを削除
            #全ての弾と敵を削除する
            self.enemies.clear()
            self.player_bullets.clear()#自機の弾を更新する処理を追加
            self.enemy_bullets.clear()#敵の弾を更新する処理を追加
            #BGMを再生する
            pyxel.playm(0,loop=True)

        #プレイ画面
        elif self.scene==Game.SCENE_PLAY:
            #プレイ状態を初期化する
            self.score=0#スコアを0に戻す
            self.play_time=0#プレイ時間を0に戻す
            self.level=1#難易度レベルを1に戻す

            #BGMを再生する
            pyxel.playm(1,loop=True)
            #自機を生成する
            Player(self,56,140)

        elif self.scene==Game.SCENE_GAMEOVER:
            #画面表示時間を設定する
            self.display_timer=60
            #自機を削除する
            self.player=None

    #ゲーム全体を更新する
    def update(self):
        #背景を更新する
        self.background.update()

        #自機を更新する
        if self.player is not None:
            self.player.update()

        #敵を更新する
        #ループ中に要素の追加・削除が行われても問題ないようコピーしたリストを使用する
        for enemy in self.enemies.copy():
            enemy.update()
        #自機の弾を更新する
        for bullet in self.player_bullets.copy():#自機の弾を更新する処理を追加
            bullet.update()
        #敵の弾を更新する
        for bullet in self.enemy_bullets.copy():#敵の弾を更新する処理を追加
            bullet.update()

    #シーンを更新する
        if self.scene==Game.SCENE_TITLE:#タイトル画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                pyxel.stop()#BGMを止める
                self.change_scene(Game.SCENE_PLAY)

        elif self.scene==Game.SCENE_PLAY:#プレイ画面
            self.play_time+=1#プレイ時間をカウントする
            self.level=self.play_time//450+1#15秒毎に難易度を上げる
            #15秒(毎秒30フレーム×15)毎に難易度を1上げる

            #敵を出現させる
            spawn_interval=max(60-self.level*10,10)
            if self.play_time%spawn_interval==0:
                kind=pyxel.rndi(Enemy.KIND_A,Enemy.KIND_C)
                Enemy(self,kind,self.level,pyxel.rndi(0,112),-8)

        elif self.scene==Game.SCENE_GAMEOVER:#ゲームオーバー画面
            if self.display_timer>0:#画面表示時間が残っている時
                self.display_timer-=1
            else:#画面表示時間が0になった時
                self.change_scene(Game.SCENE_TITLE)


    #ゲーム全体を描画する
    def draw(self):
        #画面をクリアする
        pyxel.cls(0)

        #背景を描画する
        self.background.draw()

        #自機を描画する
        if self.player is not None:
            self.player.draw()

        #敵を描画する
        for enemy in self.enemies:
            enemy.draw()

        #自機の弾を描画する
        for bullet in self.player_bullets:#自機の弾を更新する処理を追加
            bullet.draw()

        #敵の弾を描画する
        for bullet in self.enemy_bullets:#敵の弾を更新する処理を追加
            bullet.draw()

        #スコアを描画する
        pyxel.text(39,4,f"SCORE{self.score:5}",7)

        #シーンを描画する
        if self.scene==Game.SCENE_TITLE:#タイトル画面
            pyxel.blt(0,18,2,0,0,120,120,15)
            pyxel.text(31,148,"- PRESS ENTER -",6)

        elif self.scene==Game.SCENE_GAMEOVER:#ゲームオーバー画面
            pyxel.text(43,78,"GAME OVER",8)

#ゲームを生成して開始する
Game()
