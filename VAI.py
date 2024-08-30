import os
import subprocess
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Speak text using pyttsx3
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Spotify credentials
SPOTIPY_CLIENT_ID = '1DL4pRCKKmg238fsCU6i7ZYEStP9fL9o4q'
SPOTIPY_CLIENT_SECRET = '0630b553c4b147219fddc311211b4bc5'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-library-read user-read-playback-state user-modify-playback-state'

# Spotify authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# YouTube API key
YOUTUBE_API_KEY = 'AIzaSyB7Lu-f7ch9BhvHoreM8Jd3okQbFfs2bFQ'

# Function to search and play the first video on YouTube
def search_and_play_youtube(query):
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={YOUTUBE_API_KEY}'
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        if 'items' in results and len(results['items']) > 0:
            video_id = results['items'][0]['id']['videoId']
            speak_text("Ok sir, opening the first result on YouTube.")
            webbrowser.open(f'https://www.youtube.com/watch?v={video_id}')
        else:
            speak_text("No results found on YouTube.")
    else:
        speak_text("Error occurred while searching YouTube.")

# Function to play a song on Spotify
def play_song_on_spotify(song_name):
    result = sp.search(q=song_name, type='track', limit=1)
    if result['tracks']['items']:
        track_uri = result['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        speak_text(f"Playing {song_name} on Spotify.")
    else:
        speak_text("Song not found on Spotify.")

# Function to process voice commands
def process_command(command):
    if 'search up' in command:
        query = command.replace('search up', '').strip()
        search_and_play_youtube(query)
    elif 'play' in command:
        song_name = command.replace('play', '').strip()
        play_song_on_spotify(song_name)
    elif 'clip' in command:
        subprocess.run(['powershell', '-Command', 'Start-Process', 'ms-gamebar:', '-ArgumentList', '/record'])
        speak_text("Recording started.")
    else:
        speak_text("Command not recognized.")

# Main function
def main():
    speak_text("Hello, I am Jarvis. Please say something with 'jarvis' at the start to begin.")
    
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                command = command.lower()
                if 'jarvis' in command:
                    command = command.replace('jarvis', '').strip()
                    process_command(command)
                else:
                    speak_text("Please start your command with 'jarvis'.")
            except sr.UnknownValueError:
                speak_text("Sorry, I did not understand that.")
            except sr.RequestError:
                speak_text("Sorry, there was an error with the request.")
            except Exception as e:
                speak_text(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
