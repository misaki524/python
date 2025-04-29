#drink_priceという関数を作成してください
#引数1:drink_size(S/M/L)
#Sは100円、Mは200円、Lは300円
#引数2:has_whip(True/False)
#ホイップ有りは＋100円
#戻り値:飲み物の価格
#Mサイズのドリンクにホイップクリームをトッピングした場合の価格とLサイズのドリンクの価格を出力してください

def drink_price(drink_size,has_whip=False):
    price=0
    if drink_size=="S":
        price += 100
    elif drink_size=="M":
        price += 200
    elif drink_size=="L":
        price += 300

    if has_whip:
        price += 100
    return price

drink_price_M_whip=drink_price("M",True)
print(drink_price_M_whip)
drink_price_L=drink_price("L")
print(drink_price_L)