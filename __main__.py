import os
from dotenv import load_dotenv
from data_fetch import PolygonDataFetcher
from options_strategy import OptionStrategy
import pandas as pd
from compute_returns import prepare_returns

if __name__ == "__main__":
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    fetcher = PolygonDataFetcher(API_KEY)

    symbol = os.getenv("SYMBOL")
    option_symbol = os.getenv("OPTION_SYMBOL")
    options_date = os.getenv("OPTIONS_DATE")
    equity_start_date = os.getenv("EQUITY_START_DATE")
    equity_end_date = os.getenv("EQUITY_END_DATE")

    try:
        eq_data = fetcher.fetch_equity_daily_bars(symbol, equity_start_date, equity_end_date)
        eq_data['date'] = pd.to_datetime(eq_data['date'])
        print("Equity Data Sample")
        print(eq_data)
        print("\n\n")
        opt_data = fetcher.fetch_option_bars(option_symbol, equity_start_date, equity_end_date)
        opt_data['date'] = pd.to_datetime(opt_data['date'])
        print("Option Data Sample")
        print(opt_data)
        print("\n\n")

        strategy = OptionStrategy(opt_data)
        options_returns_df = strategy.compute_returns()

        combined_returns = prepare_returns(eq_data, options_returns_df)
        print(combined_returns)
    except Exception as e:
        print(f"Option data fetch error: {e}")