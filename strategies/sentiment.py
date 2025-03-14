import time
import logging
from transformers import pipeline

# Initialize sentiment analysis pipeline (this should ideally be done only once)
try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    logging.error(f"Failed to initialize sentiment pipeline: {e}")
    exit(1)

def get_sentiment(texts):
    """Analyze sentiment from a list of text inputs."""
    positive_score = 0.0
    negative_score = 0.0
    for text in texts:
        if not text:
            continue
        try:
            result = sentiment_pipeline(text)[0]
            label = result['label'].upper()
            score = result['score']
            if label == "POSITIVE":
                positive_score += score
            else:
                negative_score += score
        except Exception as e:
            logging.error(f"Sentiment analysis error: {e}")
            continue

    if positive_score + negative_score == 0:
        return "neutral"
    return "positive" if positive_score >= negative_score else "negative"

def fetch_news_and_chat(symbol):
    """Fetch news and chat messages for the given symbol."""
    # Replace with real API calls to news or chat data sources.
    # For now, using dummy data.
    news_text = "The company has reported record earnings and strong growth prospects."
    chat_text = "Investors are excited about the future of this company!"
    return [news_text, chat_text]

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

def trade_logic(symbol, dollar_amount, api):
    """Execute trading logic based on the aggregated sentiment."""
    texts = fetch_news_and_chat(symbol)
    sentiment = get_sentiment(texts)
    try:
        account = api.get_account()
        buying_power = float(account.buying_power)
        current_price = api.get_latest_trade(symbol).price
        quantity = int(dollar_amount / current_price) if dollar_amount / current_price < buying_power else int(buying_power/current_price)
        current_position = get_current_position(symbol, api)

        if sentiment == "positive":
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

        elif sentiment == "negative":
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
            logging.info("Sentiment unclear. No trading action taken.")
    except Exception as e:
        logging.error(f"Error executing trade logic: {e}")
