import datetime
import json
import os
import random
import re
import threading
import time
import requests
from logger import log_command, log_error
from voice import speak

NOTES_FILE = os.path.join(os.getcwd(), "notes.txt")
TODO_FILE = os.path.join(os.getcwd(), "todo.json")

FALLBACK_QUOTES = [
    "The secret of getting ahead is getting started. - Mark Twain",
    "It always seems impossible until it's done. - Nelson Mandela",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Quality is not an act, it is a habit. - Aristotle",
    "Believe you can and you're halfway there. - Theodore Roosevelt"
]

FALLBACK_FACTS = [
    "Honey never spoils. Trace amounts of edible honey have been found in ancient Egyptian tombs.",
    "Bananas are naturally slightly radioactive because of their potassium content.",
    "A day on Venus is longer than a year on Venus.",
    "Octopuses have three hearts and blue blood.",
    "Wombat poop is cube-shaped to prevent it from rolling away."
]

def _load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_todos(todos):
    try:
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, indent=2)
    except Exception as e:
        log_error("Failed to save todo list", e)

def add_todo(query):
    task = query.replace("add todo", "").replace("todo add", "").replace("add to do", "").replace("todo", "").strip()
    if not task:
        speak("What task would you like to add to your todo list?")
        return

    todos = _load_todos()
    todos.append({"task": task, "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    _save_todos(todos)

    msg = f"Added '{task}' to your todo list."
    speak(msg)
    log_command(query, msg)

def read_todos():
    todos = _load_todos()
    if not todos:
        speak("Your todo list is currently empty.")
        return

    speak(f"You have {len(todos)} pending task(s) in your todo list.")
    print("\n--- Todo List ---")
    for idx, item in enumerate(todos, 1):
        task_str = f"{idx}. {item['task']} (Added: {item['created_at']})"
        print(task_str)
        speak(f"Task {idx}: {item['task']}")

def delete_todo(query):
    todos = _load_todos()
    if not todos:
        speak("Your todo list is currently empty.")
        return

    item_to_remove = query.replace("delete todo", "").replace("remove todo", "").replace("delete to do", "").strip()
    if not item_to_remove:
        speak("Which todo item number would you like to remove?")
        return

    new_todos = []
    removed = False

    if item_to_remove.isdigit():
        idx = int(item_to_remove) - 1
        if 0 <= idx < len(todos):
            removed_item = todos.pop(idx)
            new_todos = todos
            removed = True
            msg = f"Removed task '{removed_item['task']}' from your todo list."
    else:
        for item in todos:
            if item_to_remove.lower() in item['task'].lower():
                removed = True
                msg = f"Removed task '{item['task']}' from your todo list."
            else:
                new_todos.append(item)

    if removed:
        _save_todos(new_todos)
        speak(msg)
        log_command(query, msg)
    else:
        speak(f"Could not find todo item matching '{item_to_remove}'.")

def get_daily_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=3)
        if res.status_code == 200:
            data = res.json()
            quote = f"{data[0]['q']} - {data[0]['a']}"
            speak("Here is your daily inspirational quote.")
            print(f"\nQuote: {quote}")
            speak(quote)
            log_command("daily quote", quote)
            return
    except Exception as e:
        log_error("Quote API error", e)

    quote = random.choice(FALLBACK_QUOTES)
    speak("Here is your quote of the day.")
    print(f"\nQuote: {quote}")
    speak(quote)
    log_command("daily quote", quote)

def get_random_fact():
    try:
        res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=3)
        if res.status_code == 200:
            data = res.json()
            fact = data["text"]
            speak("Here is an interesting random fact.")
            print(f"\nFact: {fact}")
            speak(fact)
            log_command("random fact", fact)
            return
    except Exception as e:
        log_error("Fact API error", e)

    fact = random.choice(FALLBACK_FACTS)
    speak("Here is a random fact.")
    print(f"\nFact: {fact}")
    speak(fact)
    log_command("random fact", fact)

def start_pomodoro_timer():
    duration_minutes = 25
    speak(f"Starting a {duration_minutes}-minute Pomodoro focus timer. Happy working!")
    print(f"\n[POMODORO] Focus timer started for {duration_minutes} minutes.")

    def _fire_pomodoro():
        print("\n[POMODORO COMPLETE] 25 minutes are up! Take a 5-minute break.")
        speak("Pomodoro focus timer completed! Great job. Time to take a 5 minute break!")

    timer = threading.Timer(duration_minutes * 60, _fire_pomodoro)
    timer.start()
    log_command("pomodoro timer", f"Started {duration_minutes}-minute Pomodoro timer.")

def _fire_reminder(task):
    print(f"\n[REMINDER ALERT] {task}")
    speak(f"Reminder Alert! {task}")

def set_reminder(query):
    match = re.search(r"remind me (?:to )?(.*?) in (\d+)\s*(second|seconds|minute|minutes|hour|hours)", query)
    if not match:
        speak("Please specify reminder format as: remind me to [task] in [number] seconds or minutes.")
        return

    task = match.group(1).strip()
    amount = int(match.group(2))
    unit = match.group(3)

    seconds = amount
    if "minute" in unit:
        seconds = amount * 60
    elif "hour" in unit:
        seconds = amount * 3600

    timer = threading.Timer(seconds, _fire_reminder, args=[task])
    timer.start()

    msg = f"Reminder set for '{task}' in {amount} {unit}."
    speak(msg)
    log_command(query, msg)

def take_note(query):
    note_content = query.replace("take note", "").replace("add note", "").replace("write note", "").strip()
    if not note_content:
        speak("What note would you like me to take?")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {note_content}\n")

    msg = f"Note saved: '{note_content}'"
    speak("Note saved successfully.")
    log_command(query, msg)

def read_notes():
    if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE) == 0:
        speak("You have no saved notes.")
        return

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = f.readlines()

    speak(f"You have {len(notes)} saved notes.")
    for note in notes[-5:]:
        print("Note:", note.strip())
        speak(note.strip())

def clear_notes():
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write("")
    speak("All notes have been cleared.")
    log_command("clear notes", "Cleared all notes.")
