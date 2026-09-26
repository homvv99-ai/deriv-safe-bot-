import websocket
import json
from src.config import Config

class DerivConnector:
    def __init__(self):
        self.ws = None
        
    def connect(self):
        url = f"wss://ws.derivws.com/websockets/v3?app_id={Config.DERIV_APP_ID}"
        try:
            self.ws = websocket.create_connection(url, timeout=10)
            self.authorize()
            print("✅ Connected to Deriv.")
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            
    def authorize(self):
        msg = {"authorize": Config.DERIV_PAT_DEMO}
        self._send(msg)
        res = self._receive()
        if 'error' in res:
            raise Exception(f"Auth Error: {res['error']['message']}")
        print(f"Authorized User ID: {res.get('authorize', {}).get('loginid')}")
        
    def _send(self, data_dict):
        if self.ws:
            self.ws.send(json.dumps(data_dict))
            
    def _receive(self):
        if self.ws:
            raw = self.ws.recv()
            return json.loads(raw)
        return {}
        
    def get_latest_candles(self, count=None):
        cnt = count or Config.HISTORY_COUNT
        msg = {
            "ticks_history": Config.SYMBOL,
            "style": "candles",
            "granularity": Config.GRANULARITY,
            "count": cnt,
            "end": "latest"
        }
        self._send(msg)
        res = self._receive()
        return res.get('candles', [])
