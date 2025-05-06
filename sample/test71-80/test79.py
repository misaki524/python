#トランプゲームを想定してカードクラスとデッキクラスの定義を作成してください
#[カードクラス]
#インスタンス変数1:スート(ハート/ダイヤ/スペード/クラブ)
#インスタンス変数2:数字(1~13)
#[カードデッキクラス]
#インスタンス変数1:cards(カードのリスト)
#メソッド1:shuffle(カードをシャッフル)
#メソッド2:draw_card(先頭から1枚引いて引いたカードを返す)

import random

class Card:
  def __init__(self,suit,number):
    self.suit=suit
    self.number=number

class Deck:
  def __init__(self):
    self.cards=[]
    for suit in ["ハート","ダイヤ","スペード","クラブ"]:
      for number in range(1,14):
        card=Card(suit,number)
        self.cards.append(card)
  def shuffle(self):
    random.shuffle(self.cards)
  def draw_card(self):
    return self.cards.pop(0)
