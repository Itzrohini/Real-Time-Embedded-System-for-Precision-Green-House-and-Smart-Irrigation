import os
import urllib.parse
import http
import pandas as pd
import re
from time import sleep
from datetime import datetime
from googletrans import Translator
import pygame
from gtts import gTTS
import pickle
filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
translator = Translator()
base = "http://192.168.137.2/"
import urllib.request
def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n
    except http.client.HTTPException as e:
        return e

data_list = []


ct = 0
while True:
    res = transfer(str(ct))
    response = str(res)
    print(response)
    
    # Split the received data
    values = response.split('-')
    if len(values) == 3:
        ph, t, h = values
        #save_to_excel(v1, c1, v2, c2)
        reports = [[t, h, ph]]
        predicted = loaded_model.predict(reports)
        ct=predicted
        print(str(ct[0]))
        tamil_translation = translator.translate(str(ct[0]), src='en', dest='ta').text
        print("Translated to Tamil:", tamil_translation)
        # Initialize the gTTS object with Tamil text
        tts = gTTS(text=tamil_translation, lang='ta')
        tts.save("tamil_speech.mp3")
        pygame.mixer.init()

        # Load and play the audio file in the background
        pygame.mixer.music.load("tamil_speech.mp3")
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the tick rate as needed

        # Clean up resources
        pygame.mixer.quit()
        gt = "https://api.thingspeak.com/update"
        params = {
            "api_key": "UR0CGF2DFJH5YRHC",
            "field5": tamil_translation,
            "field6": str(ph),
            "field7": str(t),
            "field8": str(h)
        }
        encoded_params = urllib.parse.urlencode(params)
        url_with_params = f"{gt}?{encoded_params}"

        # Open the URL
        conn = urllib.request.urlopen(url_with_params)
        
    
    sleep(1)

