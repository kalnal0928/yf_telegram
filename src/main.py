import yaml
import os
import logging
import asyncio
from stock_fetcher import get_stock_data, check_vix_alert
from data_formatter import format_stock_data, format_vix_alert
from telegram_sender import send_telegram_message

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """
    Main function to run the stock monitor.
    """
    try:
        # Get the absolute path to the config file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "config", "stocks.yaml")
        
        logger.info(f"Config path: {config_path}")

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            tickers = config.get("tickers", [])

        logger.info(f"Found tickers: {tickers}")

        if not tickers:
            logger.error("No tickers found in config/stocks.yaml")
            return

        stock_data = get_stock_data(tickers)
        if not stock_data:
            logger.error("No stock data fetched.")
            # Continue to check VIX even if other stocks fail
        else:
            logger.info(f"Stock data fetched for {len(stock_data)} tickers")
            message = format_stock_data(stock_data)
            logger.info(f"Formatted message length: {len(message)} characters")
            
            # 텔레그램 전송 시도
            success = await send_telegram_message(message)
            if success:
                logger.info("Stock alert sent successfully!")
            else:
                logger.error("Failed to send stock alert to Telegram")

        # Check for VIX alert
        logger.info("Checking for VIX alert...")
        vix_alert_data = check_vix_alert()
        if vix_alert_data:
            logger.info("VIX alert triggered!")
            vix_message = format_vix_alert(vix_alert_data)
            success = await send_telegram_message(vix_message)
            if success:
                logger.info("VIX alert sent successfully!")
            else:
                logger.error("Failed to send VIX alert to Telegram")
        else:
            logger.info("No VIX alert.")
            
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        # Send error message to Telegram
        error_message = f"🚨 Stock Alerter Error 🚨\n\nAn error occurred: {e}"
        await send_telegram_message(error_message)
        raise

if __name__ == "__main__":
    asyncio.run(main())