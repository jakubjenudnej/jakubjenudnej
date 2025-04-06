import os
import feedparser
import requests
from openai import OpenAI

# 🔐 Načtení API klíčů
openai_api_key = os.getenv("OPENAI_API_KEY")
pushover_user_key = os.getenv("PUSHOVER_USER_KEY")
pushover_app_token = os.getenv("PUSHOVER_APP_TOKEN")

# 🧠 Inicializace OpenAI klienta
client = OpenAI(api_key=openai_api_key)

# 🌍 RSS zdroje
sources = {
    "BBC": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "CNN": "https://rss.cnn.com/rss/money_news_international.rss",
    "Novinky": "https://www.novinky.cz/rss"
}

topics = ["ekonomika", "technologie", "AI", "burza", "bitcoin"]

# 📥 Získání článků
def fetch_articles():
    articles = []
    for source, url in sources.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            link = entry.link
            if any(topic.lower() in title.lower() for topic in topics):
                articles.append(f"[{source}] {title} – {link}")
    return articles

# 🤖 Shrnutí pomocí OpenAI
def summarize(articles):
    content = "\n".join(articles)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Shrň novinky podle témat a porovnej, jak je prezentují BBC, CNN a Novinky.cz."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# 📲 Odeslání notifikace přes Pushover
def send_notification(message):
    data = {
        "token": pushover_app_token,
        "user": pushover_user_key,
        "title": "📰 Denní shrnutí novinek",
        "message": message[:1024]  # limit Pushoveru
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    if response.status_code == 200:
        print("✅ Notifikace odeslána.")
    else:
        print("❌ Chyba při odesílání:", response.text)

# 🚀 Hlavní běh
if __name__ == "__main__":
    articles = fetch_articles()
    if articles:
        summary = summarize(articles)
        send_notification(summary)
    else:
        send_notification("Dnes nebyly nalezeny žádné relevantní novinky.")

