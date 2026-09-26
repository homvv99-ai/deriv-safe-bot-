import asyncio
import websockets
import json
from src.config import Config

class DerivConnector:
    def __init__(self):
        self.ws = None
        
    async def connect(self):
        # استخدام العنوان الرسمي المخصص للتطبيقات الخارجية مع إضافة Origin Header
        url = f"wss://ws.binaryws.com/websockets/v3?app_id={Config.DERIV_APP_ID}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://app.deriv.com"
        }
        
        try:
            print(f"🔌 Attempting connection to {url}...")
            self.ws = await asyncio.wait_for(
                websockets.connect(url, additional_headers=headers), 
                timeout=15
            )
            print("✅ WebSocket Connected Successfully.")
            await self.authorize()
        except asyncio.TimeoutError:
            raise Exception("❌ Timeout: Server did not respond within 15 seconds.")
        except Exception as e:
            raise Exception(f"❌ Connection Failed: {str(e)}")
            
    async def authorize(self):
        msg = {"authorize": Config.DERIV_PAT_DEMO}
        await self._send(msg)
        res = await self._receive(timeout=10) 
        
        if 'error' in res:
            error_msg = res['error'].get('message', 'Unknown Error')
            raise Exception(f"Auth Error: {error_msg}")
        
        login_id = res.get('authorize', {}).get('loginid')
        currency = res.get('authorize', {}).get('currency')
        balance = res.get('authorize', {}).get('balance')
        print(f"🔐 Authorized User ID: {login_id}")
        print(f"💰 Balance: {balance} {currency}")
        
    async def _send(self, data_dict):
        if self.ws:
            await self.ws.send(json.dumps(data_dict))
            
    async def _receive(self, timeout=10):
        if not self.ws: return {}
        try:
            raw = await asyncio.wait_for(self.ws.recv(), timeout=timeout)
            return json.loads(raw)
        except asyncio.TimeoutError:
            raise Exception("❌ Timeout: No response received from server.")
        
    async def get_latest_candles(self, count=None):
        cnt = count or Config.HISTORY_COUNT
        msg = {
            "ticks_history": Config.SYMBOL,
            "style": "candles",
            "granularity": Config.GRANULARITY,
            "count": cnt,
            "end": "latest"
        }
        await self._send(msg)
        res = await self._receive(timeout=15) 
        
        if 'error' in res:
             raise Exception(f"Data Fetch Error: {res['error']['message']}")
             
        return res.get('candles', [])

    async def close(self):
        if self.ws:
            await self.ws.close()
