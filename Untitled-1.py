import speech_recognition as sr
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

opts = {
    "aliaz":('Алиса','Алиска','Алисочка'),
    "tbr":('скажи','покажи'),
    "terminal":{
        "ctime":('текущее время','сейчас времнени','который час'),
        "music":('включи музыку','воспроизведи мелодию','включи песню'),
        "joke":('расскажи шутку','расскажи анегдот')
    }
}

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer,audio):
    try:
        voice = recognizer.recognize_google(audio, language= "ru-RU")
        print("[log] Распознаю..."+voice)

        if voice.startswith(opts["aliaz"]):
            terminal = voice

            for x in opts['aliaz']:
                terminal = terminal.replace(x,"").strip()

            for x in opts['tbr']:
                terminal = terminal.replace(x,"").strip()  

            terminal =  recognizer_terminal(terminal)     
            exec_terminal(terminal['terminal'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан")   
     except sr.RequestError as e:
         print("[log] Неизвестная ошибка")     

def recognizer_terminal(terminal):
    RC = {'terminal': '','percent':0}
    for c,v in opts['terminal'].items():

        for x in v:
            vrt = fuzz.ratio(terminal,x)
            if vrt > RC['percent']:
                RC['terminal'] = c
                RC['percent'] = vrt
    return RC            

def exec_terminal(terminal):   
    if terminal == 'ctime':

        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))     

    elif terminal == "joke":
        speak("У меня нету анегдотов ахахаха")

    else:
        print('Команда не распознана')    


r = sr.Recognizer()
m = sr.Microphone(device_index=3)

with m as source:
    r.adjust_for_ambient_noise(source)

    speak_engine = pyttsx3.init()

    voices = speak_engine.getProperty('voices')
    speak_engine.setProperty('voice',voices[4].id)

speak("Добрый вечер я диспетчер")
speak("ЧЕ НАДО ОТ АЛИСЫ")    

stop_listn = r.listen_in_background(m,callback)
while True: time.sleep(0.1)


# r = sr.Recognizer()
# with sr.Microphone(device_index=3) as source:
#     print("Cкажите что нибудь ...")
#     audio = r.listen(source)

# query = r.recognize_google(audio, language="ru-RU")
# print("Вы сказали:" + query.lower())