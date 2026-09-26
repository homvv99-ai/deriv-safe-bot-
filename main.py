import sys
import os
import asyncio
import time

sys.path.append(os.path.abspath('./src'))

try:
    from src.config import Config
    from src.connector import DerivConnector
except ImportError as e:
    print(f"Critical Import Error: {e}")
    sys.exit(1)

async def start_bot_async():
    print("🚀 Starting Deriv Pro Trader Engine (Async Mode)...")
    
    try:
        Config.validate()
        print("⚙️ Configuration Validated.")
    except ValueError as ve:
        print(f"❌ Stop! {ve}")
        return

    connector = DerivConnector()
    
    try:
        # 1. Connect & Authorize
        await connector.connect()
        
        # 2. Fetch Initial Data Test
        print("📊 Fetching initial market data...")
        candles = await connector.get_latest_candles(count=5)
        
        if candles:
            last_close = candles[-1]['close']
            print(f"✅ Market Data Received. Last Close Price: {last_close}")
        else:
            print("⚠️ No candle data received.")
            
    except Exception as e:
        print(f"💥 Critical Runtime Error: {e}")
    finally:
        await connector.close()
        print("🔒 Connection Closed Safely.")

def start_bot():
    asyncio.run(start_bot_async())

if __name__ == "__main__":
    start_bot()
