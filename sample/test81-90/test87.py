#動かしているPythonファイルが置いてあるフォルダの中にdoc.txtというファイルを作り「こんにちは！」
#と書き込んでおいてください
#この「こんにちは！」の1つの下の行に「さようなら！」と書き込んでください

path_w = 'doc.txt'

text_new="\nさようなら！"

with open(path_w,'a') as f:
    f.write(text_new)

