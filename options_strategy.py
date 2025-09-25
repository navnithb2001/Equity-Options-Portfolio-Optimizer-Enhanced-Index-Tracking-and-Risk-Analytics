import pandas as pd

class OptionStrategy:
    def __init__(self, option_price_df, initial_cash=10000):
        self.data = option_price_df.sort_values('date').reset_index(drop=True)
        self.cash = initial_cash
        self.position = 0  # number of option contracts held
        self.position_value = 0
        self.valuations = []  # portfolio value over time

    def trading_rule(self, row):
        """ 
        Example trading rule:
         - Buy if there is no position and price dropped more than 1% prior day
         - Sell if price increased more than 1% prior day and have position
         This is a placeholder - you can replace this with complex logic
        """

        idx = row.name
        if idx == 0:
            return  # no trade on first day due to no prior data

        prev_price = self.data.loc[idx - 1, 'close']
        price = row['close']
        price_return = (price - prev_price) / prev_price

        if self.position == 0 and price_return < -0.01:
            # Buy as many contracts as possible
            self.position = self.cash // price
            self.cash -= self.position * price
        elif self.position > 0 and price_return > 0.01:
            # Sell all positions
            self.cash += self.position * price
            self.position = 0

    def run_strategy(self):
        for idx, row in self.data.iterrows():
            self.trading_rule(row)
            # Portfolio value is cash + position value at current close price
            current_price = row['close']
            self.position_value = self.position * current_price
            total_value = self.cash + self.position_value
            self.valuations.append({'date': row['date'], 'value': total_value})

        return pd.DataFrame(self.valuations)

    def compute_returns(self):
        valuation_df = self.run_strategy()
        valuation_df['return_option'] = valuation_df['value'].pct_change()
        return valuation_df

# # Usage example
# if __name__ == "__main__":
#     # option_price_df should be a DataFrame with columns ['date', 'close']
#     # loaded from your fetched option price data
#     option_price_df = pd.DataFrame({
#         'date': pd.date_range("2025-07-01", periods=10, freq='D'),
#         'close': [58.29, 62.37, 63.55, 63.10, 58.64, 59.00, 60.0, 61.5, 62.0, 63.0]
#     })

#     strategy = OptionStrategy(option_price_df)
#     returns_df = strategy.compute_returns()
#     print(returns_df)
