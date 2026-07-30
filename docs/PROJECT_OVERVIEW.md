# NOVA AI - Technical Overview & Architecture Documentation

## 1. Project Overview

**NOVA AI** (Next-generation Operations & Voice Assistant) is an open-source, modular, asynchronous desktop voice assistant built natively in Python. It bridges natural human voice commands with local operating system controls, productivity workflows, device controls, web services, and multimedia automation.

### Core Value Proposition
- **100% Privacy & Local Execution Control**: System commands, file management, local note-taking, and hardware triggers operate locally without sending OS data to third-party servers.
- **Modular Micro-Architecture**: Designed with decoupled, single-responsibility Python modules rather than a monolithic script.
- **Resilient Fallback Design**: Dual-tier fallback mechanisms for Speech-to-Text, Text-to-Speech, Weather APIs, and News feeds ensure high uptime even during network or API key failures.

---

## 2. System Architecture

```
                                  +-----------------------+
                                  |    User Audio Input   |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |    voice.py (STT)     |
                                  |  (Google Speech API / |
                                  |   Microphone Fallback)|
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |   assistant.py (Core) |
                                  | (Command Dispatcher & |
                                  |   Pattern Matching)   |
                                  +-----------+-----------+
                                              |
       +------------------+-------------------+-------------------+------------------+
       |                  |                   |                   |                  |
       v                  v                   v                   v                  v
+--------------+   +--------------+    +--------------+    +--------------+   +--------------+
|  system.py   |   | file_manager |    | multimedia.py|    |productivity.py|   | utility.py   |
| (OS/App/Sys) |   | (Files/Scrn) |    | (Cam/Audio)  |    | (Notes/Todos)|   | (QR/Math/Pass|
+--------------+   +--------------+    +--------------+    +--------------+   +--------------+
       |                  |                   |                   |                  |
       +------------------+-------------------+-------------------+------------------+
                                              |
                                              v
                                  +-----------------------+
                                  |     voice.py (TTS)    |
                                  | (pyttsx3 / SAPI5 /    |
                                  |   win32com Fallback)  |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |       logger.py       |
                                  | (File Logging & Audit)|
                                  +-----------------------+
```

---

## 3. How Each Module Works

### `assistant.py` (Core Dispatcher & Controller)
- **Role**: Serves as the central orchestration point.
- **Functionality**: Loads environment variables, initiates greeting routines (`wishMe`), runs the core loop polling `voice.takeCommand()`, and routes parsed intent tokens to specialized handler modules via `handle_query()`.

### `voice.py` (Speech Recognition & TTS Engine)
- **Role**: Handles speech input/output.
- **Functionality**:
  - **Speech-to-Text**: Uses `speech_recognition.Recognizer` configured for low latency ambient noise adjustments (`adjust_for_ambient_noise`). Falls back to interactive CLI prompt if microphone input times out or fails.
  - **Text-to-Speech**: Uses `pyttsx3` with Windows SAPI5 driver. Utilizes thread locking (`_tts_lock`) and `pythoncom.CoInitialize()` to ensure safe multi-threaded execution. Falls back to `win32com.client.Dispatch("SAPI.SpVoice")` if `pyttsx3` encounters engine initialization issues.

### `system.py` (OS & Hardware Controller)
- **Role**: Manages native Windows system actions.
- **Functionality**: Performs application launching/killing (`psutil`), battery monitoring, CPU/RAM performance analysis, disk usage statistics, win32 API volume controls (`ctypes.windll.user32.keybd_event`), screen brightness regulation (`screen_brightness_control`), workstation locking (`LockWorkStation`), sleep, hibernation, and recycle bin emptying (`SHEmptyRecycleBinW`).

### `file_manager.py` (File System & Screenshot Engine)
- **Role**: Handles directory navigation, file discovery, and screenshot captures.
- **Functionality**: Opens user profile special folders (Downloads, Documents, Desktop, Pictures), performs recursive directory file searches across user roots, handles file creation/deletion with confirmation prompts, renames files, and captures full-screen screenshots using `pyautogui` / `PIL.ImageGrab`.

### `multimedia.py` (Media Capture & Playback)
- **Role**: Interfaces with hardware camera and microphone for media operations.
- **Functionality**: Triggers Windows Camera app or captures webcam snapshots directly via `OpenCV (cv2)`, records multi-channel WAV audio streams via `sounddevice` and `wave`, launches local video files in native players, and sends hardware media play/pause key signals.

### `productivity.py` (Task, Note & Focus Management)
- **Role**: Provides personal productivity utilities.
- **Functionality**: Manages JSON-persisted todo lists (`todo.json`), timestamped notes (`notes.txt`), triggers non-blocking background Pomodoro timers and custom reminders via `threading.Timer`, and fetches daily motivational quotes (`ZenQuotes`) and random trivia (`UselessFacts`) with offline fallback arrays.

### `utility.py` (Calculations, Conversions & Tools)
- **Role**: Provides quick utility functions.
- **Functionality**: Manages system clipboard reading/writing (`pyperclip`), generates PNG QR codes (`qrcode`), generates cryptographically safe random passwords, performs real-time currency conversions (`open.er-api.com`), unit conversions (length, weight, temperature), and evaluates mathematical expressions using a isolated evaluation context.

### `weather.py` (Weather Intelligence)
- **Role**: Fetches current weather reports.
- **Functionality**: Primary query sent to `OpenWeatherMap API`. If unconfigured or failing, automatically fails over to `wttr.in` JSON endpoint, parsing temperature, description, humidity, and wind speed.

### `news.py` (News Headlines Aggregator)
- **Role**: Retrieves top news headlines.
- **Functionality**: Tries `NewsData.io` or `NewsAPI.org` primary APIs. On key absence or API error, gracefully fails over to `Google News RSS` XML parsing.

### `browser.py` (Web Search & Navigation)
- **Role**: Automates web browser navigation.
- **Functionality**: Formats and launches search queries on YouTube, YouTube Music, Google, GitHub, LinkedIn, Stack Overflow, Google Maps, and Gmail.

### `logger.py` (Audit Trail & Error Logging)
- **Role**: Provides application logging and user command history auditing.
- **Functionality**: Uses Python's standard `logging` library for structured application logs (`logs/assistant.log`) and append-only command execution history (`logs/command_logs.txt`).

---

## 4. Design Decisions & Architectural Rationale

1. **Decoupled Single-Responsibility Architecture**:
   - *Decision*: Avoided placing all logic inside `assistant.py`.
   - *Rationale*: Isolating domain logic into distinct modules (e.g., `system.py`, `productivity.py`) makes the codebase maintainable, testable, and allows independent feature development without side effects.

2. **Multithreaded Non-Blocking Timers & TTS**:
   - *Decision*: Used `threading.Timer` for Pomodoro/reminders and `threading.Lock()` with COM initialization for TTS.
   - *Rationale*: Voice assistants must remain responsive. Blocking execution during a 25-minute Pomodoro timer or during spoken audio output would freeze user input.

3. **Dual-Tier Resilient Fallback Strategy**:
   - *Decision*: Built local fallback routines for Weather (`wttr.in`), News (`Google News RSS`), Speech Recognition (`cli input`), and TTS (`win32com SAPI`).
   - *Rationale*: Third-party APIs experience rate limits, downtime, or key invalidation. A robust voice assistant should continue functioning gracefully without crashing.

4. **Zero-Database Lightweight Persistence**:
   - *Decision*: Utilized JSON (`todo.json`), plain text (`notes.txt`), and structured logs (`command_logs.txt`).
   - *Rationale*: Eliminates heavy external database dependencies (e.g., PostgreSQL, SQLite compilation overhead) while preserving zero-configuration setup for end users.
