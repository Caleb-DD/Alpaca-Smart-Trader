# Sentiment and Technical Indicator Trading Bot

This project implements a trading bot that uses sentiment analysis and technical indicators to make trading decisions. It fetches news and chat data (for sentiment) and historical price data to execute trades based on different strategies.

## Features

* **Multiple Trading Strategies:**
    * Sentiment-based strategy
    * Moving average crossover strategy
    * Bollinger Bands strategy
    * RSI (Relative Strength Index) strategy
* **Alpaca API Integration:** Connects to the Alpaca trading API to execute trades.
* **Command-Line Interface:** Uses command-line arguments for flexible configuration.
* **Preset Management:** Save and load trading configurations as presets.
* **Logging:** Implements logging for better monitoring and debugging.

## Prerequisites

Before running the bot, ensure you have the following:

* Python 3.6 or higher
* An Alpaca trading account
* A Hugging Face account (for sentiment analysis)
* Git (for version control)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd sentiment-trading-bot
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    * You can optionally create a `.env` file in the project root directory to store your Alpaca API keys:

        ```
        ALPACA_API_KEY=your_alpaca_api_key
        ALPACA_SECRET_KEY=your_alpaca_secret_key
        ALPACA_BASE_URL=[https://paper-api.alpaca.markets](https://paper-api.alpaca.markets) # or [https://api.alpaca.markets](https://api.alpaca.markets) for live trading.
        ```

    * Add `.env` to your `.gitignore` file to prevent committing sensitive data.

5.  **Run the bot:**

    * See the "Usage" section below for command-line options.

## Usage

The bot is configured and run using command-line arguments.

###   General Arguments:

* `--api_key`:   Alpaca API key (required)
* `--secret_key`: Alpaca secret key (required)
* `--base_url`: Alpaca base URL (default: `https://paper-api.alpaca.markets`)
* `--symbol`:    Stock symbol (default: `AAPL`)
* `--dollar_amount`: Dollar amount to trade (default: `100.0`)
* `--check_interval`: Check interval in seconds (default: `300`)
* `--strategy`:  Trading strategy (default: `sentiment`)

###   Strategy-Specific Arguments:

####   Sentiment Strategy:

* No additional arguments.

####   Moving Average Strategy:

* `--short_window`: Short window for moving average (required)
* `--long_window`: Long window for moving average (required)
* `--timeframe`: Timeframe of the data to use (required) (e.g., `1Min`, `5Min`, `1Day`)

####   Bollinger Bands Strategy:

* `--window`: Window for Bollinger Bands (default: 20)
* `--num_std`: Number of standard deviations (default: 2)
* `--timeframe`: Timeframe of the data to use (default: `1Day`) (e.g., `1Min`, `5Min`, `1Day`)

####   RSI Strategy:

* `--window`: Window for RSI calculation (default: 14)
* `--overbought`: Overbought threshold (default: 70)
* `--oversold`: Oversold threshold (default: 30)
* `--timeframe`: Timeframe of the data to use (default: `1Day`) (e.g., `1Min`, `5Min`, `1Day`)

###   Examples:

* **Sentiment Strategy:**

    ```bash
    python TradingBot.py --api_key YOUR_API_KEY --secret_key YOUR_SECRET_KEY --symbol AAPL --dollar_amount 100 --check_interval 10 --strategy sentiment
    ```

* **Moving Average Strategy:**

    ```bash
    python TradingBot.py --api_key YOUR_API_KEY --secret_key YOUR_SECRET_KEY --symbol AAPL --dollar_amount 100 --check_interval 10 --strategy moving_average --short_window 20 --long_window 50 --timeframe 1Day
    ```

* **Bollinger Bands Strategy:**

    ```bash
    python TradingBot.py --api_key YOUR_API_KEY --secret_key YOUR_SECRET_KEY --symbol AAPL --dollar_amount 100 --check_interval 10 --strategy bollinger_bands --window 20 --num_std 2 --timeframe 1Day
    ```

* **RSI Strategy:**

    ```bash
    python TradingBot.py --api_key YOUR_API_KEY --secret_key YOUR_SECRET_KEY --symbol AAPL --dollar_amount 100 --check_interval 10 --strategy rsi --window 14 --overbought 70 --oversold 30 --timeframe 1Day
    ```

###   Preset Management

The bot allows you to save and load trading configurations as presets.

* **Saving Presets:**
    * After entering the parameters manually, you'll be prompted to save them as a preset.
    * Presets are stored as JSON files in the `presets/` directory.
* **Loading Presets:**
    * At the beginning of the script, you'll be asked if you want to use a preset.
    * If you choose to use a preset, you'll be able to select from the available presets.

## Dependencies

* `alpaca-trade-api`
* `transformers`
* `python-dotenv`
* `pandas`
* `pandas_ta`

## Disclaimer

This trading bot is provided for educational purposes only. Trading involves risks, and you should not trade with money you cannot afford to lose. Use this bot at your own risk.
