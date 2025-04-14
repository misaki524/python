#リストnumbersに1,1,2,3,4,5の要素が入っています
#numbersから重複した要素を取り除いて新しいリストを作成してください


numbers = [1,1,2,3,4,5]
new_numbers = list(set(numbers))
print(new_numbers)