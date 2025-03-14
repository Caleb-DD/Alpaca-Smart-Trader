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
    except Exception as e:
        logging.error(f"Error fetching positions: {e}")
    return None

def trade_logic(symbol, dollar_amount, api, short_window, long_window, timeframe):
    """Execute trading logic based on moving average crossover."""
    try:
        # Fetch historical price data
        barset = api.get_bars(symbol, timeframe, limit=long_window + 10)
        df = pd.DataFrame([bar._raw for bar in barset])
        df.set_index('t', inplace=True)
        # Calculate moving averages
        short_ma = ta.sma(df['c'], length=short_window)
        long_ma = ta.sma(df['c'], length=long_window)
        # Detect crossovers
        current_position = get_current_position(symbol, api)
        account = api.get_account()
        buying_power = float(account.buying_power)
        current_price = api.get_latest_trade(symbol).price
        quantity = int(dollar_amount / current_price) if dollar_amount / current_price < buying_power else int(buying_power/current_price)
        if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
            # Golden cross
            # ... (open long position)
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
            logging.info(f'golden cross detected, opening long position for {symbol}')
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
            # Death cross
            # ... (open short position)
            if current_position:
                if int(current_position.qty) > 0:
                    logging.info(f"Closing long position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=abs(int(current_position.qty)), side='buy', type='market', time_in_force='gtc')
                    time.sleep(1)
                    logging.info(f"Opening short position for {symbol}...")
                    api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
                else:
                    logging.info(f"Already in long position for {symbol}. No action taken.")
            else:
                logging.info(f"No current position for {symbol}. Opening short position...")
                api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')
            logging.info(f'death cross detected, opening short position for {symbol}')
        else:
            logging.info(f'no crossover detected for {symbol}')
    except Exception as e:
        logging.error(f"Error executing moving average strategy: {e}")