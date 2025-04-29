#keyが1,valueが「睦月」
#keyが2,valueが「如月」
#keyが3,valueが「弥生」
#という要素を持つ辞書monthsがあります

#この辞書を使って
#「1月は和風月名で睦月です」
#「2月は和風月名で如月です」
#「3月は和風月名で弥生です」
#と1ずつ出力してください

months={1:"睦月",2:"如月",3:"弥生"}

for key,value in months.items():
    print(f"{key}月は和風月名で{value}です")