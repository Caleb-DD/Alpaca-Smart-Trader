# strategies/bollinger_bands.py

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

def trade_logic(symbol, dollar_amount, api, window=20, num_std=2, timeframe="1Day"):
    """Execute trading logic based on Bollinger Bands."""
    try:
        barset = api.get_bars(symbol, timeframe, limit=window + 10)
        df = pd.DataFrame([bar._raw for bar in barset])
        df.set_index('t', inplace=True)

        bbands = ta.bbands(df['c'], length=window, std=num_std)
        df = df.join(bbands)

        current_price = df['c'].iloc[-1]
        lower_band = df[f'BBL_{window}_{num_std}'].iloc[-1]
        upper_band = df[f'BBU_{window}_{num_std}'].iloc[-1]

        current_position = get_current_position(symbol, api)
        account = api.get_account()
        buying_power = float(account.buying_power)
        quantity = int(dollar_amount / current_price) if dollar_amount / current_price < buying_power else int(buying_power/current_price)

        if current_price <= lower_band:
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

        elif current_price >= upper_band:
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
        logging.error(f"Error executing Bollinger Bands strategy: {e}")