import sounddevice as sd
import numpy as np

device_count = len(sd.query_devices()) #デバイスの数取得

for i in range(device_count):
    device_info = sd.query_devices(i)
    print(device_info)


