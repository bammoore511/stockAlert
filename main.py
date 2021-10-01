import os
import requests
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"

# load and instantiate environment variables
load_dotenv(".env")
news_api_key = os.getenv("news_api_key")
alpha_stock_key = os.getenv("alpha_stock_key")
twilio_sid = os.getenv("twilio_sid")
twilio_auth_token = os.getenv("twilio_auth_token")

# HTTP request for the stock data for STOCK
stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': alpha_stock_key,
}
stocks = requests.get(STOCK_API_ENDPOINT, params=stock_parameters)
stocks.raise_for_status()

# work with JSON data to get the closing price of the stock for yesterday and the day before.
stock_data = stocks.json()["Time Series (Daily)"]
stock_list = [value for (key, value) in stock_data.items()]

yesterday_close = float(stock_list[0]["5. adjusted close"])
day_before_close = float(stock_list[1]["5. adjusted close"])

# find the percent difference, and if it is greater than +- 5%
pct_difference = (abs(yesterday_close - day_before_close) / yesterday_close) * 100
if pct_difference > 5 or pct_difference < -5:
    pass

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# HTTP request for news articles for COMPANY_NAME
news = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={news_api_key}")
news.raise_for_status()
articles = news.json()["articles"]
print(articles)


# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

