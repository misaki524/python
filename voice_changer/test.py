import pyaudio
import wave

pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    device_info = pa.get_device_info_by_index(i)
    print(device_info)