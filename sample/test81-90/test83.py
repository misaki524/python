#今、編集して動かしているPythonファイルと同じフォルダに以下のようなPythonファイルがあるとします。
#ファイル名はmoudule.pyです。
#このファイルをimportしてCardクラスを使ってスートがハートで数字が1のカードを作成してそのカードのスートと数字を出力してください。
#また、URLを出力してください。

from moudule import Card,URL

card=Card("ハート",1)
print(f"{card.suit}{card.number}")
print(URL)
