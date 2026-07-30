import threading
import pyttsx3
import speech_recognition as sr
from logger import log_command, log_error, log_info

try:
    import pythoncom
except ImportError:
    pythoncom = None

try:
    import win32com.client
except ImportError:
    win32com = None

_tts_lock = threading.Lock()

def speak(audio):
    if not audio:
        return

    print(f"\nAssistant: {audio}")

    with _tts_lock:
        if pythoncom:
            try:
                pythoncom.CoInitialize()
            except Exception:
                pass

        spoken = False

        try:
            try:
                engine = pyttsx3.init("sapi5")
            except Exception:
                engine = pyttsx3.init()

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)
            engine.setProperty("rate", 175)

            engine.say(audio)
            engine.runAndWait()
            try:
                engine.stop()
            except Exception:
                pass
            del engine
            spoken = True
        except Exception as e:
            log_error("pyttsx3 speech playback error", e)

        if not spoken and win32com:
            try:
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(audio)
                spoken = True
            except Exception as ex:
                log_error("SAPI.SpVoice fallback error", ex)

def takeCommand():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query.lower().strip()

    except sr.WaitTimeoutError:
        print("Listening timed out. No speech detected.")
        return ""
    except sr.UnknownValueError:
        speak("Please say that again.")
        return ""
    except sr.RequestError as e:
        speak("Speech recognition service unavailable.")
        log_error("Speech Recognition API error", e)
        return ""
    except Exception as e:
        print(f"Microphone notice ({e}). Switching to text input mode...")
        try:
            query = input("You (Type command or press Enter to retry): ").strip()
            return query.lower()
        except (KeyboardInterrupt, EOFError):
            return "exit"
