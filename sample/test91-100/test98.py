#Pythonの標準モジュールであるpathlibのPathクラスのcwdメソッドを使って
#作業しているPythonファイルが置いてあるフォルダのpathを出力してください

from pathlib import Path

x=Path.cwd()
print(x)