#class Student:
#    def __init__(self,name,grade,section):
#        self.name=name
#        self.grade=grade
#        self.section=section
#        self.scores={}

#テストの点数の合計を返すメソッドtotal_scoreを追加してください

#student=Student("鈴木",2,"B")

#数学:80点、英語:70点、国語:90点を追加したあとstudeneのテストの点数を出力してください

class Student:
    def __init__(self,name,grade,section):
        self.name=name
        self.grade=grade
        self.section=section
        self.scores={}

    def add_score(self,subject,score):
        self.scores[subject]=score

    def total_score(self):
        return sum(self.scores.values())

student=Student("鈴木",2,"B")
student.add_score("数学",80)
student.add_score("英語",70)
student.add_score("国語",90)
print(student.total_score())
