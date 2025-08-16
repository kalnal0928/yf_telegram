import yaml
import os
import logging
from stock_fetcher import get_stock_data
from data_formatter import format_stock_data
from telegram_sender import send_telegram_message

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
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
            return

        logger.info(f"Stock data fetched for {len(stock_data)} tickers")

        message = format_stock_data(stock_data)
        logger.info(f"Formatted message length: {len(message)} characters")
        
        # 텔레그램 전송 시도
        success = send_telegram_message(message)
        if success:
            logger.info("Stock alert sent successfully!")
        else:
            logger.error("Failed to send stock alert to Telegram")
            
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()