
import random

#ゲームの開始
print('数当てゲームスタート')
print('私が1~9までの数値を使ってランダムな数を作ります')
print('あなたは1桁から9桁を指定してください')

#桁数入力
while True:
  n = int(input('何桁の数字でゲームをしますか？(1~9):'))
  #1~9の入力が入力がされたらループを抜ける
  if 1 <= n <= 9:
    break
  print('1~9の数字を入力してください')
#正解の数
numbers = [1,2,3,4,5,6,7,8,9]
secret_numbers = random.sample(numbers,n) #numbersのリストからn子の値をランダムに選択しsecret_numbersのリストに格納

#試行回数を初期化
trial_count = 0
#ユーザーから推測した数字を受け取って正解までループを回す
while True:
  guess_number = input(f'{n}桁の数字を入力してください')

  #試行回数をカウントアップ
  trial_count += 1
  print(f'{trial_count}回目の解答です') #f-string(f文字列)_文字列の部分は固定し、数字の部分だけ変更したい場合に使用
