#pythonの標準モジュールであるosのgetenv関数を使って
#HOMEという環境変数に設定されている値を出力してください

import os

x=os.getenv("HOME")
print(x)