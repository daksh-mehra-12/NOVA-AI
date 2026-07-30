import ctypes
import datetime
import os
import subprocess
import time
import wave
import cv2
import sounddevice as sd
from logger import log_command, log_error
from voice import speak

PHOTOS_DIR = os.path.join(os.getcwd(), "Photos")
RECORDINGS_DIR = os.path.join(os.getcwd(), "Recordings")
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(RECORDINGS_DIR, exist_ok=True)

VK_MEDIA_PLAY_PAUSE = 0xCD

def open_camera():
    speak("Opening camera.")
    log_command("open camera", "Opened Windows Camera app.")
    try:
        os.system("start microsoft.windows.camera:")
    except Exception as e:
        log_error("Open camera error", e)
        speak("Could not open camera app.")

def capture_photo():
    speak("Capturing photo in 3 seconds. Please look at the camera.")
    print("Preparing webcam...")
    time.sleep(2)

    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            speak("Webcam is not accessible.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(PHOTOS_DIR, f"photo_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            msg = f"Photo captured and saved as photo_{timestamp}.jpg in Photos directory."
            speak("Photo captured successfully.")
            print(f"Saved photo: {filename}")
            log_command("capture photo", msg)
        else:
            speak("Failed to capture image from camera.")
    except Exception as e:
        log_error("Capture photo error", e)
        speak("Unable to capture photo.")

def record_audio(duration=30):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.wav")
    samplerate = 44100

    speak(f"Recording audio for {duration} seconds. Please speak now.")
    print(f"\nRecording audio ({duration} seconds)...")

    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
        sd.wait()

        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(recording.tobytes())

        msg = f"Audio recording saved as recording_{timestamp}.wav in Recordings folder."
        speak("Audio recording completed successfully.")
        print(f"Saved audio: {filepath}")
        log_command("record audio", msg)
    except Exception as e:
        log_error("Audio recording error", e)
        speak("Failed to record audio.")

def play_local_video(query):
    user_home = os.path.expanduser("~")
    search_dirs = [
        os.path.join(user_home, "Videos"),
        os.path.join(user_home, "Downloads"),
        os.getcwd()
    ]

    found_video = None
    for d in search_dirs:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".wmv")):
                    found_video = os.path.join(d, f)
                    break
        if found_video:
            break

    if found_video:
        speak(f"Playing video: {os.path.basename(found_video)}")
        try:
            os.startfile(found_video)
        except Exception:
            subprocess.Popen([found_video], shell=True)
        log_command("play video", f"Playing local video {found_video}")
    else:
        speak("No video file found in Videos or Downloads folder.")

def media_play_pause():
    try:
        ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 2, 0)
        msg = "Toggled media play/pause."
        speak(msg)
        log_command("play pause music", msg)
    except Exception as e:
        log_error("Media play/pause error", e)
