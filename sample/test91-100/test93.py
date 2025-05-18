#x=6
#y=10

#numbers=[1,4,0,12,6]

#try:
#    result=y/numbers[x]
#    print(result)
#except IndexError:
#    print("リストの範囲を超えるインデックスです")
#except ZeroDivisionError:
#    print('ゼロで割ることはできません')

#リストnumbersの範囲を超えてインデックスが指定された場合もゼロで割り算が行なわれた場合も一律
#「エラーが発生しました」と出力するように修正してください

x=2
y=10

numbers=[1,4,0,12,6]

try:
    result=y/numbers[x]
    print(result)
except (IndexError,ZeroDivisionError):
    print("エラーが発生しました")
