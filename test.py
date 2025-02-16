import sounddevice as sd
import numpy as np

# サンプルレート、録音時間、チャンネル数の設定
fs = 44100  # サンプルレート
duration = 5  # 録音時間（秒）
channels = 1  # チャンネル数（モノラル）

# 録音開始
print("録音開始")
audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
sd.wait()  # 録音が終了するまで待機
print("録音終了")

# 録音したデータを表示（オプション）
print(audio_data)
