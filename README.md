# US Stock Monitor with Telegram Notification System

This project automatically fetches real-time information about US stocks of interest and sends notifications to Telegram at specified times.

## Features

- Fetches stock data using `yfinance`.
- Formats the data into a human-readable message.
- Sends the message to a Telegram chat using a bot.
- Scheduled to run using GitHub Actions.

## Setup

1.  **Clone the repository.**
2.  **Install dependencies:** `pip install -r requirements.txt`
3.  **Configure stocks:** Edit `config/stocks.yaml` to add the stock tickers you want to monitor.
4.  **Set up Telegram bot:**
    *   Create a new bot using BotFather and get the token.
    *   Get your chat ID.
5.  **Set up GitHub Secrets:**
    *   `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
    *   `TELEGRAM_CHAT_ID`: Your Telegram chat ID.
6.  **Run the script manually:** You can trigger the workflow manually from the Actions tab in your GitHub repository.
