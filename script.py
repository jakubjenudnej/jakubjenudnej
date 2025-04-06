import openai
import feedparser
import requests
import os

# 🔐 Načtení API klíčů
openai.api_key = os.getenv("OPENAI_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")

# 🌍 RSS zdroje
sources = {
    "BBC": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "CNN": "https://rss.cnn.com/rss/money_news_international.rss",
    "Novinky": "https://www.novinky.cz/rss",
}

topics = ["ekonomika", "technologie", "AI", "burza", "bitcoin"]

# 📥 Stažení článků
def fetch_articles():
    articles = []
    for source, url in sources.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            content = f"{entry.title} – {entry.link}"
            if any(topic.lower() in entry.title.lower() for topic in topics):
                articles.append(f"[{source}] {content}")
    return articles

# 🤖 Shrnutí pomocí OpenAI
def summarize(articles):
    content = "\n".join(articles)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Shrň novinky podle témat a porovnej, jak je prezentují BBC, CNN a Novinky.cz."},
            {"role": "user", "content": content}
        ]
    )
    return response["choices"][0]["message"]["content"]

# 📲 Odeslání přes Pushover
def send_notification(message):
    data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": "📰 Denní shrnutí novinek",
        "message": message[:1024]  # limit
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
