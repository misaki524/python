#xとyに適当な数値を代入します
#1,4,0,12,6という要素を持つリストnumbersがあります
#numbersからインデックスがxの要素を取り出してyをその要素で割った結果を出力してください
#ただし、numbersから要素を取り出すときにリストの範囲を超えるインデックスを指定しまった場合には
#「リストの範囲を超えるインデックスです」と出力してください
#また、0で割られた場合は「ゼロで割ることはできません」と出力してください

x=6
y=10

numbers=[1,4,0,12,6]

try:
    result=y/numbers[x]
    print(result)
except IndexError:
    print("リストの範囲を超えるインデックスです")
except ZeroDivisionError:
    print('ゼロで割ることはできません')