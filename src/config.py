import os

class Config:
    TG_TOKEN = os.getenv('TG_TOKEN')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')
    DERIV_APP_ID = os.getenv('DERIV_APP_ID', '1089')
    DERIV_PAT_DEMO = os.getenv('DERIV_PAT_DEMO')
    
    SYMBOL = 'R_100'
    GRANULARITY = 60
    HISTORY_COUNT = 50
    TRADE_STAKE = 1.0
    
    @staticmethod
    def validate():
        errors = []
        if not Config.TG_TOKEN: errors.append("TG_TOKEN")
        if not Config.TG_CHAT_ID: errors.append("TG_CHAT_ID")
        if not Config.DERIV_PAT_DEMO: errors.append("DERIV_PAT_DEMO")
        if errors: raise ValueError(f"Missing secrets: {errors}")
        return True
