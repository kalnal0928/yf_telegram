import datetime

def format_stock_data(stock_data):
    """
    Formats stock data into a Telegram message.
    """
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) # KST
    message = f"📊 미국 주식 현황 ({now.strftime('%Y-%m-%d %H:%M:%S KST')})\n\n"

    for ticker, data in stock_data.items():
        if data is None:
            message += f"{ticker} 데이터를 가져오는데 실패했습니다.\n\n"
            continue

        name = data.get("name", ticker)
        current_price = data.get("current_price", 0)
        change = data.get("change", 0)
        change_percent = data.get("change_percent", 0)
        volume = data.get("volume", 0)
        pe_ratio = data.get("pe_ratio", "N/A")
        fifty_two_week_high = data.get("fifty_two_week_high", 0)
        fifty_two_week_low = data.get("fifty_two_week_low", 0)

        emoji = "📈" if change > 0 else "📉"
        sign = "+" if change > 0 else ""

        message += f"🍎 {name} ({ticker})\n"
        message += f"💰 ${current_price:.2f} ({sign}{change:.2f}, {sign}{change_percent:.2f}%) {emoji}\n"
        message += f"📈 52주 최고가: ${fifty_two_week_high:.2f} | 📉 52주 최저가: ${fifty_two_week_low:.2f}\n"
        message += f"📊 거래량: {volume:,} | PER: {pe_ratio}\n\n"

    return message

if __name__ == '__main__':
    # For testing purposes
    sample_data = {
        'AAPL': {
            'name': 'Apple Inc.',
            'current_price': 185.25,
            'change': 2.15,
            'change_percent': 1.17,
            'volume': 45200000,
            'pe_ratio': 28.5,
            'fifty_two_week_high': 199.62,
            'fifty_two_week_low': 164.08
        },
        'GOOGL': {
            'name': 'Alphabet Inc.',
            'current_price': 142.80,
            'change': -1.05,
            'change_percent': -0.73,
            'volume': 22800000,
            'pe_ratio': 25.2,
            'fifty_two_week_high': 151.55,
            'fifty_two_week_low': 101.88
        }
    }
    formatted_message = format_stock_data(sample_data)
    print(formatted_message)
