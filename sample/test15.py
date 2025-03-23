#fruitsというリストにりんご」「バナナ」「オレンジ」の要素が入っています。
#このリストの先頭要素を取り出して「先頭は◯◯です」と出力してください。
#また、リストfruitsの末尾要素を取り出して「末尾は◯◯です」と出力してください。

fruits=["りんご","バナナ","オレンジ"]


first_fruits = fruits[0]
last_fruits = fruits[-1]

print(f"先頭は{first_fruits}です")
print(f"末尾は{last_fruits}です")