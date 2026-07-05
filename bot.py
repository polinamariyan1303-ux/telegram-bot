import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8961218182:AAF17RA7SwHn3qLPCsGz8JfIVha9Bvu"
YANDEX_API_KEY = "AQVNWlucEz6w9rj_XYbJ-oNAUjNzc0OdodgQ-Yz"
AGENT_ID = "ag-fvtggoimbgmjmf0oqf94"

def ask_bot(user_message):
    url = f"https://api.yandex.cloud/ai/assistant/v1/agents/{AGENT_ID}/chat"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"message": user_message, "session_id": "telegram_user"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if "result" in result and "message" in result["result"]:
                return result["result"]["message"]["text"]
            elif "answer" in result:
                return result["answer"]
            elif "text" in result:
                return result["text"]
            else:
                return f"Ошибка: неожиданный формат ответа\n{result}"
        else:
            return f"❌ Ошибка API: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот для претензий\n\n"
        "Привет! Кидай мне текст жалобы клиента, и я дам готовый ответ по закону.\n\n"
        "📌 Пример:\n"
        "«Клиент купил телефон 10 дней назад, экран сломался. Требует вернуть деньги.»"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Анализирую...")
    response = ask_bot(update.message.text)
    await update.message.reply_text(response)

def main():
    print("🚀 Запуск бота...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
