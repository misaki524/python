#14,32,80,1,9
#という要素が入っているnumbersというリストがあります
#sum_and_avgという関数を作成します
#sum_and_avg関数は引数にリストを受け取りそのリストの値の合計と平均を返す関数です
#このsum_and_avg関数を使ってnumbersの合計と平均を出力してください

numbers=[14,32,80,1,9]

#total = sum(numbers)
#sum_and_avg = total / len(numbers)
#print(f"合計値: {total}")
#print(f"平均値: {sum_and_avg}")

def sum_and_avg(nums):
    total=sum(nums)
    avg=total / len(nums)
    return total,avg

total,avg=sum_and_avg(numbers)
print(total)
print(avg)
