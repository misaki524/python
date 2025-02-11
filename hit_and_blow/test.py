
import random

def check_hit_and_blow(secret,guess):
  """"ユーザーの推測値と正解を比較してヒットとブローの数を返す"""
  #ヒットとブロー変数の初期化
  hit = 0
  blow = 0

  #ヒットのカウント(ヒット=数字と位置が合っている)
  for i in range(len(secret)):
    if secret[i] == guess[i]:
      hit += 1

  #重複のカウント
  hit_and_blow = 0
  for num in secret:
    if num in guess:
      hit_and_blow += 1

  #ブロー＝重複数からヒット数を引く
  blow = hit_and_blow - hit

  return hit,blow

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
print(secret_numbers)

#試行回数を初期化
trial_count = 0
#ユーザーから推測した数字を受け取って正解までループを回す
while True:
  guess_number = input(f'{n}桁の数字を入力してください')

  #入力の整数のリストに変換
  guess_list = []
  for char in guess_number:
    guess_list.append(int(char))
  print(guess_list)

  #試行回数をカウントアップ
  trial_count += 1
  print(f'{trial_count}回目の解答です') #f-string(f文字列)_文字列の部分は固定し、数字の部分だけ変更したい場合に使用

  #ユーザーの推測値を正解と比較しヒット数とブロー数を返す
  hit,blow = check_hit_and_blow(secret_numbers,guess_list)

  #結果表示
  if hit == n:
    print(f'正解！ゲームクリアです！正解＝{secret_numbers}')
    print(f'{trial_count}回で正解しました')
    break
  else:
    print(f'ヒット={hit},ブロー＝{blow}')
