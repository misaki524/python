#ng_numbersというリストに4,9,13という要素が入っています
#1から20までの数値を1ずつ出力してng_numbersに含まれている数値の場合は出力をスキップしてください


ng_numbers=[4,9,13]

for i in range(1,21):
    if i in ng_numbers:
        continue
    print(i)
