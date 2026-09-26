import asyncio
import websockets
import json
from src.config import Config

class DerivConnector:
    def __init__(self):
        self.ws = None
        
    async def connect(self):
        url = f"wss://ws.derivws.com/websockets/v3?app_id={Config.DERIV_APP_ID}"
        try:
            # مهلة 15 ثانية للاتصال الأولي
            self.ws = await asyncio.wait_for(websockets.connect(url), timeout=15)
            print("✅ WebSocket Connected.")
            await self.authorize()
        except asyncio.TimeoutError:
            raise Exception("❌ Timeout: Server did not respond to connection request.")
        except Exception as e:
            raise Exception(f"❌ Connection Failed: {str(e)}")
            
    async def authorize(self):
        msg = {"authorize": Config.DERIV_PAT_DEMO}
        await self._send(msg)
        res = await self._receive(timeout=10) # مهلة 10 ثوانٍ للرد
        
        if 'error' in res:
            raise Exception(f"Auth Error: {res['error']['message']}")
        
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
            raise Exception("❌ Timeout: No response received from server within limit.")
        
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
        res = await self._receive(timeout=15) # مهلة أطول لجلب البيانات
        
        if 'error' in res:
             raise Exception(f"Data Fetch Error: {res['error']['message']}")
             
        return res.get('candles', [])

    async def close(self):
        if self.ws:
            await self.ws.close()
