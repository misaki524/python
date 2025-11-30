#シーン(画面)モジュール

#scenesフォルダのクラスを__init__.pyでインポートすることで
#from scenes import PlayScene,TitleScene,GameOverScene
#のようにまとめてインポートできるようにする

from .clear_scene import ClearScene #クリア画面クラス
from .gameover_sceene import GameOverScene #ゲームオーバー画面クラス
from .play_scene import PlayScene #プレイ画面クラス
from .title_scene import TitleScene #タイトル画面クラス
