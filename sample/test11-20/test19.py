#phone_list=['03', '1111', '2222']
#という電話番号の番号の部分を要素に持つリストがあります。
#このリストの各要素をハイフンで結合した文字列を出力してください

phone_list=['03', '1111', '2222']
result = '-'.join(phone_list)
print(result)