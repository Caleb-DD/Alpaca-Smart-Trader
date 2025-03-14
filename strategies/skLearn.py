# strategies/sklearn_pattern.py

import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def get_current_position(symbol, api):
    """Check if a position exists for the given symbol."""
    try:
        positions = api.list_positions()
        for position in positions:
            if position.symbol == symbol:
                return position
        return None
    except Exception as e:
        logging.error(f"Error fetching positions: {e}")
        return None

def trade_logic(symbol, dollar_amount, api, timeframe="1Day", limit=100, trend_window=20):
    """Execute trading logic based on scikit-learn trend analysis."""
    try:
        barset = api.get_bars(symbol, timeframe, limit=limit)
        df = pd.DataFrame([bar._raw for bar in barset])
        df.set_index('t', inplace=True)

        # Calculate trend using linear regression
        prices = df['c'].values.reshape(-1, 1)
        times = np.arange(len(prices)).reshape(-1, 1)
        model = LinearRegression()
        model.fit(times[-trend_window:], prices[-trend_window:])

        # Predict future price
        future_time = times[-1] + 1
        predicted_price = model.predict([[future_time]])[0][0]

        # Determine trend direction
        current_price = df['c'].iloc[-1]
        trend_direction = "up" if predicted_price > current_price else "down"

        current_position = get_current_position(symbol, api)
        account = api.get_account()
        buying_power = float(account.buying_power)
        quantity = int(dollar_amount / current_price) if dollar_amount / current_price < buying_power else int(buying_power/current_price)

        if trend_direction == "up":
            if current_position:
                if int(current_position.qty) < 0:
                    logging.info(f"Closing short position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=abs(int(current_position.qty)), side='buy', type='market', time_in_force='gtc')
                    time.sleep(1)
                    logging.info(f"Opening long position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
                else:
                    logging.info(f"Already in long position for {symbol}. No action taken.")
            else:
                logging.info(f"No current position for {symbol}. Opening long position...")
                api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')

        elif trend_direction == "down":
            if current_position:
                if int(current_position.qty) > 0:
                    logging.info(f"Closing long position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=int(current_position.qty), side='sell', type='market', time_in_force='gtc')
                    time.sleep(1)
                    logging.info(f"Opening short position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')
                else:
                    logging.info(f"Already in short position for {symbol}. No action taken.")
            else:
                logging.info(f"No current position for {symbol}. Opening short position...")
                api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')

        else:
            logging.info(f"No signal detected for {symbol}.")

    except Exception as e:
        logging.error(f"Error executing sklearn_pattern strategy: {e}")