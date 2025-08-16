# The `python-telegram-bot` package provides the `telegram` module.
import telegram
import os

def send_telegram_message(message):
    """
    Sends a message to a Telegram chat.
    """
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables not set.")
        return

    try:
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

if __name__ == '__main__':
    # For testing purposes. 
    # You need to set the environment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
    test_message = "*Test message* from the stock monitor!"
    send_telegram_message(test_message)