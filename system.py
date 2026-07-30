import ctypes
import os
import platform
import subprocess
import time
import psutil
import screen_brightness_control as sbc
from logger import log_command, log_error
from voice import speak

APP_MAP = {
    "notepad": "notepad.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "vs code": "code",
    "vscode": "code",
    "code": "code",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe"
}

PROCESS_MAP = {
    "notepad": ["notepad.exe"],
    "chrome": ["chrome.exe"],
    "google chrome": ["chrome.exe"],
    "calculator": ["calc.exe", "CalculatorApp.exe", "Calculator.exe"],
    "calc": ["calc.exe", "CalculatorApp.exe"],
    "vs code": ["Code.exe"],
    "vscode": ["Code.exe"],
    "code": ["Code.exe"],
    "paint": ["mspaint.exe"],
    "word": ["WINWORD.EXE"],
    "excel": ["EXCEL.EXE"],
    "cmd": ["cmd.exe"],
    "command prompt": ["cmd.exe"],
    "terminal": ["WindowsTerminal.exe", "wt.exe"],
    "explorer": ["explorer.exe"]
}

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def open_app(query):
    app_name = query.replace("open app", "").replace("open", "").strip()
    if not app_name:
        speak("Which application would you like me to open?")
        return

    target = APP_MAP.get(app_name, app_name)
    speak(f"Opening {app_name}")
    try:
        if target.endswith(".exe"):
            os.system(f"start {target}")
        else:
            subprocess.Popen(target, shell=True)
        log_command(query, f"Opened {app_name}")
    except Exception as e:
        log_error(f"Could not open {app_name}", e)
        speak(f"Failed to open {app_name}.")

def close_app(query):
    app_name = query.replace("close app", "").replace("close", "").strip()
    if not app_name:
        speak("Which application would you like me to close?")
        return

    targets = PROCESS_MAP.get(app_name, [f"{app_name}.exe"])
    closed_count = 0

    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in [t.lower() for t in targets]:
                proc.kill()
                closed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if closed_count > 0:
        msg = f"Closed {app_name} successfully."
    else:
        msg = f"{app_name} is not currently running."

    speak(msg)
    log_command(query, msg)

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            msg = "Battery information unavailable. System is running on AC power or desktop computer."
        else:
            percent = battery.percent
            plugged = "charging or plugged in" if battery.power_plugged else "running on battery"
            msg = f"Your battery is currently at {percent} percent and is {plugged}."
        speak(msg)
        log_command("battery status", msg)
    except Exception as e:
        log_error("Battery check error", e)
        speak("Unable to retrieve battery status.")

def get_system_status():
    try:
        speak("Checking system performance...")
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_available_gb = round(ram.available / (1024 ** 3), 2)
        ram_total_gb = round(ram.total / (1024 ** 3), 2)

        msg = f"CPU usage is at {cpu_usage} percent. RAM usage is at {ram_percent} percent, with {ram_available_gb} GB available out of {ram_total_gb} GB."
        speak(msg)
        log_command("system status", msg)
    except Exception as e:
        log_error("System status error", e)
        speak("Unable to retrieve CPU and RAM usage.")

def get_disk_usage():
    try:
        disk = psutil.disk_usage('/')
        total_gb = round(disk.total / (1024 ** 3), 2)
        used_gb = round(disk.used / (1024 ** 3), 2)
        free_gb = round(disk.free / (1024 ** 3), 2)
        percent = disk.percent

        msg = f"Disk usage: {percent} percent used. Total: {total_gb} GB, Used: {used_gb} GB, Free space: {free_gb} GB."
        speak(msg)
        print(f"Disk Usage: {msg}")
        log_command("disk usage", msg)
    except Exception as e:
        log_error("Disk usage error", e)
        speak("Unable to retrieve disk usage.")

def get_system_info():
    try:
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()
        arch = platform.architecture()[0]
        processor = platform.processor() or "x86/x64 Processor"
        cores = psutil.cpu_count(logical=True)
        ram_total = round(psutil.virtual_memory().total / (1024 ** 3), 2)

        msg = f"Operating System: {os_name} {os_release} ({arch}). Processor: {processor} with {cores} cores. Total Installed RAM: {ram_total} GB."
        speak(f"You are running {os_name} {os_release} with {ram_total} GB of RAM and a {cores} core processor.")
        print("\n--- System Information ---")
        print(f"OS: {os_name} {os_release} (Build {os_version})")
        print(f"Architecture: {arch}")
        print(f"Processor: {processor}")
        print(f"CPU Cores: {cores}")
        print(f"Total RAM: {ram_total} GB")
        log_command("system info", msg)
    except Exception as e:
        log_error("System info error", e)
        speak("Unable to retrieve system information.")

def control_volume(query):
    def press_vk(vk_code, count=1):
        for _ in range(count):
            ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
            time.sleep(0.05)

    if "up" in query or "increase" in query:
        press_vk(VK_VOLUME_UP, 5)
        msg = "Volume increased."
    elif "down" in query or "decrease" in query:
        press_vk(VK_VOLUME_DOWN, 5)
        msg = "Volume decreased."
    elif "mute" in query or "unmute" in query:
        press_vk(VK_VOLUME_MUTE, 1)
        msg = "Toggled volume mute."
    else:
        press_vk(VK_VOLUME_UP, 3)
        msg = "Adjusted volume."

    speak(msg)
    log_command(query, msg)

def control_brightness(query):
    try:
        current = sbc.get_brightness()
        current_val = current[0] if isinstance(current, list) and current else 50

        if "increase" in query or "up" in query or "more" in query:
            new_val = min(100, current_val + 20)
        elif "decrease" in query or "down" in query or "less" in query:
            new_val = max(0, current_val - 20)
        elif "max" in query or "full" in query:
            new_val = 100
        elif "min" in query or "low" in query:
            new_val = 10
        else:
            new_val = 50

        sbc.set_brightness(new_val)
        msg = f"Screen brightness set to {new_val} percent."
        speak(msg)
        log_command(query, msg)
    except Exception as e:
        log_error("Brightness control error", e)
        speak("Unable to adjust screen brightness.")

def lock_pc():
    speak("Locking your PC.")
    log_command("lock pc", "Locked PC workstation.")
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        log_error("Lock workstation error", e)

def sleep_pc():
    speak("Putting PC to sleep.")
    log_command("sleep pc", "Triggered PC sleep mode.")
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    except Exception as e:
        log_error("Sleep PC error", e)

def hibernate_pc():
    speak("Hibernating PC.")
    log_command("hibernate pc", "Triggered PC hibernation.")
    try:
        os.system("shutdown /h")
    except Exception as e:
        log_error("Hibernate PC error", e)

def empty_recycle_bin():
    try:
        res = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        msg = "Recycle bin emptied successfully."
        speak(msg)
        log_command("empty recycle bin", msg)
    except Exception as e:
        log_error("Empty recycle bin error", e)
        speak("Unable to empty recycle bin.")
