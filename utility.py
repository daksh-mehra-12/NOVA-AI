import datetime
import os
import random
import re
import string
import pyautogui
import pyperclip
import qrcode
import requests
from logger import log_command, log_error
from voice import speak

QR_DIR = os.path.join(os.getcwd(), "QRCodes")
os.makedirs(QR_DIR, exist_ok=True)

def clipboard_copy(query):
    text_to_copy = query.replace("copy to clipboard", "").replace("copy clipboard", "").replace("copy", "").strip()
    if not text_to_copy:
        speak("What text would you like me to copy to the clipboard?")
        return

    pyperclip.copy(text_to_copy)
    msg = f"Copied '{text_to_copy}' to your clipboard."
    speak("Text copied to clipboard.")
    print(f"Clipboard: {text_to_copy}")
    log_command(query, msg)

def clipboard_read():
    try:
        content = pyperclip.paste()
        if content and content.strip():
            msg = f"Clipboard content: {content.strip()}"
            speak("Here is what is currently on your clipboard.")
            print(f"\n--- Clipboard Content ---\n{content}\n")
            speak(content[:200])
            log_command("read clipboard", msg)
        else:
            speak("Your clipboard is currently empty.")
    except Exception as e:
        log_error("Clipboard read error", e)
        speak("Unable to read clipboard content.")

def generate_qr_code(query):
    data = query.replace("generate qr code for", "").replace("generate qr code", "").replace("make qr code", "").replace("qr code", "").strip()
    if not data:
        speak("What text or URL should I generate a QR code for?")
        return

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(QR_DIR, f"qr_{timestamp}.png")
        img.save(filename)

        msg = f"QR code generated for '{data}' and saved as qr_{timestamp}.png in QRCodes directory."
        speak("QR code generated successfully.")
        print(f"Saved QR Code: {filename}")
        os.startfile(filename)
        log_command(query, msg)
    except Exception as e:
        log_error(f"QR code generation error for {data}", e)
        speak("Failed to generate QR code.")

def generate_password(query):
    length = 14
    match = re.search(r"(\d+)", query)
    if match:
        length = max(6, min(64, int(match.group(1))))

    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = "".join(random.choice(chars) for _ in range(length))

    pyperclip.copy(password)
    msg = f"Generated {length}-character secure password and copied it to clipboard."
    speak(f"Generated a {length}-character secure password and copied it to your clipboard.")
    print(f"\nGenerated Password: {password} (Copied to Clipboard!)")
    log_command(query, msg)

def convert_currency(query):
    match = re.search(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]{3})\s*(?:to|in)\s*([a-zA-Z]{3})", query)
    if not match:
        speak("Please specify currency conversion as: convert 100 USD to INR or 50 EUR to USD.")
        return

    amount = float(match.group(1))
    from_curr = match.group(2).upper()
    to_curr = match.group(3).upper()

    try:
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            rates = data.get("rates", {})
            if to_curr in rates:
                converted = round(amount * rates[to_curr], 2)
                msg = f"{amount} {from_curr} is equal to {converted} {to_curr}."
                speak(msg)
                print(f"Currency: {msg}")
                log_command(query, msg)
                return
    except Exception as e:
        log_error("Currency converter API error", e)

    speak(f"Unable to convert {from_curr} to {to_curr}.")

def convert_units(query):
    km_to_mile = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kilometer|kilometers)\s*(?:to|in)\s*(?:mile|miles)", query)
    if km_to_mile:
        val = float(km_to_mile.group(1))
        res = round(val * 0.621371, 2)
        msg = f"{val} kilometers is equal to {res} miles."
        speak(msg)
        log_command(query, msg)
        return

    mile_to_km = re.search(r"(\d+(?:\.\d+)?)\s*(?:mile|miles)\s*(?:to|in)\s*(?:km|kilometer|kilometers)", query)
    if mile_to_km:
        val = float(mile_to_km.group(1))
        res = round(val / 0.621371, 2)
        msg = f"{val} miles is equal to {res} kilometers."
        speak(msg)
        log_command(query, msg)
        return

    kg_to_lb = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilogram|kilograms)\s*(?:to|in)\s*(?:lb|lbs|pound|pounds)", query)
    if kg_to_lb:
        val = float(kg_to_lb.group(1))
        res = round(val * 2.20462, 2)
        msg = f"{val} kilograms is equal to {res} pounds."
        speak(msg)
        log_command(query, msg)
        return

    lb_to_kg = re.search(r"(\d+(?:\.\d+)?)\s*(?:lb|lbs|pound|pounds)\s*(?:to|in)\s*(?:kg|kilogram|kilograms)", query)
    if lb_to_kg:
        val = float(lb_to_kg.group(1))
        res = round(val / 2.20462, 2)
        msg = f"{val} pounds is equal to {res} kilograms."
        speak(msg)
        log_command(query, msg)
        return

    c_to_f = re.search(r"(\d+(?:\.\d+)?)\s*(?:celsius|c)\s*(?:to|in)\s*(?:fahrenheit|f)", query)
    if c_to_f:
        val = float(c_to_f.group(1))
        res = round((val * 9 / 5) + 32, 2)
        msg = f"{val} degrees Celsius is equal to {res} degrees Fahrenheit."
        speak(msg)
        log_command(query, msg)
        return

    f_to_c = re.search(r"(\d+(?:\.\d+)?)\s*(?:fahrenheit|f)\s*(?:to|in)\s*(?:celsius|c)", query)
    if f_to_c:
        val = float(f_to_c.group(1))
        res = round((val - 32) * 5 / 9, 2)
        msg = f"{val} degrees Fahrenheit is equal to {res} degrees Celsius."
        speak(msg)
        log_command(query, msg)
        return

    speak("Unit conversion format: e.g. convert 10 km to miles, 50 kg to lbs, or 37 celsius to fahrenheit.")

def calculate(query):
    expr = query.replace("calculate", "").replace("what is", "").replace("math", "").strip()

    expr = expr.replace("plus", "+").replace("minus", "-")
    expr = expr.replace("multiplied by", "*").replace("times", "*").replace("into", "*").replace("x", "*")
    expr = expr.replace("divided by", "/").replace("divided", "/").replace("over", "/")
    expr = expr.replace("power", "**").replace("raised to", "**")

    clean_expr = re.sub(r"[^\d\.\+\-\*\/\(\)\s\*\^]", "", expr)

    if not clean_expr.strip():
        speak("Could not parse mathematical expression.")
        return

    try:
        result = eval(clean_expr, {"__builtins__": None}, {})
        msg = f"The result of {clean_expr} is {result}"
        speak(f"The result is {result}")
        print(f"Math: {clean_expr} = {result}")
        log_command(query, msg)
    except Exception as e:
        log_error("Calculator evaluation error", e)
        speak("Unable to calculate result.")
