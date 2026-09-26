import os

class Config:
    # --- Telegram Settings ---
    TG_TOKEN = os.getenv('TG_TOKEN')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')
    
    # --- Deriv API Settings ---
    DERIV_APP_ID = os.getenv('DERIV_APP_ID', '1089') # Default public app id
    DERIV_PAT_DEMO = os.getenv('DERIV_PAT_DEMO')     # Token for Demo Account
    
    # --- Trading Parameters ---
    SYMBOL = 'R_100'          # Volatility Index 100
    GRANULARITY = 60          # Candle duration in seconds (1 minute)
    HISTORY_COUNT = 50        # Number of candles to analyze per tick
    TRADE_STAKE = 1.0         # Default stake amount
    
    @staticmethod
    def validate():
        """Check if critical secrets are present before starting."""
        errors = []
        if not Config.TG_TOKEN: errors.append("TG_TOKEN missing")
        if not Config.TG_CHAT_ID: errors.append("TG_CHAT_ID missing")
        if not Config.DERIV_PAT_DEMO: errors.append("DERIV_PAT_DEMO missing")
        
        if errors:
            raise ValueError(f"Configuration Error: {', '.join(errors)}")
        return True
