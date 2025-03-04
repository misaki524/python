import sounddevice as sd #オーディオの入出力の行うためのライブラリ
import pyaudio #音声入力や出力を管理するための別のライブラリ
import numpy as np #数値計算を行うライブラリ



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
  return

# マイクインデックスを取得
mic_index = get_mic_index(pa)
if mic_index is not None:
    # 録音の長さを設定して録音開始
    duration = 5  # 秒
    audio_data = record(pa, mic_index, duration)

#辞書型
##辞書型(dict型)とはkeyと値(value)がセットになったデータ型

#sd.query_devices(i)について
#sounddevice ライブラリの関数の一つで、システムに接続されているオーディオデバイス（マイクやスピーカーなど）の情報を取得。
#i は、デバイスの番号（インデックス）です。例えば、i = 0 は最初のオーディオデバイス、i = 1 は2番目のデバイスを指す。
#この関数が返すのは辞書型（dict）のデータ。
#辞書型とはkeyと値(value)がセットになったデータ型。