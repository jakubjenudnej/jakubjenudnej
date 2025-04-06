import os
import feedparser
import requests
from openai import OpenAI

# 🔐 Load secrets from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
pushover_user_key = os.getenv("PUSHOVER_USER_KEY")
pushover_app_token = os.getenv("PUSHOVER_APP_TOKEN")

# 🧠 OpenAI client
client = OpenAI(api_key=openai_api_key)

# 🌍 RSS sources
sources = {
    "BBC Tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC UK": "https://feeds.bbci.co.uk/news/rss.xml",
    "BBC US": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
    "CNN": "https://rss.cnn.com/rss/money_news_international.rss",
    "Novinky": "https://www.novinky.cz/rss",
    "Forbes": "https://www.forbes.com/technology/feed/",
    "Seznam Zprávy": "https://www.seznamzpravy.cz/rss",
    "PBS": "https://www.pbs.org/newshour/feeds/rss/headlines"
}

# 🏷️ Topics to track
topics = ["economy", "technology", "ai", "artificial intelligence", "stock market", "bitcoin", "elon musk", "trump"]

# 📥 Fetch articles based on keywords
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

# 🤖 Summarize articles using OpenAI
def summarize(articles):
    content = "\n".join(articles)

    # ✂️ Prevent too long prompts
    max_token_input = 7000
    if len(content.split()) > max_token_input:
        content = " ".join(content.split()[:max_token_input])

    if not content.strip():
        return "No relevant news articles found in the last 24 hours."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a news summarization assistant. Based on the articles below, generate a short and clear summary "
                    "divided into the following topics: Economy, Technology, Artificial Intelligence, Stock Market, Bitcoin, Elon Musk, Donald Trump. "
                    "Summarize only events from the last 24 hours. If there are no updates for a topic, say 'No major updates.' "
                    "Sources include BBC Tech, BBC UK, BBC US, CNN, Forbes, Novinky.cz, Seznam Zprávy, and PBS. "
                    "Output should be mobile-friendly and written in clear English."
                )
            },
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# 📲 Send summary via Pushover
def send_notification(message):
    data = {
        "token": pushover_app_token,
        "user": pushover_user_key,
        "title": "📰 Daily News for Jacob",
        "message": message[:1024]  # Limit to 1024 characters for Pushover
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    if response.status_code == 200:
        print("✅ Notification sent.")
    else:
        print("❌ Error sending notification:", response.text)

# 🚀 Run the full process
if __name__ == "__main__":
    articles = fetch_articles()
    if articles:
        summary = summarize(articles)
        send_notification(summary)
    else:
        send_notification("No relevant news articles found today.")
