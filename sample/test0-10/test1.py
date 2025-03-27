#int型の100を文字列に型変換してxに代入
#文字型の"100.1"をfloat型に型変換してyに代入
#float型の100.0をint型に型変換してzに代入
#それぞれの値と型をprint関数を使用して出力

#int型の100を文字列に型変換してxに代入
x=100
print(str(x)) #str(a)で文字列にデータ型変換
print(type(str(x)))

#文字型の"100.1"をfloat型に型変換してyに代入
y="100.1"
print(float(y)) #float(a)で浮動小数点数にデータ型変換
print(type(float(y)))

#float型の100.0をint型に型変換してzに代入
z=100.1
print(int(z))
print(type(int(z)))#int(a)で浮動小数点数をint型変換

#それぞれの値と型をprint関数を使用して出力
x=str(100)
y=float("100.1")
z=int(100.1)
print(x,y,z)
print(type(x),type(y),type(z))
