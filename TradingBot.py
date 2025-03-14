import time
import os
from alpaca_trade_api import REST
from transformers import pipeline
import logging
from importlib import import_module
import json

# === Configuration ===

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize sentiment analysis pipeline
try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    logging.error(f"Failed to initialize sentiment pipeline: {e}")
    exit(1)

# === Helper Functions ===

def load_preset(preset_name):
    """Loads a preset from a JSON file."""
    try:
        with open(f"presets/{preset_name}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Preset '{preset_name}' not found.")
        return None

def save_preset(preset_name, params):
    """Saves parameters as a preset in a JSON file."""
    os.makedirs("presets", exist_ok=True)
    with open(f"presets/{preset_name}.json", "w") as f:
        json.dump(params, f, indent=4)

# === Main Bot Loop ===

def run_bot(api_key, secret_key, base_url, symbol, dollar_amount, check_interval, strategy, **strategy_kwargs):
    try:
        api = REST(api_key, secret_key, base_url=base_url)
        try:
            strategy_module = import_module(f"strategies.{strategy}")
        except ImportError:
            logging.error(f"Strategy '{strategy}' not found in 'strategies' directory.")
            return

        while True:
            # Debugging: Print dollar_amount
            print(f"Debugging: dollar_amount in run_bot: {dollar_amount}")

            try:
                strategy_module.trade_logic(symbol, dollar_amount, api, **strategy_kwargs)
            except Exception as e:
                logging.error(f"Error executing strategy '{strategy}': {e}")
            time.sleep(int(check_interval))
    except Exception as e:
        logging.error(f"Bot execution error: {e}")

if __name__ == "__main__":
    use_preset = input("Use preset? (yes/no): ").lower() == "yes"

    try:
        if use_preset:
            try:
                presets = [f.split(".json")[0] for f in os.listdir("presets") if f.endswith(".json")]
                print("Available presets:", presets)
                preset_name = input("Enter preset name: ")
                params = load_preset(preset_name)
                if params:
                    api_key = params["api_key"]
                    secret_key = params["secret_key"]
                    base_url = params.get("base_url", "https://paper-api.alpaca.markets")
                    symbol = params["symbol"]
                    dollar_amount = params["dollar_amount"]
                    check_interval = params["check_interval"]
                    strategy = params["strategy"]
                    strategy_kwargs = params.get("strategy_kwargs", {})
                else:
                    exit()
            except FileNotFoundError:
                print("No presets folder found, running manual input")
                use_preset = False
        if not use_preset:
            api_key = input("Enter Alpaca API Key: ")
            secret_key = input("Enter Alpaca Secret Key: ")
            base_url = input("Enter Alpaca Base URL (default: https://paper-api.alpaca.markets): ") or "https://paper-api.alpaca.markets"
            symbol = input("Enter Stock Symbol (default: AAPL): ") or "AAPL"
            while True:
                try:
                    dollar_amount = float(input("Enter Dollar Amount to Trade: "))
                    if dollar_amount > 0:
                        break
                    else:
                        print("Dollar amount must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            check_interval = int(input("Enter Check Interval (seconds, default: 10): ") or 10)
            strategy = input("Enter Trading Strategy (sentiment, moving_average): ") or "sentiment"

            strategy_kwargs = {}
            if strategy == "moving_average":
                strategy_kwargs["short_window"] = int(input("Enter Short Window for Moving Average: "))
                strategy_kwargs["long_window"] = int(input("Enter Long Window for Moving Average: "))
                strategy_kwargs["timeframe"] = input("Enter Timeframe (1Min, 5Min, 1Day, etc.): ")

            save_option = input("Save as preset? (yes/no): ").lower() == "yes"
            if save_option:
                preset_name = input("Enter preset name: ")
                # Ensure dollar_amount is converted to float before saving
                params = {
                    "api_key": api_key,
                    "secret_key": secret_key,
                    "base_url": base_url,
                    "symbol": symbol,
                    "dollar_amount": float(dollar_amount),
                    "check_interval": check_interval,
                    "strategy": strategy,
                    "strategy_kwargs": strategy_kwargs,
                }
                save_preset(preset_name, params)

        # Debugging: Print dollar_amount
        print(f"Debugging: dollar_amount before run_bot: {dollar_amount}")

        run_bot(api_key, secret_key, base_url, symbol, dollar_amount, check_interval, strategy, **strategy_kwargs)
    except Exception as e:
        print(f"An error occurred during input: {e}")
        