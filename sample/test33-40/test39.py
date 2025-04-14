#1,12,5,10,13,7,90の要素を持つ集合numbersがあります。
#この集合の2番目に大きい要素を取り出して出力してください。

numbers={1,12,5,10,13,7,90}
new_numbers=sorted(numbers)
second_numbers=new_numbers[-2]
print(second_numbers)