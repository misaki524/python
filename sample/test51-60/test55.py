#namesというリストに
#鈴木、田中、山田、佐藤、伊藤
#要素が入っています
#それぞれに「さん」をつけて1人ずつ名前を出力してください


names=['鈴木','田中','田中','佐藤','伊藤']

for name in names:#for 変数 in リスト名:
    print(f"{name}さん")#f文字列で文字列の中に変数を埋め込める