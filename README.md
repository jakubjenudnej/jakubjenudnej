# 📰 Daily News for Jacob

Tento projekt automaticky každý den v 6:00 (čas Praha):

- 📡 Stáhne aktuální novinky z:
  - BBC UK & BBC Technology
  - CNN
  - Novinky.cz
  - Forbes (Tech)
  - Seznam Zprávy
  - PBS (americká veřejnoprávní TV)

- 🧠 Nechá ChatGPT (OpenAI) vytvořit přehledně strukturované shrnutí:
  - Rozdělené podle témat: Ekonomika, Technologie, AI, Burza, Bitcoin, Elon Musk, Trump

- 📲 Pošle shrnutí přes **Pushover** jako notifikaci na tvůj telefon, tablet nebo MacBook

---

## 🚀 Co potřebuješ

### 🔐 API klíče (vlož jako GitHub Secrets):
| Název                | Odkud získat                                     |
|----------------------|--------------------------------------------------|
| `OPENAI_API_KEY`     | [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) |
| `PUSHOVER_USER_KEY`  | Po přihlášení na [https://pushover.net](https://pushover.net) |
| `PUSHOVER_APP_TOKEN` | Vytvoř si vlastní app na [https://pushover.net/apps/build](https://pushover.net/apps/build) |

---

## ⚙️ Automatické spouštění

Skript se spouští každý den automaticky díky **GitHub Actions**.

🕕 Spouštění nastaveno na `0 4 * * *` (4:00 UTC = 6:00 Praha)

Můžeš také spustit ručně přes záložku **Actions → Run workflow**

---

## 📥 Výstup

Strukturované shrnutí novinek jako:

