# strategies/rsi.py

import logging
import pandas as pd
import pandas_ta as ta

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

def trade_logic(symbol, dollar_amount, api, window=14, overbought=70, oversold=30, timeframe="1Day"):
    """Execute trading logic based on RSI."""
    try:
        barset = api.get_bars(symbol, timeframe, limit=window + 10)
        df = pd.DataFrame([bar._raw for bar in barset])
        df.set_index('t', inplace=True)

        rsi = ta.rsi(df['c'], length=window)
        current_rsi = rsi.iloc[-1]

        current_position = get_current_position(symbol, api)
        account = api.get_account()
        buying_power = float(account.buying_power)
        current_price = api.get_latest_trade(symbol).price
        quantity = int(dollar_amount / current_price) if dollar_amount / current_price < buying_power else int(buying_power/current_price)

        if current_rsi < oversold:
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

        elif current_rsi > overbought:
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
        logging.error(f"Error executing RSI strategy: {e}")