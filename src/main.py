import yaml
from stock_fetcher import get_stock_data
from data_formatter import format_stock_data
from telegram_sender import send_telegram_message

def main():
    """
    Main function to run the stock monitor.
    """
    with open("../config/stocks.yaml", "r") as f:
        config = yaml.safe_load(f)
        tickers = config.get("tickers", [])

    if not tickers:
        print("No tickers found in config/stocks.yaml")
        return

    stock_data = get_stock_data(tickers)
    if not stock_data:
        print("No stock data fetched.")
        return

    message = format_stock_data(stock_data)
    send_telegram_message(message)

if __name__ == "__main__":
    main()
