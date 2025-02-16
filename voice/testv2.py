import sounddevice as sd
import numpy as np

# サンプルレート、録音時間、チャンネル数の設定
fs = 44100  # サンプルレート
duration = 5  # 録音時間（秒）
channels = 1  # チャンネル数（モノラル）

# 生成する音（例: サイン波）
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440Hzのサイン波

# 再生
print("再生開始")
sd.play(audio_data, samplerate=fs)
sd.wait()  # 再生が終了するまで待機
print("再生終了")
