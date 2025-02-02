import subprocess
import wolframalpha
import pyttsx3
import json
import random
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import shutil
import smtplib
import ctypes
import time
import requests
import winshell
from twilio.rest import Client
from bs4 import BeautifulSoup
from urllib.request import urlopen

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning sir!")
    elif hour < 18:
        speak("Good Afternoon sir!")
    else:
        speak("Good Evening sir!")
    speak("I am jarvis, your assistant, how can i help you sir")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening sir...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing sir...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"Smile said: {query}\n")
    except Exception:
        print("Unable to Recognize your voice sir..") 
        return "None"
    return query.lower()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Replace with environment variables for security
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        server.sendmail(os.getenv('EMAIL_USER'), to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("I am not able to send this email.")

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'jarvis open youtube' in query:
            webbrowser.open("https://youtube.com")
        
        elif 'jarvis open google' in query:
            webbrowser.open("https://google.com")
            
        elif  'jarvis open github' in query:
            webbrowser.open("https://github.com")
            
        elif  'jarvis open telegram' in query:
            webbrowser.open("https://web.telegram.org/a/")

        elif 'jarvis play music' in query:
            music_dir = os.path.expanduser("~/Music")
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No music files found!")

        elif 'jarvis time is' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif 'email' in query:
            speak("What should I say?")
            content = takeCommand()
            speak("Whom should I send it to?")
            to = input("Enter recipient email: ")
            sendEmail(to, content)

        elif 'news' in query:
            try:
                api_key = os.getenv('NEWS_API_KEY')
                url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    for i, article in enumerate(articles[:5], start=1):
                        speak(f"News {i}: {article['title']}")
                        print(f"{i}. {article['title']}")
                else:
                    speak("Couldn't fetch news at the moment.")
            except Exception as e:
                print(e)
                speak("Error fetching news.")

        elif 'shutdown' in query:
            speak("Shutting down the system.")
            os.system('shutdown /s /t 5')

        elif 'restart' in query:
            speak("Restarting the system.")
            os.system('shutdown /r /t 5')

        elif 'say some joke' in query:
            try:
                import pyjokes
                joke = pyjokes.get_joke()
                speak(joke)
                print(joke)
            except ImportError:
                speak("Jokes module not found sir.")

        elif 'calculate' in query:
            try:
                client = wolframalpha.Client(os.getenv('WOLFRAM_API_KEY'))
                query = query.replace("calculate", "")
                res = client.query(query)
                answer = next(res.results).text
                speak(f"The answer is {answer}")
                print(f"The answer is {answer}")
            except Exception:
                speak("Sorry, I couldn't calculate that sir.")

        elif 'jarvis goodbye' in query:
            speak("bye sir, i feel great because of you sir")
            break
