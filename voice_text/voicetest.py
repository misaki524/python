import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source,duration =1)
    print('マイクに向かってタメ口で話しかけてください')
    audio=r.listen (source)
