import os
import feedparser
import requests
from openai import OpenAI

# 🔐 API klíče
openai_api_key = os.getenv("OPENAI_API_KEY")
pushover_user_key = os.getenv("PUSHOVER_USER_KEY")
pushover_app_token = os.getenv("PUSHOVER_APP_TOKEN")

# 🧠 OpenAI klient
client = OpenAI(api_key=openai_api_key)

# 🌍 RSS zdroje
sources = {
    "BBC": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "CNN": "https://rss.cnn.com/rss/money_news_international.rss",
    "Novinky": "https://www.novinky.cz/rss"
}

# 🏷️ Klíčová slova
topics = ["ekonomika", "technologie", "AI", "burza", "bitcoin", "elon musk", "trump"]

# 📥 Stažení článků
def fetch_articles():
    articles = []
    for source, url in sources.items():
        feed = feedparser.parse(url)
        count = 0
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            combined = f"{title} {entry.get('summary', '')}".lower()

            if any(topic in combined for topic in topics):
                articles.append(f"[{source}] {title} – {link}")
                count += 1
            if count >= 10:
                break
    return articles

# 🤖 Shrnutí pomocí OpenAI
def summarize(articles):
    content = "\n".join(articles)
    if not content.strip():
        return "Dnes nebyly nalezeny žádné relevantní články ke sledovaným tématům."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Jsi zpravodajský asistent. Shrni hlavní témata z následujících článků "
                    "a pokud možno porovnej, jak se liší pohled BBC, CNN a Novinky.cz. "
                    "Zaměř se na témata jako AI, ekonomika, burza, bitcoin, Elon Musk, Trump."
                )
            },
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# 📲 Odeslání notifikace
def send_notification(message):
    data = {
        "token": pushover_app_token,
        "user": pushover_user_key,
        "title": "📰 Denní shrnutí novinek",
        "message": message[:1024]  # Pushover limit
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
