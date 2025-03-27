#変数xに10、変数yに2を代入し、「xをかけるyの結果」と「x割るyの結果」の合計を出力
#また「xのy乗」から「xをyで割った余り」を引いた数を出力

#代入
x=10
y=2

#resultに「xをかけるyの結果」と「x割るyの結果」の合計を代入
result=(x*y)+(x/y)
print(result)

#「xのy乗」は**が2つ。「x割るyの結果」は％が割り算。result_1に代入
result_1=(x**y)-(x%y)
print(result_1)