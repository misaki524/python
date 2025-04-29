#phone_numberという文字列に何か適当な電話番号を代入してください
#phone_numberが0120で始まるかどうかを確認し0120で始まるなら
#"フリーダイヤルです"と出力してください

phone_number="0120-1111-2222"
number="0120"

if phone_number.startswith(number):
    print("フリーダイヤルです")