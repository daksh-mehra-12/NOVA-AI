import datetime
import os
import smtplib
import sys
import webbrowser
import pyjokes
import wikipedia
from dotenv import load_dotenv
import browser as browser_mod
import file_manager as file_mod
import logger as logger_mod
import multimedia as media_mod
import news as news_mod
import productivity as prod_mod
import system as system_mod
import utility as util_mod
import voice as voice_mod
import weather as weather_mod

from logger import log_command, log_error, log_info
from voice import speak, takeCommand

# Load environment variables
load_dotenv()


def wishMe():
    """Greet user based on current time of day."""
    hour = datetime.datetime.now().hour
    if 3 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    speak(f"{greeting} I am your AI Voice Assistant. How can I help you today?")
    log_info("Assistant started.")


def sendEmail(receiver, message):
    """Send email via SMTP."""
    sender = os.getenv("EMAIL_USER", "YOUR_EMAIL@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "YOUR_APP_PASSWORD")

    if sender == "YOUR_EMAIL@gmail.com" or password == "YOUR_APP_PASSWORD":
        speak("Email credentials are not configured. Please set EMAIL_USER and EMAIL_PASSWORD in your .env file.")
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        server.quit()
        msg = "Email sent successfully."
        speak(msg)
        log_command("send email", msg)
    except Exception as e:
        log_error("Email sending error", e)
        speak("Unable to send email. Check credentials and internet connection.")


def handle_query(query):
    """Dispatch user query to appropriate module handlers."""
    if not query:
        return True

    log_command(query, "Received query")

    # 🎵 1. YouTube Music Router (play music / any music related query)
    if "play music" in query or "play song" in query or (query.startswith("play ") and not any(k in query for k in ["video", "local", "note", "todo"])):
        browser_mod.play_youtube_music(query)

    # 2. Open / Close Apps & Folders
    elif "open downloads" in query:
        file_mod.open_special_folder("downloads")
    elif "open documents" in query:
        file_mod.open_special_folder("documents")
    elif "open desktop" in query:
        file_mod.open_special_folder("desktop")
    elif "open pictures" in query or "open photos" in query:
        file_mod.open_special_folder("pictures")
    elif query.startswith("open "):
        if "youtube" in query:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "google" in query:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif "github" in query:
            webbrowser.open("https://github.com")
            speak("Opening GitHub")
        elif "linkedin" in query:
            webbrowser.open("https://linkedin.com")
            speak("Opening LinkedIn")
        elif "gmail" in query or "mail" in query:
            browser_mod.open_gmail()
        elif "maps" in query:
            browser_mod.open_google_maps(query)
        elif "camera" in query:
            media_mod.open_camera()
        else:
            system_mod.open_app(query)

    elif query.startswith("close "):
        system_mod.close_app(query)

    # 3. File Operations
    elif "search file" in query or "find file" in query:
        file_mod.search_file(query)
    elif "create folder" in query or "new folder" in query or "make folder" in query:
        file_mod.create_folder(query)
    elif "delete file" in query or "remove file" in query:
        file_mod.delete_file(query)
    elif "rename file" in query or "rename" in query:
        file_mod.rename_file(query)
    elif "screenshot" in query:
        file_mod.take_screenshot()

    # 4. System Controls
    elif "lock pc" in query or "lock computer" in query or "lock workstation" in query:
        system_mod.lock_pc()
    elif "sleep pc" in query or "sleep computer" in query:
        system_mod.sleep_pc()
    elif "hibernate pc" in query or "hibernate" in query:
        system_mod.hibernate_pc()
    elif "empty recycle bin" in query or "clear recycle bin" in query:
        system_mod.empty_recycle_bin()
    elif "brightness" in query:
        system_mod.control_brightness(query)
    elif "disk usage" in query or "disk space" in query or "storage" in query:
        system_mod.get_disk_usage()
    elif "system info" in query or "system information" in query or "pc info" in query or "specs" in query:
        system_mod.get_system_info()
    elif "battery" in query:
        system_mod.get_battery_status()
    elif "cpu" in query or "ram" in query or "system status" in query or "performance" in query:
        system_mod.get_system_status()
    elif "volume" in query or "mute" in query or "unmute" in query:
        system_mod.control_volume(query)

    # 5. Multimedia
    elif "open camera" in query:
        media_mod.open_camera()
    elif "capture photo" in query or "take photo" in query or "click photo" in query or "take picture" in query:
        media_mod.capture_photo()
    elif "record audio" in query or "start recording" in query or "voice record" in query:
        media_mod.record_audio(30)
    elif "play local video" in query or "play video" in query:
        media_mod.play_local_video(query)
    elif "pause music" in query or "resume music" in query or "pause" in query or "play pause" in query:
        media_mod.media_play_pause()

    # 6. Browser Searches
    elif "search youtube" in query or "youtube search" in query:
        browser_mod.search_youtube(query)
    elif "search github" in query or "github search" in query:
        browser_mod.search_github(query)
    elif "search linkedin" in query or "linkedin search" in query:
        browser_mod.search_linkedin(query)
    elif "search stackoverflow" in query or "search stack overflow" in query:
        browser_mod.search_stackoverflow(query)

    # 7. Productivity
    elif "add todo" in query or "new todo" in query or "add task" in query:
        prod_mod.add_todo(query)
    elif "read todo" in query or "show todo" in query or "view todo" in query or "todo list" in query:
        prod_mod.read_todos()
    elif "delete todo" in query or "remove todo" in query or "clear todo" in query:
        prod_mod.delete_todo(query)
    elif "daily quote" in query or "quote of the day" in query or "quote" in query:
        prod_mod.get_daily_quote()
    elif "random fact" in query or "tell me a fact" in query or "fact" in query:
        prod_mod.get_random_fact()
    elif "pomodoro" in query or "focus timer" in query:
        prod_mod.start_pomodoro_timer()
    elif "take note" in query or "add note" in query or "write note" in query:
        prod_mod.take_note(query)
    elif "read note" in query or "show note" in query or "view note" in query:
        prod_mod.read_notes()
    elif "clear note" in query:
        prod_mod.clear_notes()
    elif "remind" in query or "reminder" in query:
        prod_mod.set_reminder(query)

    # 8. Utility & Conversions
    elif "clipboard read" in query or "read clipboard" in query or "what is on clipboard" in query or "paste" in query:
        util_mod.clipboard_read()
    elif "clipboard copy" in query or "copy to clipboard" in query:
        util_mod.clipboard_copy(query)
    elif "qr code" in query or "generate qr" in query or "make qr" in query:
        util_mod.generate_qr_code(query)
    elif "password generator" in query or "generate password" in query or "create password" in query:
        util_mod.generate_password(query)
    elif "currency" in query or "convert" in query and any(c in query for c in ["usd", "inr", "eur", "gbp"]):
        util_mod.convert_currency(query)
    elif "convert" in query and any(u in query for u in ["km", "mile", "kg", "lb", "celsius", "fahrenheit"]):
        util_mod.convert_units(query)
    elif "calculate" in query or "math" in query:
        util_mod.calculate(query)

    # 9. Weather, News & Internet Check
    elif "weather" in query:
        if "weather in" in query:
            city = query.replace("weather in", "").strip()
        else:
            speak("Which city's weather would you like to check?")
            city = takeCommand()

        if city:
            weather_mod.getWeather(city)
    elif "news" in query or "headline" in query:
        news_mod.getNews()
    elif "internet" in query or "online" in query or "ping" in query:
        try:
            import requests
            res = requests.get("https://www.google.com", timeout=3)
            if res.status_code == 200:
                speak("Your internet connection is active and stable.")
            else:
                speak("Internet connection check returned unexpected response.")
        except Exception:
            speak("No internet connection detected.")

    # 10. Wikipedia & Google Search
    elif "wikipedia" in query:
        search_term = query.replace("wikipedia", "").strip()
        if not search_term:
            speak("What should I search on Wikipedia?")
            search_term = takeCommand()

        if search_term:
            try:
                speak("Searching Wikipedia...")
                result = wikipedia.summary(search_term, sentences=2)
                print("\nWikipedia Result:\n", result)
                speak(result)
                log_command(query, result)
            except Exception as e:
                log_error("Wikipedia error", e)
                speak("No result found on Wikipedia.")

    elif "search" in query:
        term = query.replace("search", "").strip()
        if term:
            speak(f"Searching for {term}")
            webbrowser.open(f"https://www.google.com/search?q={term}")

    # 11. Joke, Time, Date
    elif "joke" in query:
        joke = pyjokes.get_joke()
        print("\nJoke:", joke)
        speak(joke)
        log_command(query, joke)
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        today_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today_date}")
    elif "log" in query or "history" in query:
        logs = logger_mod.get_command_logs(10)
        if logs:
            speak("Displaying latest command logs.")
            print("\n--- Recent Command Logs ---")
            for line in logs:
                print(line)
        else:
            speak("No command logs available.")

    # 12. Email & Exit
    elif "send email" in query:
        speak("Who is the recipient email address?")
        receiver = input("Enter receiver email address: ").strip()
        if receiver:
            speak("What should I send?")
            content = takeCommand()
            if content:
                sendEmail(receiver, content)
    elif "exit" in query or "quit" in query or "bye" in query:
        speak("Goodbye! Have a great day.")
        return False
    else:
        speak("I am sorry, I didn't recognize that command. Could you please rephrase?")

    return True


if __name__ == "__main__":
    try:
        wishMe()
        running = True
        while running:
            query = takeCommand()
            if query:
                running = handle_query(query)

    except KeyboardInterrupt:
        print("\nExiting Assistant...")
        speak("Goodbye!")