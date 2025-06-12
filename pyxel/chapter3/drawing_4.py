import pyxel

pyxel.init(160,120,title="sample drawing")

x=80



pyxel.circ(80,60,8,3) #円を書く
pyxel.circb(80,60,8,7) #円の輪郭を書く
pyxel.line(76,57,76,60,0) #左目
pyxel.line(82,57,82,60,0) #右目
pyxel.line(76,63,82,63,0) #口
pyxel.pset(75,62,0) #口の左端
pyxel.pset(83,62,0) #口の右端

pyxel.show() #画面を表示する
