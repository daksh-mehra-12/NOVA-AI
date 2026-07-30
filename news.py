import os
import xml.etree.ElementTree as ET
import requests
from logger import log_command, log_error
from voice import speak

def getNews():
    api_key = os.getenv("NEWS_API_KEY", "YOUR_NEWS_API_KEY")

    if api_key != "YOUR_NEWS_API_KEY":
        try:
            if api_key.startswith("pub_"):
                url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=in&language=en"
            else:
                url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

            res = requests.get(url, timeout=5)
            data = res.json()

            articles = data.get("results", []) or data.get("articles", [])
            if articles:
                speak("Here are today's top news headlines.")
                for i, article in enumerate(articles[:5]):
                    title = article.get("title")
                    if title:
                        print(f"News {i+1}: {title}")
                        speak(f"News {i+1}: {title}")
                log_command("news", "Fetched news headlines via News API.")
                return
        except Exception as e:
            log_error("News API error", e)

    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            items = root.findall(".//item")[:5]

            if items:
                speak("Here are the latest top news headlines.")
                for i, item in enumerate(items):
                    title = item.find("title").text
                    print(f"News {i+1}: {title}")
                    speak(f"News {i+1}: {title}")
                log_command("news", "Fetched news headlines via Google News RSS.")
                return
    except Exception as e:
        log_error("Google News RSS error", e)

    speak("Unable to fetch top news headlines at the moment.")
