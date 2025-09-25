import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
from polygon import RESTClient
from datetime import datetime, timedelta

class PolygonDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"

    def fetch_equity_daily_bars(self, symbol, start_date, end_date):
        """
        Fetch daily historical equity price bars
        Args:
            symbol (str): Stock ticker symbol, e.g. 'AAPL'
            start_date (str): Start date in 'YYYY-MM-DD'
            end_date (str): End date in 'YYYY-MM-DD'
        Returns:
            pd.DataFrame: DataFrame with columns ['t', 'o', 'h', 'l', 'c', 'v'] (time, open, high, low, close, volume)
        """
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            "apiKey": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'results' not in data:
            raise Exception(f"No data found for {symbol}. Response: {data}")

        bars = data['results']
        df = pd.DataFrame(bars)
        df['t'] = pd.to_datetime(df['t'], unit='ms')
        df = df.rename(columns={'t': 'date', 'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
        return df[['date', 'open', 'high', 'low', 'close', 'volume']]

    def fetch_option_bars(self, option_symbol, start_date, end_date):
        """
        Fetch daily option open-close price data for a specific date.
        Args:
            option_symbol (str): Option symbol, e.g. 'AAPL230616C00150000' (standardized format)
            start_date (str): Date in 'YYYY-MM-DD' format
            end_date (str): Date in 'YYYY-MM-DD' format

        Returns:
            pd.DataFrame: DataFrame with columns ['date', 'open', 'high', 'low', 'close', 'volume']
        """
        client = RESTClient(self.api_key)

        aggs = []
        for a in client.list_aggs(
            f"O:{option_symbol}",
            1,
            "day",
            start_date,
            end_date,
            adjusted="true",
            sort="asc",
            limit=120,
        ):
            aggs.append(a)

        daily_list = [{
            "open": agg.open,
            "high": agg.high,
            "low": agg.low,
            "close": agg.close,
            "volume": agg.volume,
            "count": agg.transactions,
            "vwap": agg.vwap,
            "date": pd.to_datetime(agg.timestamp, unit='ms')
        } for agg in aggs]

        df = pd.DataFrame(daily_list)
        return df
