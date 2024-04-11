import streamlit as st
import sounddevice as sd 
import pyttsx3
import webbrowser
import os
import streamlit.components.v1 as component
import speech_recognition as sr
import scipy.io.wavfile as wavfile
import streamlit_webrtc as stwt
import pyaudio

from pathlib import Path

recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

speaking = False

def myai(text):
    global speaking
    message = f"<div style='text-align: left;'>Assistant: {text}</div>"
    st.markdown(message, unsafe_allow_html=True)
    
    #st.text(f"Assistant: {text}")
    
    if not speaking:
        speaking = True
        engine.say(text)
        engine.runAndWait()
        speaking = False

def introduce_assistant():
    text = "Hello! I am your virtual assistant."
    myai(text)

def prompt_user():  
    text = "How may I help you?\nYou can say:\n- 'Shop'\n- 'About Us'\n-  'Contact us' to get in touch\n- 'Order' "
    myai(text)

def cmd():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    #Adjust for ambient noise
    #with sr.Microphone() as source:
       # recognizer.adjust_for_ambient_noise(source, duration=0.5)
    prompt_user()
    text = "Clearing background noises... Please wait"
    myai(text)

    # Prompt the user for input
    text = "Your choice..."
    myai(text)
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    try:
        user_input = recognize_audio(recording, fs)
        print('User input:', user_input)
        message = f"<div style='text-align: right;'>{user_input} :User</div>"
        st.markdown(message, unsafe_allow_html=True)
        process_input(user_input)

    except Exception as ex:
        print("An error occurred:", ex)
        text = "An error occurred. Please try again."
        myai(text)

def recognize_audio(recording, fs):
    recognizer = sr.Recognizer()

    try:
        # Save the recorded audio to a WAV file
        wavfile.write("recorded_audio.wav", fs, recording)

        # Load the saved audio file for speech recognition
        with sr.AudioFile("recorded_audio.wav") as source:
            audio_data = recognizer.record(source)
        
        # Use the recognizer to recognize speech from the audio data
        recognized_text = recognizer.recognize_google(audio_data)
        return recognized_text
    except sr.UnknownValueError:
        # Handle cases where speech recognition cannot understand the audio
        return "Unknown speech"
    except sr.RequestError as e:
        # Handle errors that occur when making the API request
        return f"Could not request results from Google Speech Recognition service; {e}"

def process_input(user_input):
    if 'shop' in user_input:
        shop()

    elif 'about us' in user_input:
        about_us()

    elif 'contact' in user_input:
        contact_us()

    else:
        assistant_response = "Sorry, I didn't understand. Could you please repeat?"
        myai(assistant_response)
    
    # Update chat display with user input
    
   

def shop():
    text = "You can let me know about your product or can go Manually to shop; to shop manually kindly say manually"
    myai(text)
    # Add your shop functionality here
    # For demonstration purposes, let's open a web page
    webbrowser.open('Shop.html')

def about_us():
    text = "Sure"
    myai(text)
    webbrowser.open('AboutUs.html')

def contact_us():
    text = "For any queries, please send an email to aditirg2@gmail.com."
    myai(text)

def main():
   
    st.title("Virtual Assistant")

    introduce_assistant()

    #user_input = st.text_input("Type your query here:")
    #if st.button("Send"):
    #    process_input(user_input)

    while True:
        #prompt_user()
        cmd()

if __name__ == '__main__':
    main()
