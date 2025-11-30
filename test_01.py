data=[ ]
#i と j のすべての組み合わせのうち、i と j が違うものだけをリストに入れる
for i in [1,2,3]:#は 1 → 2 → 3 の順に動く
    for j in [1,2]:#j は 1 → 2 の順に動く
        if i !=j:#と j が 違うときだけ タプル (i, j) を data に追加
            data.append((i,j))
print(data)