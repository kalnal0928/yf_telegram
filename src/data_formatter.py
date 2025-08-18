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
        weekly_change = data.get("weekly_change", 0)
        weekly_change_percent = data.get("weekly_change_percent", 0)
        daily_changes = data.get("daily_changes", [])
        volume = data.get("volume", 0)
        pe_ratio = data.get("pe_ratio", "N/A")
        fifty_two_week_high = data.get("fifty_two_week_high", 0)
        fifty_two_week_low = data.get("fifty_two_week_low", 0)

        emoji = "📈" if change > 0 else "📉"
        sign = "+" if change > 0 else ""
        weekly_sign = "+" if weekly_change > 0 else ""

        message += f"🍎 {name} ({ticker})\n"
        message += f"💰 일일 변동: ${current_price:.2f} ({sign}{change:.2f}, {sign}{change_percent:.2f}%) {emoji}\n"
        message += f"🗓️ 주간 변동: {weekly_sign}{weekly_change:.2f} ({weekly_sign}{weekly_change_percent:.2f}%)\n"
        
        if daily_changes:
            message += "\n📅 주간 일별 등락:\n"
            for daily_change in daily_changes:
                daily_sign = "+" if daily_change['change'] > 0 else ""
                daily_emoji = "📈" if daily_change['change'] > 0 else "📉"
                message += f"- {daily_change['date']}: {daily_sign}{daily_change['change']:.2f} ({daily_sign}{daily_change['change_percent']:.2f}%) {daily_emoji}\n"

        message += f"\n📈 52주 최고가: ${fifty_two_week_high:.2f} | 📉 52주 최저가: ${fifty_two_week_low:.2f}\n"
        message += f"📊 거래량: {volume:,} | PER: {pe_ratio}\n\n"

    return message

def format_vix_alert(vix_data):
    """
    Formats VIX alert data into a Telegram message.
    """
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) # KST
    message = f"🚨 VIX 지수 변동 알림 ({now.strftime('%Y-%m-%d %H:%M:%S KST')}) 🚨\n\n"
    
    current_price = vix_data.get('current_price', 0)
    change_percent = vix_data.get('change_percent', 0)

    message += f"VIX 지수가 급등했습니다!\n"
    message += f"현재 VIX: {current_price:.2f}\n"
    message += f"전일 대비: {change_percent:+.2f}%\n\n"

    if vix_data.get('price_alert'):
        message += "🔥 VIX 지수가 25를 돌파했습니다.\n"
    if vix_data.get('percent_alert'):
        message += "🔥 VIX 지수가 20% 이상 급등했습니다.\n"
        
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

    sample_vix_data = {
        'current_price': 26.5,
        'change_percent': 22.5,
        'price_alert': True,
        'percent_alert': True
    }
    formatted_vix_alert = format_vix_alert(sample_vix_data)
    print(formatted_vix_alert)