#name,grade,sectionをイニシャライザの引数で初期化するように変更してください

#class Student:
#    def __init__(self):
#        self.name=""
#        self.grade=1
#        self.section="A"
#        self.scores={}

#nameに"鈴木"、gradeに2、sectionに"B"という値を持つStudentオブジェクトを作成してstudentという変数に
#代入してstudentのインスタンス変数nameを出力してください。

class Student:
    def __init__(self,name,grade,section):
        self.name=name
        self.grade=grade
        self.section=section
        self.scores={}

student=Student("鈴木",2,"B")
print(student.name)