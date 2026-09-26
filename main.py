import sys
import os
import time

sys.path.append(os.path.abspath('./src'))

try:
    from src.config import Config
    from src.connector import DerivConnector
except ImportError as e:
    print(f"Critical Import Error: {e}")
    sys.exit(1)

def start_bot():
    print("🚀 Starting Deriv Pro Trader Engine...")
    
    try:
        Config.validate()
        print("⚙️ Configuration Validated.")
    except ValueError as ve:
        print(f"❌ Stop! {ve}")
        return

    connector = DerivConnector()
    connector.connect()
    
    print("📊 Fetching initial market data...")
    candles = connector.get_latest_candles(count=5)
    
    if candles:
        last_close = candles[-1]['close']
        print(f"✅ Market Data Received. Last Close Price: {last_close}")
    else:
        print("⚠️ No candle data received.")

    print("🔄 System Ready. Waiting for Strategy Implementation...")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    start_bot()
