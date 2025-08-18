import telegram
import os
import logging
import asyncio

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_telegram_message(message):
    """
    Sends a message to a Telegram chat asynchronously.
    """
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    logger.info(f"Bot token exists: {bool(bot_token)}")
    logger.info(f"Chat ID exists: {bool(chat_id)}")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set")
        return False
    
    if not chat_id:
        logger.error("TELEGRAM_CHAT_ID environment variable is not set")
        return False

    try:
        bot = telegram.Bot(token=bot_token)
        logger.info("Bot instance created successfully")
        
        # The new API does not have get_chat, so we can't validate the chat_id beforehand.
        # We will catch the exception on send_message instead.
        
        result = await bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN)
        logger.info(f"Message sent successfully! Message ID: {result.message_id}")
        return True
        
    except telegram.error.Unauthorized:
        logger.error("Bot token is invalid or bot is not authorized")
        return False
    except telegram.error.ChatNotFound:
        logger.error(f"Chat ID {chat_id} not found or bot is not a member")
        return False
    except telegram.error.Forbidden:
        logger.error("Bot is not allowed to send messages to this chat")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending message to Telegram: {e}")
        return False

if __name__ == '__main__':
    # 테스트용
    test_message = "*Test message* from the stock monitor!"
    asyncio.run(send_telegram_message(test_message))
