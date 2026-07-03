"""
LYFE - Deriv API Integration
WebSocket connection for real-time trading data and execution
Supports both public Deriv API and custom API keys
"""

import json
import threading
import websocket
import requests
from datetime import datetime
from typing import Callable, Optional, Dict, List


class DerivAPI:
    """Deriv WebSocket API client for trading"""
    
    WEBSOCKET_URL = "wss://ws.derivws.com/websockets/v3?app_id=1089"
    
    def __init__(self):
        self.ws = None
        self.connected = False
        self.api_token = None
        self.app_id = "1089"  # Default public app ID
        self.req_id = 0
        self.callbacks = {}
        self.price_callbacks = []
        self.connection_callbacks = []
        self.thread = None
        self.lock = threading.Lock()
        
        # Market data cache
        self.price_cache = {}
        self.account_info = {}
        
        # Supported symbols with their Deriv IDs
        self.symbols = {
            "R_10": {"name": "Volatility 10 Index", "category": "synthetic"},
            "R_25": {"name": "Volatility 25 Index", "category": "synthetic"},
            "R_50": {"name": "Volatility 50 Index", "category": "synthetic"},
            "R_75": {"name": "Volatility 75 Index", "category": "synthetic"},
            "R_100": {"name": "Volatility 100 Index", "category": "synthetic"},
            "1HZ10V": {"name": "Volatility 10 (1s)", "category": "synthetic"},
            "1HZ25V": {"name": "Volatility 25 (1s)", "category": "synthetic"},
            "1HZ50V": {"name": "Volatility 50 (1s)", "category": "synthetic"},
            "1HZ75V": {"name": "Volatility 75 (1s)", "category": "synthetic"},
            "1HZ100V": {"name": "Volatility 100 (1s)", "category": "synthetic"},
            "frxEURUSD": {"name": "EUR/USD", "category": "forex"},
            "frxGBPUSD": {"name": "GBP/USD", "category": "forex"},
            "frxUSDJPY": {"name": "USD/JPY", "category": "forex"},
            "frxAUDUSD": {"name": "AUD/USD", "category": "forex"},
            "frxUSDCAD": {"name": "USD/CAD", "category": "forex"},
            "frxXAUUSD": {"name": "Gold/USD", "category": "commodity"},
            "frxXAGUSD": {"name": "Silver/USD", "category": "commodity"},
            "OTC_AAPL": {"name": "Apple Inc.", "category": "stock"},
            "OTC_GOOGL": {"name": "Alphabet Inc.", "category": "stock"},
            "OTC_TSLA": {"name": "Tesla Inc.", "category": "stock"},
            "OTC_AMZN": {"name": "Amazon.com", "category": "stock"},
        }
    
    def connect(self, api_token=None, app_id=None):
        """Connect to Deriv WebSocket API"""
        if app_id:
            self.app_id = app_id
        if api_token:
            self.api_token = api_token
        
        url = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"
        
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()
    
    def disconnect(self):
        """Disconnect from API"""
        self.connected = False
        if self.ws:
            self.ws.close()
    
    def _on_open(self, ws):
        """Handle connection open"""
        self.connected = True
        
        # Authenticate if token provided
        if self.api_token:
            self._send({
                "authorize": self.api_token
            })
        
        # Subscribe to tick streams for all symbols
        for symbol in self.symbols.keys():
            self.subscribe_ticks(symbol)
        
        # Notify callbacks
        for cb in self.connection_callbacks:
            cb(True)
    
    def _on_message(self, ws, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            
            # Handle tick data
            if "tick" in data:
                tick = data["tick"]
                symbol = tick.get("symbol")
                price = tick.get("quote")
                
                if symbol and price:
                    self.price_cache[symbol] = {
                        "price": price,
                        "time": datetime.now().isoformat(),
                        "epoch": tick.get("epoch")
                    }
                    
                    # Notify price subscribers
                    for cb in self.price_callbacks:
                        cb(symbol, price)
            
            # Handle authorization response
            if "authorize" in data:
                self.account_info = data.get("authorize", {})
            
            # Handle proposal/proposal_open_contract
            if "proposal" in data:
                req_id = data.get("req_id")
                if req_id and req_id in self.callbacks:
                    self.callbacks[req_id](data["proposal"])
                    del self.callbacks[req_id]
            
            # Handle buy response
            if "buy" in data:
                req_id = data.get("req_id")
                if req_id and req_id in self.callbacks:
                    self.callbacks[req_id](data["buy"])
                    del self.callbacks[req_id]
            
            # Handle error
            if "error" in data:
                error = data["error"]
                print(f"Deriv API Error: {error.get('message', 'Unknown error')}")
        
        except Exception as e:
            print(f"Message handling error: {e}")
    
    def _on_error(self, ws, error):
        """Handle errors"""
        self.connected = False
        print(f"Deriv WebSocket Error: {error}")
        for cb in self.connection_callbacks:
            cb(False)
    
    def _on_close(self, ws, close_status, close_msg):
        """Handle connection close"""
        self.connected = False
        for cb in self.connection_callbacks:
            cb(False)
    
    def _send(self, data):
        """Send message to WebSocket"""
        if self.ws and self.connected:
            self.ws.send(json.dumps(data))
    
    def _get_req_id(self):
        """Get next request ID"""
        with self.lock:
            self.req_id += 1
            return self.req_id
    
    # ========== Public API Methods ==========
    
    def subscribe_ticks(self, symbol):
        """Subscribe to tick stream"""
        self._send({
            "ticks": symbol,
            "subscribe": 1,
            "req_id": self._get_req_id()
        })
    
    def unsubscribe_ticks(self, symbol):
        """Unsubscribe from tick stream"""
        self._send({
            "ticks": symbol,
            "subscribe": 0,
            "req_id": self._get_req_id()
        })
    
    def get_price(self, symbol):
        """Get current price for symbol"""
        return self.price_cache.get(symbol, {}).get("price")
    
    def get_all_prices(self):
        """Get all cached prices"""
        return self.price_cache
    
    def on_price_update(self, callback):
        """Register price update callback"""
        self.price_callbacks.append(callback)
    
    def on_connection_change(self, callback):
        """Register connection change callback"""
        self.connection_callbacks.append(callback)
    
    # ========== Trading Methods (require auth) ==========
    
    def get_balance(self):
        """Get account balance"""
        if not self.connected:
            return None
        
        req_id = self._get_req_id()
        self._send({
            "balance": 1,
            "subscribe": 1,
            "req_id": req_id
        })
    
    def buy_contract(self, symbol, contract_type, amount, duration, duration_unit="t", callback=None):
        """Buy a contract"""
        if not self.connected:
            return None
        
        req_id = self._get_req_id()
        
        proposal = {
            "proposal": 1,
            "amount": amount,
            "basis": "stake",
            "contract_type": contract_type,  # CALL or PUT
            "currency": "USD",
            "duration": duration,
            "duration_unit": duration_unit,
            "symbol": symbol,
            "req_id": req_id
        }
        
        if callback:
            self.callbacks[req_id] = callback
        
        self._send(proposal)
        return req_id
    
    def execute_buy(self, proposal_id, price, callback=None):
        """Execute buy from proposal"""
        req_id = self._get_req_id()
        
        if callback:
            self.callbacks[req_id] = callback
        
        self._send({
            "buy": proposal_id,
            "price": price,
            "req_id": req_id
        })
        
        return req_id
    
    def get_portfolio(self):
        """Get open positions"""
        req_id = self._get_req_id()
        self._send({
            "portfolio": 1,
            "req_id": req_id
        })
    
    def sell_contract(self, contract_id, price=0):
        """Sell/close a contract"""
        req_id = self._get_req_id()
        self._send({
            "sell": contract_id,
            "price": price,
            "req_id": req_id
        })
    
    def get_trading_times(self):
        """Get trading times for all symbols"""
        req_id = self._get_req_id()
        self._send({
            "trading_times": "today",
            "req_id": req_id
        })
    
    # ========== Utility Methods ==========
    
    def is_connected(self):
        """Check if connected"""
        return self.connected
    
    def get_account_info(self):
        """Get account information"""
        return self.account_info
    
    def get_symbols(self, category=None):
        """Get available symbols"""
        if category:
            return {k: v for k, v in self.symbols.items() if v["category"] == category}
        return self.symbols
