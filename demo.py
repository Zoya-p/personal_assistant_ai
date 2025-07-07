import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import pandas as pd
import random
import time
import json


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def parse_email(spoken_email):
    spoken_email = spoken_email.lower()
    spoken_email = spoken_email.replace(" at ", "@")
    spoken_email = spoken_email.replace(" dot ", ".")
    spoken_email = spoken_email.replace(" underscore ", "_")
    spoken_email = spoken_email.replace(" dash ", "-")
    spoken_email = spoken_email.replace(" space ", "")
    spoken_email = spoken_email.replace(" ", "")
    return spoken_email

def speak(audio):
    print(f"\U0001F9E0 Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")
    speak("I am your virtual assistant, Dean. Please tell me how may I help you.")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\U0001F3A4 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("\U0001F9E0 Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")  
        return "None"
    return query.lower()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('aijarvis79@gmail.com', 'password')  
        server.sendmail('aijarvis79@gmail.com', to, content)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


contacts_file = 'contacts.json'
try:
    with open(contacts_file, 'r') as f:
        contacts = json.load(f)
except FileNotFoundError:
    contacts = {}

df_real = pd.read_csv("gmail_emails_classified.csv")
df_real['subject'] = df_real['subject'].fillna('')
df_real['body'] = df_real['body'].fillna('')
df_real['text'] = df_real['subject'] + " " + df_real['body']

songs = [
    r"D:\\music\\Aha Tamatar Bade Mazedaar Arnav Chaphekar (DjPunjab.Farm).mp3",
    r"D:\\music\\gentle-rain-for-relaxation-and-sleep-337279.mp3",
    r"D:\\music\\soft-brown-noise-299934.mp3"
]


if __name__ == "__main__":
    wishMe()
    speak("Voice spam filter is activated. Say 'spam' to check emails or 'exit' to stop.")

    while True:
        query = takeCommand()

        if 'exit' in query:
            speak("Deactivating spam warning system. Goodbye.")
            break

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            speak("What should I search on YouTube?")
            topic = takeCommand()
            webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")

        elif 'open google' in query:
            speak("What should I search on Google?")
            topic = takeCommand()
            webbrowser.open(f"https://www.google.com/search?q={topic}")

        elif 'play music' in query:
            song = random.choice(songs)
            os.startfile(song)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Dean, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Elite BooK\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'send email' in query:
            speak("Who should I send the email to?")
            recipient_name = takeCommand()
            if recipient_name in contacts:
                to = contacts[recipient_name]
            else:
                speak("Dean, please tell me their email. Say it like name at domain dot com")
                spoken_email = takeCommand()
                to = parse_email(spoken_email)
                contacts[recipient_name] = to
                with open(contacts_file, 'w') as f:
                    json.dump(contacts, f)

            speak("What should I say?")
            content = takeCommand()

            speak(f"You said: {content}")
            speak(f"Sending to: {to}. Should I send it now? Say yes or no.")
            confirmation = takeCommand()

            if 'yes' in confirmation:
                success = sendEmail(to, content)
                if success:
                    speak("Email has been sent!")
                else:
                    speak("Sorry Dean. Email could not be sent.")
            else:
                speak("Email canceled, Dean.")

        elif 'spam' in query:
            if 'Label' in df_real.columns:
                spam_emails = df_real[df_real['Label'].str.lower() == 'spam']
                if spam_emails.empty:
                    speak("You are safe, Dean. No spam emails today.")
                else:
                    speak(f"Dean, you have {len(spam_emails)} spam emails.")
                    for idx, row in spam_emails.iterrows():
                        speak(f"Spam alert: {row['subject']}")
            else:
                speak("Spam labels not available in the email data.")

        elif 'urgent email' in query:
            urgent_emails = df_real[df_real['Predicted_Category'] == 'urgent']
            if urgent_emails.empty:
                speak("You have no urgent emails.")
            else:
                speak(f"You have {len(urgent_emails)} urgent emails.")
                for idx, row in urgent_emails.iterrows():
                    speak(f"Subject: {row['subject']}")

        elif 'meeting email' in query:
            meeting_emails = df_real[df_real['Predicted_Category'] == 'meeting']
            if meeting_emails.empty:
                speak("You have no meeting emails.")
            else:
                speak(f"You have {len(meeting_emails)} meeting emails.")
                for idx, row in meeting_emails.iterrows():
                    speak(f"Subject: {row['subject']}")

        elif 'schedule email' in query:
            schedule_emails = df_real[df_real['Predicted_Category'] == 'schedule']
            if schedule_emails.empty:
                speak("You have no schedule emails.")
            else:
                speak(f"You have {len(schedule_emails)} schedule emails.")
                for idx, row in schedule_emails.iterrows():
                    speak(f"Subject: {row['subject']}")

        elif 'personal email' in query:
            personal_emails = df_real[df_real['Predicted_Category'] == 'personal']
            if personal_emails.empty:
                speak("You have no personal emails.")
            else:
                speak(f"You have {len(personal_emails)} personal emails.")
                for idx, row in personal_emails.iterrows():
                    speak(f"Subject: {row['subject']}")

        elif 'information email' in query:
            info_emails = df_real[df_real['Predicted_Category'] == 'information']
            if info_emails.empty:
                speak("You have no information emails.")
            else:
                speak(f"You have {len(info_emails)} information emails.")
                for idx, row in info_emails.iterrows():
                    speak(f"Subject: {row['subject']}")
