import speech_recognition as sr
import pyttsx3
import requests
import datetime
import json
import nltk
from nltk.tokenize import word_tokenize

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service.")
            return ""

def get_weather(city):
    api_key = "dbcee6578a60c82a8bb67071b9601724"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Sorry, I could not find the weather for that location.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    speak(f"Here are the search results for {query}.")
    print(f"Opening web search for: {url}")

def set_reminder(reminder_text):
    reminder_time = datetime.datetime.now() + datetime.timedelta(seconds=10)  # Simple 10 second reminder
    speak(f"Reminder set for: {reminder_text}. I will remind you in 10 seconds.")
    # This is just for demonstration; you would need a more robust scheduling system for real reminders
    print(f"Reminder: {reminder_text} at {reminder_time}")

def process_command(command):
    if "weather" in command:
        city = command.split("in")[-1].strip()  # Extract city name
        get_weather(city)
    elif "search" in command:
        query = command.split("search for")[-1].strip()
        search_web(query)
    elif "remind me" in command:
        reminder_text = command.split("remind me")[-1].strip()
        set_reminder(reminder_text)
    else:
        speak("I am not sure how to help with that.")

def main():
    speak("Hello! I am your voice-controlled assistant.")
    while True:
        command = listen()
        if command == "exit":
            speak("Goodbye!")
            break
        process_command(command)

if __name__ == "__main__":
    main()
