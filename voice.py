import pyttsx3
import datetime
import wikipedia
import os
import webbrowser
import pyjokes
import pywhatkit as kit
import streamlit as st

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Global flag to check if the engine is speaking
is_speaking = False

# Define the speak function
def speak(audio):
    global is_speaking
    if not is_speaking:
        try:
            is_speaking = True
            engine.say(audio)
            engine.runAndWait()
        except RuntimeError:
            pass
        finally:
            is_speaking = False

# Define the wish time function
def wish_time(name):
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 6:
        speak('Good night! Sleep tight.')
    elif 6 <= hour < 12:
        speak('Good morning!')
    elif 12 <= hour < 18:
        speak('Good afternoon!')
    else:
        speak('Good evening!')
    speak(f"{name}, how can I help you?")

# Function to perform tasks based on the command
def perform_task(query):
    query = query.lower()
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            st.write(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak(f"Multiple meanings found for '{query}'. Please be specific.")
        except wikipedia.exceptions.PageError:
            speak(f"'{query}' does not match any Wikipedia page.")
    elif 'play' in query:
        song = query.replace('play', "")
        speak("Playing " + song)
        kit.playonyt(song)
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")
    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")
    elif 'search' in query:
        s = query.replace('search', '')
        kit.search(s)
    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
    elif 'open code' in query:
        code_path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)
    elif 'joke' in query:
        speak(pyjokes.get_joke())
    elif "where is" in query:
        query = query.replace("where is", "")
        location = query
        speak(f"Locating {location}")
        webbrowser.open("https://www.google.nl/maps/place/" + location.replace(" ", "+"))
    elif 'exit' in query:
        speak("Exiting now.")

# Main function to run the Streamlit app
def main():
    st.title("Voice Assistant")

    # Input to get user's name
    name = st.text_input("Enter Your Name", "User")

    # Input for user to enter voice command
    command = st.text_input("Enter your command manually")

    # Button to perform task
    if st.button("Execute Command"):
        if command:
            perform_task(command)
        else:
            st.write("Please enter a command.")

if __name__ == "__main__":
    main()
