#このような商品の名前とその商品の単価と数量が入った辞書を要素に持つitemsというリストがあります
#items=[
#    {"name":"りんご","unit_price":100,"quantity":3},
#    {"name":"みかん","unit_price":50,"quantity":5},
#    {"name":"バナナ","unit_price":80,"quantity":2},
#]
#このリストを使って3つの商品の金額を合計した合計金額を計算してください

items=[
    {"name":"りんご","unit_price":100,"quantity":3},
    {"name":"みかん","unit_price":50,"quantity":5},
    {"name":"バナナ","unit_price":80,"quantity":2},
]

total = 0
for num in items:
    price=num["unit_price"]*num["quantity"]
    total += price
print(total)