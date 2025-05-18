#外部ライブラリであるqrcodeはQRコードを生成することができるライブラリです。
#qrcodeのmake関数を引数にURLを渡して呼び出すとそのURLをQRコードに変換することができます。
#makeの戻り値はQRコードの画像オブジェクトです。
#QRコードの画像を保存するには画像オブジェクトのsaveメソッドを使います。
#引数には保存するファイル名を指定します。
#動画のURLをQRコードに変換して画像ファイルとして保存してください。

import qrcode

url="https://www.youtube.com/watch?v=v5lpFzSwKbc&t=6301s"
img=qrcode.make(url)
img.save("supu.png")
