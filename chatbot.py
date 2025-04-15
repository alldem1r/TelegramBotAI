import google.generativeai as genai
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

TELEGRAM_BOT_TOKEN = "7437578911:AAGBhWRgYrVIL4wZFK2CC8TZV90fOB0ys5E"
GEMINI_API_KEY = "AIzaSyB_vl6q8lrLJt_KQvjr-cqCc1RHctvQnh0"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

predefined_answers = {
    "who created you?": "Sultan Zhumakadyr",
    "who are you?": "My name is Milo.",
    "what do you do?": "Answer your questions.",
    "кто тебя создал?": "Султан Жумакадыр",
    "кто ты?": "Меня зовут Майло.",
    "что ты делаешь?": "Отвечаю на ваши вопросы.",
}

def start(update, context):
    """Sends a welcome message when the /start command is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your conversational bot. Ask me anything!")

def handle_message(update, context):
    """Handles incoming text messages."""
    user_message = update.message.text.lower()  # Convert to lowercase for easier matching.

    if user_message in predefined_answers:
        response_text = predefined_answers[user_message]
    else:
        try:
            response = model.generate_content(update.message.text)
            response_text = response.text
        except Exception as e:
            response_text = f"Sorry, I encountered an error: {e}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def error(update, context):
    """Log Errors caused by Updates."""
    print(f'Update {update} caused error {context.error}')

def main():
    """Starts the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()