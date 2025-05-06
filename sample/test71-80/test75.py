#scoresはテストの点数を辞書で持っています

#class Student:
#    def __init__(self,name,grade,section):
#        self.name=name
#        self.grade=grade
#        self.section=section
#        self.scores={}

#テストの点数を追加するメソッドadd_scoreを追加してください(科目メイトその科目の点数を引数で受け取る)

#student=Student("鈴木",2,"B")

#数学:80点、英語:70点、国語:90点を追加しstudeneのインスタンス変数scoresを出力してください

class Student:
    def __init__(self,name,grade,section):
        self.name=name
        self.grade=grade
        self.section=section
        self.scores={}

    def add_score(self,subject,score):
        self.scores[subject]=score

student=Student("鈴木",2,"B")
student.add_score("数学",80)
student.add_score("英語",70)
student.add_score("国語",90)

print(student.scores)
