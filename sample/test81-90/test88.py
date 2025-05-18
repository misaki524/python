#動かしているPythonファイルが置いてあるフォルダの中にdoc.txtというファイルを作り
#1行目に「こんにちは！」
#2行目に「さようなら！」
#と書き込んでおいて下さい
#doc.txt中身を全て読み込んでprint関数で出力してください

path_w = 'doc.txt'

with open(path_w,"r") as f:
    text=f.read()

print(text)