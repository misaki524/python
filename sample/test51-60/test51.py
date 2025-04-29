#mail_addressという文字列に何か適当なメールアドレスを代入してください
#mail_addressが@gmail.comで終わるかを確認し@gmail.comで終わるなら"Gmailアドレスです"と出力してください

mail_address="aaabbbccc@gmail.com"

if mail_address.endswith("@gmail.com"):
    print("Gmailアドレスです")