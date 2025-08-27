#keyが1、valueが「睦月」
#keyが2、valueが「如月」
#keyが3、valueが「弥生」
#という要素を持つ辞書monthsがあります

#keyが3の要素を削除して削除した要素のvalueと削除後のmonthsを出力してください

months={1:"睦月",2:"如月",3:"弥生"}
del months[3]
print(months)

#別回答
#months={1:"睦月",2:"如月",3:"弥生"}
#remove=months.pop[3]
#print(remove)
#print(months)