#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import speech_recognition as sr
import pyttsx3 

def load_page_data(file_path):
    page_data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            page_data.append(row)
    return page_data

def scrape_webpage_summary(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            summary = "Summary not found on the webpage."
            return summary
        else:
            return "Failed to retrieve the webpage."
    except Exception as e:
        return f"Error: {str(e)}"

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say a page name:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio).lower()
        print(f"User said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None  
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None  

def speak_text(text, language_code):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  
    voices = engine.getProperty('voices')
    for voice in voices:
        if language_code in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def main():
    downloads_folder = os.path.expanduser("~" + "/Downloads")
    file_name = '2.csv'
    file_path = os.path.join(downloads_folder, file_name).replace('\\', '/')
    page_data = load_page_data(file_path)

    while True:
        user_input = recognize_speech()  

        if user_input == 'exit':
            print("Goodbye!")
            break

        found_page = None
        for page in page_data:
            if user_input == page['Page Name'].lower():
                found_page = page
                break

        if found_page:
            url = found_page['URL']
            webbrowser.open(url)
            print(f"Opening '{found_page['Page Name']}' page at {url}")

            summary = found_page.get('Summary', 'Summary not available.')
            
            target_language = input("Enter the target language for translation (e.g., 'fr' for French, 'en' for English): ")
            
            translated_summary = translate_text(summary, target_language)

            print(f"Translated Summary: {translated_summary}")

            speak_text(translated_summary, target_language)
        else:
            print("Page not found. Please try again.")

if __name__ == "__main__":
    main()


# In[ ]:




