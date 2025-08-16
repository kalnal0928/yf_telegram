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
            
            if hist.empty:
                print(f"Warning: No history found for {ticker}, skipping.")
                continue

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

if __name__ == '__main__':
    # For testing purposes
    sample_tickers = ["AAPL", "GOOGL"]
    stock_data = get_stock_data(sample_tickers)
    print(stock_data)
