import yfinance as yf
import pandas as pd

def get_stock_data(tickers):
    """
    Fetches stock data for a list of tickers.
    """
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="8d") # 7일 전 데이터까지 가져오기
            
            if hist.empty or len(hist) < 2:
                print(f"Warning: Not enough history found for {ticker}, skipping.")
                continue

            # 일일 변동 계산
            daily_changes_list = []
            # 어제 종가부터 7일 전까지, 총 7개 데이터
            for i in range(1, min(8, len(hist))):
                prev_close = hist['Close'].iloc[-i-1]
                current_close = hist['Close'].iloc[-i]
                change = current_close - prev_close
                change_percent = (change / prev_close) * 100 if prev_close else 0
                daily_changes_list.append({
                    'date': hist.index[-i].strftime('%m-%d'),
                    'change': change,
                    'change_percent': change_percent
                })
            daily_changes_list.reverse() # 최신 날짜가 위로 오도록

            # 주간 변동 계산
            price_7d_ago = hist['Close'].iloc[0]
            current_price = info.get("currentPrice", info.get("regularMarketPrice"))
            weekly_change = current_price - price_7d_ago
            weekly_change_percent = (weekly_change / price_7d_ago) * 100 if price_7d_ago else 0

            data[ticker] = {
                "current_price": current_price,
                "previous_close": info.get("previousClose"),
                "change": 0,
                "change_percent": 0,
                "weekly_change": weekly_change,
                "weekly_change_percent": weekly_change_percent,
                "daily_changes": daily_changes_list,
                "volume": info.get("volume"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "name": info.get("shortName", ticker)
            }

            if data[ticker]["current_price"] and data[ticker]["previous_close"]:
                change = data[ticker]["current_price"] - data[ticker]["previous_close"]
                data[ticker]["change"] = change
                data[ticker]["change_percent"] = (change / data[ticker]["previous_close"]) * 100 if data[ticker]["previous_close"] else 0
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            data[ticker] = None
    return data

def check_vix_alert():
    """
    Checks for VIX alert conditions.
    """
    try:
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="2d")

        if hist.empty or len(hist) < 2:
            print("Warning: Not enough history found for VIX, skipping alert check.")
            return None

        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2]
        
        price_alert = current_price > 25
        
        change_percent = ((current_price - previous_close) / previous_close) * 100
        percent_alert = change_percent > 20

        if price_alert or percent_alert:
            return {
                "current_price": current_price,
                "change_percent": change_percent,
                "price_alert": price_alert,
                "percent_alert": percent_alert
            }
            
    except Exception as e:
        print(f"Error checking VIX alert: {e}")
    
    return None

if __name__ == '__main__':
    # For testing purposes
    sample_tickers = ["AAPL", "GOOGL"]
    stock_data = get_stock_data(sample_tickers)
    import json
    print("--- Stock Data ---")
    print(json.dumps(stock_data, indent=4))

    print("\n--- VIX Alert Check ---")
    vix_alert_data = check_vix_alert()
    if vix_alert_data:
        from data_formatter import format_vix_alert
        alert_message = format_vix_alert(vix_alert_data)
        print(alert_message)
    else:
        print("No VIX alert.")