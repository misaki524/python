#xに何か適当な数値を代入しxを0で割った結果を出力するコードを書き
#例外が発生したら「ゼロで割ることはできません」と出力してください

x=10



try:
    result=x/0
    print(result)
except ZeroDivisionError:
    print('ゼロで割ることはできません')