import pandas as pd

def prepare_returns(eq_df, opt_df):
    eq_df = eq_df.copy()
    eq_df['return_equity'] = eq_df['close'].pct_change()
    opt_df = opt_df.copy()
    combined = pd.merge(eq_df[['date', 'return_equity']], opt_df[['date', 'return_option']], on='date', how='inner')
    combined.dropna(inplace=True)
    return combined