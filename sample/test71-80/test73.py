#Studentというクラス定義を書いてください
#インスタンス変数
#・nameは名前(文字列)→空文字で初期化
#・gradeは学年(int)→1で初期化
#・sectionはクラス(文字列)→"A"で初期化
#・scoresはテストの点数(辞書)→空の辞書で初期化
#これらのインスタンス変数をイニシャライザで初期化します

class Student:
    def __init__(self):
        self.name=""
        self.grade=1
        self.section="A"
        self.scores={}
