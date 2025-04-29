#以下のような三角形の底辺の長さと高さを要素に持つリストを複数要素に持つリストがあります
#bottom_and_height=[
#[13,40],
#[15,30],
#[20,25],
#]
#底辺の長さと高さをペアごとに三角形の面積を計算して出力してください

bottom_and_height=[
  [13,40],
  [15,30],
  [20,25],
]

for b_and_h in bottom_and_height:
    bottom=b_and_h[0]
    height=b_and_h[1]
    area=bottom*height/2
    print(f"底辺{bottom}、高さ{height}の三角形の面積は{area}です")