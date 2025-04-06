import os
import feedparser
import requests
from openai import OpenAI

# 🔐 API klíče z GitHub Secrets
openai_api_key = os.getenv("OPENAI_API_KEY")
pushover_user_key = os.getenv("PUSHOVER_USER_KEY")
pushover_app_token = os.getenv("PUSHOVER_APP_TOKEN")

# 🧠 Inicializace OpenAI klienta
client = OpenAI(api_key=openai_api_key)

# 🌍 Zpravodajské zdroje (RSS)
sources = {
    "BBC Tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC UK": "https://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "https://rss.cnn.com/rss/money_news_international.rss",
    "Novinky": "https://www.novinky.cz/rss",
    "Forbes": "https://www.forbes.com/technology/feed/",
    "Seznam Zprávy": "https://www.seznamzpravy.cz/rss",
    "PBS": "https://www.pbs.org/newshour/feeds/rss/headlines"
}

# 🏷️ Sledovaná témata
topics = ["ekonomika", "technologie", "AI", "umělá inteligence", "burza", "bitcoin", "elon musk", "trump"]

# 📥 Získání článků podle témat
def fetch_articles():
    articles = []
    for source, url in sources.items():
        feed = feedparser.parse(url)
        count = 0
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            summary = entry.get("summary", "")
            combined = f"{title} {summary}".lower()

            if any(topic in combined for topic in topics):
                articles.append(f"[{source}] {title} – {link}")
                count += 1
            if count >= 10:
                break
    return articles

# 🤖 Shrnutí podle témat s rozdělením
def summarize(articles):
    content = "\n".join(articles)

    # 🧤 Pojistka na délku promptu
    max_token_input = 7000
    if len(content.split()) > max_token_input:
        content = " ".join(content.split()[:max_token_input])

    if not content.strip():
        return "Dnes nebyly nalezeny žádné relevantní články ke sledovaným tématům."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Jsi zpravodajský asistent. Na základě článků níže vytvoř stručné shrnutí "
                    "rozdělené podle následujících témat: Ekonomika, Technologie, Umělá inteligence, Burza, Bitcoin, Elon Musk, Donald Trump. "
                    "U každého tématu napiš, co se za posledních 24 hodin stalo. "
                    "Pokud nejsou žádné relevantní informace, napiš 'Žádné nové zprávy.' "
                    "Zdroje zahrnují BBC Tech, BBC UK, CNN, Novinky.cz, Forbes, Seznam Zprávy a PBS. "
                    "Výstup napiš přehledně, pro zobrazení na telefonu."
                )
            },
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# 📲 Odeslání přes Pushover
def send_notification(message):
    data = {
        "token": pushover_app_token,
        "user": pushover_user_key,
        "title": "📰 Daily News for Jacob",
        "message": message[:1024]  # limit 1024 znaků
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

