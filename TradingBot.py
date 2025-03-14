import time
import os
from alpaca_trade_api import REST
from transformers import pipeline
import logging
import argparse
from importlib import import_module

# === Configuration ===

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize sentiment analysis pipeline
try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    logging.error(f"Failed to initialize sentiment pipeline: {e}")
    exit(1)

# === Main Bot Loop ===

def run_bot(api_key, secret_key, base_url, symbol, dollar_amount, check_interval, strategy, **strategy_kwargs):
    try:
        api = REST(api_key, secret_key, base_url=base_url)
        # Import the selected strategy module
        try:
            strategy_module = import_module(f"strategies.{strategy}")
        except ImportError:
            logging.error(f"Strategy '{strategy}' not found in 'strategies' directory.")
            return

        while True:
            # Execute the trading logic from the strategy module
            try:
                strategy_module.trade_logic(symbol, dollar_amount, api, **strategy_kwargs)
            except Exception as e:
                logging.error(f"Error executing strategy '{strategy}': {e}")

            time.sleep(int(check_interval))
    except Exception as e:
        logging.error(f"Bot execution error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trading Bot")
    parser.add_argument("--api_key", required=True, help="Alpaca API key")
    parser.add_argument("--secret_key", required=True, help="Alpaca secret key")
    parser.add_argument("--base_url", default="https://paper-api.alpaca.markets", help="Alpaca base URL")
    parser.add_argument("--symbol", default="AAPL", help="Stock symbol")
    parser.add_argument("--dollar_amount", type=float, default=100.0, help="Dollar amount to trade")
    parser.add_argument("--check_interval", type=int, default=300, help="Check interval in seconds")
    parser.add_argument("--strategy", default="sentiment", help="Trading strategy (sentiment, moving_average, etc.)")

    # Strategy-specific arguments (you can add more as needed)
    if parser.parse_known_args()[0].strategy == "moving_average":
        parser.add_argument("--short_window", type=int, default=20, help="Short window for moving average")
        parser.add_argument("--long_window", type=int, default=50, help="Long window for moving average")
        parser.add_argument("--timeframe", default="1Day", help="Timeframe of the data to use. (1Min, 5Min, 15Min, 1Day etc.)")

    args = parser.parse_args()

    # Pass strategy-specific arguments as keyword arguments
    strategy_kwargs = {}
    if args.strategy == "moving_average":
        strategy_kwargs["short_window"] = args.short_window
        strategy_kwargs["long_window"] = args.long_window
        strategy_kwargs["timeframe"] = args.timeframe

    run_bot(args.api_key, args.secret_key, args.base_url, args.symbol, args.dollar_amount, args.check_interval, args.strategy, **strategy_kwargs)