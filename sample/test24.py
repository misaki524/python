#リストodd_numbersに1,3,5,7という奇数の数値が入っています
#リストeven_numbersに2,4,6,8という偶数の数値が入っています
#odd_numbersに9という要素を追加してeven_numbersから8という要素を削除してそれぞれのリストを出力してください
#ただし新しいリストは作らずodd_numbersとeven_numbers自体を直接変更してください

odd_numbers=[1,3,5,7]
even_numbers=[2,4,6,8]
odd_numbers.append(9)
print(odd_numbers)
even_numbers.remove(8)
print(even_numbers)