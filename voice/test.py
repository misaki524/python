import sounddevice as sd #オーディオの入出力の行うためのライブラリ
import pyaudio #音声入力や出力を管理するための別のライブラリ
import numpy as np #数値計算を行うライブラリ
import soundfile as sf
import matplotlib.pyplot as plt  # グラフ描画用のライブラリ
import wave
import os
import librosa





#sounddeviceライブラリの関数で接続されているオーディオデバイスの情報を取得
#query_devices()感ん数が返したデバイスのリストの長さを取得しdevice_count変数にその数を代入する
#device_count = len(sd.query_devices()) #デバイスの数取得


def get_mic_index(pa):

  #マイクチャンネル一覧をリストに追加する。17行目まで関数にまとめる
  #マイクデバイスのインデックスを格納するための空のリストmic_listを作成
  mic_list=[]#max_input_channelsが1以上のマイクチャンネルのみを検索するためにmic_listという変数を定義
  #接続されているすべてのデバイスに対して繰り返し処理を行う。
  #device_count は、接続されているデバイスの数で、i は各デバイスのインデックス。
  device_count = len(sd.query_devices())#get_device_count関数を作成
  for i in range(device_count):
      #sounddevice ライブラリの query_devices() 関数を使用して、デバイス番号 i に関する情報を取得。
      #この情報には、デバイスの名前、入力・出力チャンネル数などが含まれている。
      device_info = sd.query_devices(i)
      #forループの中で「max_input_channels」というキーの中に「num_of_input_ch」の値を入れる
      num_of_input_ch=device_info['max_input_channels']
      #num_of_input_chという変数にはオーディオデバイスが持っている「入力チャンネル数」が入っている
      #0を超える場合に「max_input_channels」にindex値を追加
      if num_of_input_ch>0:
          #デバイス1: 入力チャンネル数 1（マイクがある） → リストに追加
          #デバイス2: 入力チャンネル数 0（マイクがない） → リストに追加しない
          #デバイス3: 入力チャンネル数 2（マイクがある） → リストに追加
          #mic_list.append()はmic_listに追加
          mic_list.append(device_info['index'])
  return mic_list[0]

#pyaudio ライブラリを使って、オーディオの設定やデバイスの操作を管理するオブジェクトを作成。
pa=pyaudio.PyAudio()

def record(pa,index,duration):
  sampling_rate=44100
  frame_size=1024

  #ストリームを開く
  stream=pa.open(format=pyaudio.paInt16,channels=1,
                rate=sampling_rate,
                input=True,
                input_device_index=index,
                frames_per_buffer=frame_size)
  #ループの設定
  dt=1/sampling_rate
  #総録音時間(duration)をデータ記録間隔(dt)で割ることでdurationを構成する総データ点いくつあればいいかを計算する
  n=int(((duration/dt)/frame_size))
  print(n)

#録音する
  waveforom=[] #waveforomは入れ物最初空だがループ回るごとにstream.read(frame_size)に取得したフレームサイズ分のデータを追加していく
  print('start')
  for i in range(n):
    frame=stream.read(frame_size)
    waveforom.append(frame)

#ストリームの終了
  stream.stop_stream()
  stream.close()

#データをまとめる
  waveforom=b"".join(waveforom)#フレームごとに録音されたデータを結合させ、1つの長い波型をデータにする

#バイトデータを数値データに変換
#（bytes）を numpy の配列に変換するための関数。音声データが数値（整数）の配列にする
  byte_to_num=np.frombuffer(waveforom,dtype="int16")

#最大値を計算
#2**16 は16ビットで表現できる最大の値 (65536) を意味します。
#その半分が正の最大値なので、65536 / 2 = 32768 となり、その1つ少ない値が最大振幅 32767 です
  max_value=float((2**16/2)-1)

  return byte_to_num,sampling_rate
def graph_plot(x,y):
  #波風をグラフにする関数
  #グラフ日設定
  fig,ax=plt.subplots()
  ax.set_xlabel('Time[s]')
  ax.set_ylabel('Amplitude')
  #データのプロット
  ax.plot(x,y)
  plt.show()
  plt.close()
  return

try:
  # マイクインデックスを取得
  mic_index = get_mic_index(pa)
  if mic_index is not None:
    # 録音の長さを設定して録音開始
    duration = 5  # 秒
    #waveform の長さ（録音された音声データのサンプル数）と、その内容（音声データそのもの）を表示しています。
    #len(waveform) で、録音されたデータの長さ（サンプル数）を取得し、waveform には実際の音声データが格納されています。
    waveform,sampling_rate = record(pa, mic_index, duration)
    print(len(waveform),waveform)

    # WAVファイルに保存する
    save_path = 'recorded.wav'  # ファイル保存先

    #ボイスチェンジする
    n_steps=8
    waveform_shfted=librosa.effects.pitch_shift(waveform,sr=sampling_rate,n_steps=n_steps)

    # waveform_shfted を int16 に戻してから書き込む
    # ピッチシフト後のデータは float32 なので、int16 型に戻す必要がある
    waveform_shfted_int16 = np.int16(waveform_shfted * 32767)  # 音量の調整（-32768から32767の範囲）


    # ファイル保存
    with wave.open(save_path, mode='wb') as wb:
        wb.setnchannels(1)  # モノラル
        wb.setsampwidth(2)  # 16bit=2byte
        wb.setframerate(sampling_rate)
        # データをWAVファイルに書き込む
        wb.writeframes(bytearray(waveform))
    print(f"音声を {save_path} に保存しました。")

    # 音声データを -1.0 から 1.0 の範囲に正規化
    waveform = waveform.astype(np.float32)  # np.int16 -> np.float32 へ変換
    waveform = waveform / 32768.0  # 16bitの音声データは -32768 から 32767 なので、32768で割る

    #グラフをプロットする
    dt=1/sampling_rate
    t=np.arange(0,len(waveform)*dt,dt)#np.arange()で時間軸を作成取得済みの振り幅(y軸)と共に
    waveform = waveform / 32768.0
    graph_plot(t,waveform)#graph_plot関数に渡す

finally:
  # 必ず終了処理を実行
  pa.terminate()
  print('end')



#辞書型
##辞書型(dict型)とはkeyと値(value)がセットになったデータ型

#sd.query_devices(i)について
#sounddevice ライブラリの関数の一つで、システムに接続されているオーディオデバイス（マイクやスピーカーなど）の情報を取得。
#i は、デバイスの番号（インデックス）です。例えば、i = 0 は最初のオーディオデバイス、i = 1 は2番目のデバイスを指す。
#この関数が返すのは辞書型（dict）のデータ。
#辞書型とはkeyと値(value)がセットになったデータ型。