import datetime
import logging
import os

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

APP_LOG_FILE = os.path.join(LOG_DIR, "assistant.log")
COMMAND_LOG_FILE = os.path.join(LOG_DIR, "command_logs.txt")

logger = logging.getLogger("VoiceAssistant")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(APP_LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

def log_info(message):
    logger.info(message)

def log_error(message, exc=None):
    if exc:
        logger.error(f"{message} - Exception: {exc}")
    else:
        logger.error(message)

def log_command(query, response):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] User: {query} | Assistant: {response}\n"
        with open(COMMAND_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        log_info(f"Command executed: {query} -> {response}")
    except Exception as e:
        log_error("Failed to write to command log", e)

def get_command_logs(limit=10):
    if not os.path.exists(COMMAND_LOG_FILE) or os.path.getsize(COMMAND_LOG_FILE) == 0:
        return []

    try:
        with open(COMMAND_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-limit:]]
    except Exception as e:
        log_error("Failed to read command logs", e)
        return []
