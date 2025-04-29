#14,32,80,1,9
#という要素が入っているnumbersというリストがあります
#is_evenという関数を作ります
#is_even関数は引数に数値を1つ受け取りその数値が偶数か奇数かを判定して偶数ならTrue、奇数ならFalseを返す関数です
#is_even関数を使ってnumbersの要素が偶数か奇数かを判定し「◯◯は偶数」「◯◯は奇数」と判定結果を出力してください


numbers=[14,32,80,1,9]

def is_even(n):
    return n % 2 ==0
for num in numbers:
    if is_even(num):
        print(f"{num}は偶数")
    else:
        print(f"{num}は奇数")

