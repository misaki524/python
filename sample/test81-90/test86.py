#textという変数に「こんにちは！」という文字列が代入されています
#これをdoc.textというファイルに書き込んでください

path_w = 'doc.txt'

text = 'こんにちは！'

with open(path_w,'w') as f:
    f.write(text)

