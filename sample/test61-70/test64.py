#addressesという辞書がありkeyに名前、valueにメールアドレスが入っています。
#この中からメールアドレスのドメインがgmail.comのデータだけを取り出して新しいgmail_addressesという辞書を作ってください
#そしてgmail_addressesを出力してください

addresses={
    "鈴木":"suzukki@example.com",
    "田中":"tanaka@example.com",
    "山田":"yamada@example.com",
    "サプー":"python.supu.vtuber@gmail.com"
}

gmail_addresses={}
for name,addresses in addresses.items():
    if addresses.endswith("@gmail.com"):
        gmail_addresses[name]=addresses
print(gmail_addresses)