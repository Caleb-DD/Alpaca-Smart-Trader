# Alpaca Smart Trader

This project implements an automated trading bot that uses various strategies to make trading decisions. It integrates with the Alpaca trading API to execute trades based on user-defined configurations, which can be saved and loaded as presets.

## Features

* **Multiple Trading Strategies:**
    * Sentiment-based strategy
    * Moving average crossover strategy
    * Bollinger Bands strategy
    * RSI (Relative Strength Index) strategy
    * Option to make your own strategy
* **Alpaca API Integration:** Connects to the Alpaca trading API to execute trades.
* **Interactive Command-Line Interface:** Uses prompts to gather user inputs for flexible configuration.
* **Preset Management:** Save and load trading configurations as presets.
* **Logging:** Implements logging for better monitoring and debugging.
* **Input Validation:** Ensures that the users inputs are valid.

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
    cd alpaca-trading-bot
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

    ```bash
    python TradingBot.py
    ```

## Usage

The bot uses an interactive command-line interface. When you run `TradingBot.py`, it will prompt you for the necessary parameters.

###   Input Parameters:

* **Alpaca API Key:** Your Alpaca API key.
* **Alpaca Secret Key:** Your Alpaca secret key.
* **Alpaca Base URL:** Alpaca base URL (default: `https://paper-api.alpaca.markets`).
* **Stock Symbol:** Stock symbol (default: `AAPL`).
* **Dollar Amount to Trade:** Dollar amount to trade.
* **Check Interval:** Check interval in seconds (default: `10`).
* **Trading Strategy:** Trading strategy (`sentiment`, `moving_average`, `bollinger_bands`, `rsi`).

###   Strategy-Specific Inputs:

* **Moving Average Strategy:**
    * Short window for moving average.
    * Long window for moving average.
    * Timeframe of the data to use (e.g., `1Min`, `5Min`, `1Day`).
* **Bollinger Bands Strategy:**
    * Window for Bollinger Bands.
    * Number of standard deviations.
    * Timeframe of the data to use (e.g., `1Min`, `5Min`, `1Day`).
* **RSI Strategy:**
    * Window for RSI calculation.
    * Overbought threshold.
    * Oversold threshold.
    * Timeframe of the data to use (e.g., `1Min`, `5Min`, `1Day`).

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
