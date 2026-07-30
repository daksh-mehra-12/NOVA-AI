import urllib.parse
import webbrowser
from logger import log_command, log_error
from voice import speak

def search_youtube(query):
    term = query.replace("search youtube for", "").replace("search youtube", "").replace("youtube search", "").strip()
    if not term:
        speak("What would you like me to search on YouTube?")
        return

    speak(f"Searching YouTube for {term}")
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(term)}"
    webbrowser.open(url)
    log_command(query, f"Searched YouTube for {term}")

def play_youtube_music(query):
    song_name = query.replace("play music", "").replace("play song", "").replace("music", "").replace("play", "").strip()
    if not song_name:
        song_name = "trending songs"

    speak(f"Playing {song_name} on YouTube.")
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song_name + ' song')}"
    webbrowser.open(url)
    log_command(query, f"Played {song_name} on YouTube.")

def search_github(query):
    term = query.replace("search github for", "").replace("search github", "").replace("github search", "").strip()
    if not term:
        speak("What would you like me to search on GitHub?")
        return

    speak(f"Searching GitHub for {term}")
    url = f"https://github.com/search?q={urllib.parse.quote(term)}"
    webbrowser.open(url)
    log_command(query, f"Searched GitHub for {term}")

def search_linkedin(query):
    term = query.replace("search linkedin for", "").replace("search linkedin", "").replace("linkedin search", "").strip()
    if not term:
        speak("What would you like me to search on LinkedIn?")
        return

    speak(f"Searching LinkedIn for {term}")
    url = f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(term)}"
    webbrowser.open(url)
    log_command(query, f"Searched LinkedIn for {term}")

def search_stackoverflow(query):
    term = query.replace("search stack overflow for", "").replace("search stackoverflow for", "").replace("search stack overflow", "").replace("search stackoverflow", "").strip()
    if not term:
        speak("What code query would you like to search on Stack Overflow?")
        return

    speak(f"Searching Stack Overflow for {term}")
    url = f"https://stackoverflow.com/search?q={urllib.parse.quote(term)}"
    webbrowser.open(url)
    log_command(query, f"Searched Stack Overflow for {term}")

def open_gmail():
    speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com")
    log_command("open gmail", "Opened Gmail inbox.")

def open_google_maps(query):
    location = query.replace("open google maps", "").replace("google maps", "").replace("maps", "").strip()
    if location and location not in ["open", "search"]:
        speak(f"Opening Google Maps for {location}")
        url = f"https://www.google.com/maps/search/{urllib.parse.quote(location)}"
    else:
        speak("Opening Google Maps.")
        url = "https://maps.google.com"

    webbrowser.open(url)
    log_command(query, f"Opened Google Maps: {url}")
