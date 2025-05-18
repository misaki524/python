#動かしているPythonファイルが置いてあるフォルダの中にdoc.txtというファイルを作り
#1行目に「こんにちは！」
#2行目に「さようなら！」
#と書き込んでおいて下さい
#doc.txtを読み込み1行1行がリストの要素となるリストを作成しそのリストを出力してみてください


path_w = 'doc.txt'

with open(path_w,"r") as f:
    lines=f.readlines()

print(lines)