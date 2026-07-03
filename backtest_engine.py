"""
LYFE - Backtesting Engine
Professional backtesting with multiple strategies
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional
from enum import Enum
import json


class TradeDirection(Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradeStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    SL = "STOP_LOSS"
    TP = "TAKE_PROFIT"


@dataclass
class Trade:
    """Individual trade record"""
    id: int
    symbol: str
    direction: TradeDirection
    entry_price: float
    volume: float
    entry_time: datetime
    sl: Optional[float] = None
    tp: Optional[float] = None
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    profit: float = 0.0
    pips: float = 0.0
    status: TradeStatus = TradeStatus.OPEN
    commission: float = 0.0
    swap: float = 0.0
    strategy: str = ""


@dataclass
class BacktestResult:
    """Complete backtest results"""
    strategy_name: str
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    initial_balance: float
    final_balance: float
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    sharpe_ratio: float = 0.0
    total_return: float = 0.0
    total_return_pct: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_trade: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    expectancy: float = 0.0
    trades: List[Trade] = field(default_factory=list)
    equity_curve: List[Dict] = field(default_factory=list)
    monthly_returns: Dict = field(default_factory=dict)


class BacktestEngine:
    """Professional backtesting engine"""
    
    def __init__(self):
        self.initial_balance = 10000.0
        self.leverage = 100
        self.commission_per_lot = 3.5
        self.spread_pips = 1.5
        self.risk_per_trade = 0.02
        
        # Asset specifications
        self.specs = {
            "EURUSD": {"pip": 0.0001, "contract": 100000, "spread": 1.2},
            "GBPUSD": {"pip": 0.0001, "contract": 100000, "spread": 1.5},
            "USDJPY": {"pip": 0.01, "contract": 100000, "spread": 1.5},
            "AUDUSD": {"pip": 0.0001, "contract": 100000, "spread": 1.6},
            "USDCAD": {"pip": 0.0001, "contract": 100000, "spread": 1.8},
            "XAUUSD": {"pip": 0.1, "contract": 100, "spread": 2.5},
            "BTCUSD": {"pip": 1.0, "contract": 1, "spread": 15.0},
            "NAS100": {"pip": 1.0, "contract": 10, "spread": 2.0},
            "R_10": {"pip": 0.001, "contract": 1, "spread": 0.5},
            "R_25": {"pip": 0.001, "contract": 1, "spread": 0.5},
            "R_50": {"pip": 0.001, "contract": 1, "spread": 0.5},
            "R_75": {"pip": 0.001, "contract": 1, "spread": 0.5},
            "R_100": {"pip": 0.001, "contract": 1, "spread": 0.5},
        }
        
        # Strategy registry
        self.strategies = {
            "ema_crossover": self.ema_crossover_strategy,
            "rsi_divergence": self.rsi_divergence_strategy,
            "bollinger_bounce": self.bollinger_bounce_strategy,
            "macd_momentum": self.macd_momentum_strategy,
            "breakout": self.breakout_strategy,
            "smart_money": self.smart_money_concepts_strategy,
        }
    
    def get_strategies(self):
        """Get available strategy names"""
        return list(self.strategies.keys())
    
    def run_backtest(self, strategy_name: str, data: pd.DataFrame, 
                     symbol: str = "EURUSD", timeframe: str = "1H",
                     **kwargs) -> BacktestResult:
        """Run backtest with specified strategy"""
        
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy_func = self.strategies[strategy_name]
        
        # Initialize backtest state
        balance = self.initial_balance
        equity = balance
        trades = []
        equity_curve = []
        trade_id = 0
        
        spec = self.specs.get(symbol, {"pip": 0.0001, "contract": 100000, "spread": 1.5})
        pip_value = spec["pip"]
        contract_size = spec["contract"]
        spread = spec["spread"] * pip_value
        
        # Calculate indicators
        data = strategy_func(data, mode="indicators")
        
        # Iterate through data
        for i in range(50, len(data) - 1):
            row = data.iloc[i]
            next_row = data.iloc[i + 1]
            
            # Check for signals
            signal = strategy_func(data.iloc[:i+1], mode="signal", current=row)
            
            if signal and signal.get("action") in ["BUY", "SELL"]:
                trade_id += 1
                direction = TradeDirection.BUY if signal["action"] == "BUY" else TradeDirection.SELL
                
                # Calculate position size
                risk_amount = balance * self.risk_per_trade
                sl_distance = abs(signal.get("entry", row["close"]) - signal.get("sl", row["close"]))
                if sl_distance == 0:
                    sl_distance = 10 * pip_value
                
                position_size = risk_amount / (sl_distance * contract_size / pip_value)
                position_size = min(position_size, balance * self.leverage / (row["close"] * contract_size))
                
                # Apply spread
                if direction == TradeDirection.BUY:
                    entry = row["close"] + spread / 2
                else:
                    entry = row["close"] - spread / 2
                
                # Create trade
                trade = Trade(
                    id=trade_id,
                    symbol=symbol,
                    direction=direction,
                    entry_price=entry,
                    volume=position_size,
                    entry_time=row.name if isinstance(row.name, datetime) else datetime.now(),
                    sl=signal.get("sl"),
                    tp=signal.get("tp"),
                    commission=self.commission_per_lot * position_size * 2,
                    strategy=strategy_name
                )
                
                # Simulate trade outcome
                trade = self._simulate_trade(trade, data.iloc[i+1:], pip_value, contract_size)
                
                # Update balance
                balance += trade.profit - trade.commission - trade.swap
                trades.append(trade)
                
                # Record equity
                equity_curve.append({
                    "time": trade.exit_time.isoformat() if trade.exit_time else "",
                    "equity": balance
                })
        
        # Calculate results
        return self._calculate_results(trades, equity_curve, strategy_name, symbol, timeframe)
    
    def _simulate_trade(self, trade: Trade, future_data: pd.DataFrame, 
                        pip_value: float, contract_size: float) -> Trade:
        """Simulate trade outcome"""
        
        for _, row in future_data.iterrows():
            high, low = row["high"], row["low"]
            
            if trade.direction == TradeDirection.BUY:
                # Check SL
                if trade.sl and low <= trade.sl:
                    trade.exit_price = trade.sl
                    trade.exit_time = row.name if isinstance(row.name, datetime) else datetime.now()
                    trade.pips = (trade.exit_price - trade.entry_price) / pip_value
                    trade.profit = trade.pips * pip_value * contract_size * trade.volume
                    trade.status = TradeStatus.SL
                    return trade
                
                # Check TP
                if trade.tp and high >= trade.tp:
                    trade.exit_price = trade.tp
                    trade.exit_time = row.name if isinstance(row.name, datetime) else datetime.now()
                    trade.pips = (trade.exit_price - trade.entry_price) / pip_value
                    trade.profit = trade.pips * pip_value * contract_size * trade.volume
                    trade.status = TradeStatus.TP
                    return trade
            
            else:  # SELL
                # Check SL
                if trade.sl and high >= trade.sl:
                    trade.exit_price = trade.sl
                    trade.exit_time = row.name if isinstance(row.name, datetime) else datetime.now()
                    trade.pips = (trade.entry_price - trade.exit_price) / pip_value
                    trade.profit = trade.pips * pip_value * contract_size * trade.volume
                    trade.status = TradeStatus.SL
                    return trade
                
                # Check TP
                if trade.tp and low <= trade.tp:
                    trade.exit_price = trade.tp
                    trade.exit_time = row.name if isinstance(row.name, datetime) else datetime.now()
                    trade.pips = (trade.entry_price - trade.exit_price) / pip_value
                    trade.profit = trade.pips * pip_value * contract_size * trade.volume
                    trade.status = TradeStatus.TP
                    return trade
        
        # Close at last available price if not hit SL/TP
        if len(future_data) > 0:
            last = future_data.iloc[-1]
            trade.exit_price = last["close"]
            trade.exit_time = last.name if isinstance(last.name, datetime) else datetime.now()
            
            if trade.direction == TradeDirection.BUY:
                trade.pips = (trade.exit_price - trade.entry_price) / pip_value
            else:
                trade.pips = (trade.entry_price - trade.exit_price) / pip_value
            
            trade.profit = trade.pips * pip_value * contract_size * trade.volume
            trade.status = TradeStatus.CLOSED
        
        return trade
    
    def _calculate_results(self, trades: List[Trade], equity_curve: List[Dict],
                          strategy_name: str, symbol: str, timeframe: str) -> BacktestResult:
        """Calculate final backtest metrics"""
        
        if not trades:
            return BacktestResult(
                strategy_name=strategy_name, symbol=symbol, timeframe=timeframe,
                start_date="", end_date="", initial_balance=self.initial_balance,
                final_balance=self.initial_balance
            )
        
        winning_trades = [t for t in trades if t.profit > 0]
        losing_trades = [t for t in trades if t.profit <= 0]
        
        total_profit = sum(t.profit for t in trades)
        gross_profit = sum(t.profit for t in winning_trades) if winning_trades else 0
        gross_loss = abs(sum(t.profit for t in losing_trades)) if losing_trades else 1
        
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Calculate max drawdown
        peak = self.initial_balance
        max_dd = 0
        max_dd_pct = 0
        running_balance = self.initial_balance
        
        for trade in trades:
            running_balance += trade.profit - trade.commission
            if running_balance > peak:
                peak = running_balance
            dd = peak - running_balance
            dd_pct = (dd / peak) * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd
            if dd_pct > max_dd_pct:
                max_dd_pct = dd_pct
        
        # Sharpe ratio
        returns = [t.profit for t in trades]
        avg_return = np.mean(returns) if returns else 0
        std_return = np.std(returns) if returns else 1
        sharpe = (avg_return / std_return) * np.sqrt(252) if std_return > 0 else 0
        
        # Expectancy
        avg_win = np.mean([t.profit for t in winning_trades]) if winning_trades else 0
        avg_loss = abs(np.mean([t.profit for t in losing_trades])) if losing_trades else 0
        expectancy = (win_rate / 100 * avg_win) - ((1 - win_rate / 100) * avg_loss)
        
        return BacktestResult(
            strategy_name=strategy_name,
            symbol=symbol,
            timeframe=timeframe,
            start_date=trades[0].entry_time.strftime("%Y-%m-%d") if trades else "",
            end_date=trades[-1].exit_time.strftime("%Y-%m-%d") if trades and trades[-1].exit_time else "",
            initial_balance=self.initial_balance,
            final_balance=self.initial_balance + total_profit,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            win_rate=round(win_rate, 2),
            profit_factor=round(profit_factor, 2),
            max_drawdown=round(max_dd, 2),
            max_drawdown_pct=round(max_dd_pct, 2),
            sharpe_ratio=round(sharpe, 2),
            total_return=round(total_profit, 2),
            total_return_pct=round((total_profit / self.initial_balance) * 100, 2),
            avg_win=round(avg_win, 2),
            avg_loss=round(avg_loss, 2),
            avg_trade=round(np.mean(returns), 2) if returns else 0,
            largest_win=round(max((t.profit for t in winning_trades), default=0), 2),
            largest_loss=round(min((t.profit for t in losing_trades), default=0), 2),
            expectancy=round(expectancy, 2),
            trades=trades,
            equity_curve=equity_curve
        )
    
    # ========== Strategy Implementations ==========
    
    def ema_crossover_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """EMA Crossover Strategy"""
        if mode == "indicators":
            data["ema_fast"] = data["close"].ewm(span=12).mean()
            data["ema_slow"] = data["close"].ewm(span=26).mean()
            data["rsi"] = self._calculate_rsi(data["close"])
            return data
        
        elif mode == "signal" and current is not None:
            if len(data) < 3:
                return None
            
            prev = data.iloc[-2]
            
            # Bullish cross
            if prev["ema_fast"] <= prev["ema_slow"] and current["ema_fast"] > current["ema_slow"]:
                if current["rsi"] > 50 and current["rsi"] < 80:
                    return {
                        "action": "BUY",
                        "entry": current["close"],
                        "sl": current["low"] - 0.0005,
                        "tp": current["close"] + (current["close"] - current["low"]) * 2
                    }
            
            # Bearish cross
            if prev["ema_fast"] >= prev["ema_slow"] and current["ema_fast"] < current["ema_slow"]:
                if current["rsi"] < 50 and current["rsi"] > 20:
                    return {
                        "action": "SELL",
                        "entry": current["close"],
                        "sl": current["high"] + 0.0005,
                        "tp": current["close"] - (current["high"] - current["close"]) * 2
                    }
        
        return None
    
    def rsi_divergence_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """RSI Divergence Strategy"""
        if mode == "indicators":
            data["rsi"] = self._calculate_rsi(data["close"], 14)
            data["ema_50"] = data["close"].ewm(span=50).mean()
            return data
        
        elif mode == "signal" and current is not None:
            if len(data) < 20:
                return None
            
            # Look for bullish divergence
            price_lows = data["low"].tail(10)
            rsi_lows = data["rsi"].tail(10)
            
            if price_lows.iloc[-1] < price_lows.iloc[-5] and rsi_lows.iloc[-1] > rsi_lows.iloc[-5]:
                if current["rsi"] < 40:
                    return {
                        "action": "BUY",
                        "entry": current["close"],
                        "sl": current["low"] - 0.001,
                        "tp": current["close"] + 0.003
                    }
            
            # Look for bearish divergence
            price_highs = data["high"].tail(10)
            rsi_highs = data["rsi"].tail(10)
            
            if price_highs.iloc[-1] > price_highs.iloc[-5] and rsi_highs.iloc[-1] < rsi_highs.iloc[-5]:
                if current["rsi"] > 60:
                    return {
                        "action": "SELL",
                        "entry": current["close"],
                        "sl": current["high"] + 0.001,
                        "tp": current["close"] - 0.003
                    }
        
        return None
    
    def bollinger_bounce_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """Bollinger Bands Bounce Strategy"""
        if mode == "indicators":
            data["sma_20"] = data["close"].rolling(20).mean()
            std = data["close"].rolling(20).std()
            data["bb_upper"] = data["sma_20"] + 2 * std
            data["bb_lower"] = data["sma_20"] - 2 * std
            data["rsi"] = self._calculate_rsi(data["close"])
            return data
        
        elif mode == "signal" and current is not None:
            if current["close"] <= current["bb_lower"] and current["rsi"] < 35:
                return {
                    "action": "BUY",
                    "entry": current["close"],
                    "sl": current["low"] - 0.001,
                    "tp": current["sma_20"]
                }
            
            if current["close"] >= current["bb_upper"] and current["rsi"] > 65:
                return {
                    "action": "SELL",
                    "entry": current["close"],
                    "sl": current["high"] + 0.001,
                    "tp": current["sma_20"]
                }
        
        return None
    
    def macd_momentum_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """MACD Momentum Strategy"""
        if mode == "indicators":
            ema_12 = data["close"].ewm(span=12).mean()
            ema_26 = data["close"].ewm(span=26).mean()
            data["macd"] = ema_12 - ema_26
            data["macd_signal"] = data["macd"].ewm(span=9).mean()
            data["macd_hist"] = data["macd"] - data["macd_signal"]
            return data
        
        elif mode == "signal" and current is not None:
            if len(data) < 3:
                return None
            
            prev = data.iloc[-2]
            
            # MACD crossover
            if prev["macd"] <= prev["macd_signal"] and current["macd"] > current["macd_signal"]:
                if current["macd_hist"] > 0:
                    return {
                        "action": "BUY",
                        "entry": current["close"],
                        "sl": current["low"] - 0.001,
                        "tp": current["close"] + 0.003
                    }
            
            if prev["macd"] >= prev["macd_signal"] and current["macd"] < current["macd_signal"]:
                if current["macd_hist"] < 0:
                    return {
                        "action": "SELL",
                        "entry": current["close"],
                        "sl": current["high"] + 0.001,
                        "tp": current["close"] - 0.003
                    }
        
        return None
    
    def breakout_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """Breakout Strategy"""
        if mode == "indicators":
            data["atr"] = self._calculate_atr(data)
            data["resistance"] = data["high"].rolling(20).max()
            data["support"] = data["low"].rolling(20).min()
            data["volume_sma"] = data.get("volume", data["close"] * 0).rolling(20).mean()
            return data
        
        elif mode == "signal" and current is not None:
            if len(data) < 5:
                return None
            
            prev = data.iloc[-2]
            
            # Resistance breakout
            if prev["high"] < prev["resistance"] and current["close"] > current["resistance"]:
                return {
                    "action": "BUY",
                    "entry": current["close"],
                    "sl": current["support"],
                    "tp": current["close"] + (current["close"] - current["support"]) * 1.5
                }
            
            # Support breakdown
            if prev["low"] > prev["support"] and current["close"] < current["support"]:
                return {
                    "action": "SELL",
                    "entry": current["close"],
                    "sl": current["resistance"],
                    "tp": current["close"] - (current["resistance"] - current["close"]) * 1.5
                }
        
        return None
    
    def smart_money_concepts_strategy(self, data: pd.DataFrame, mode="indicators", current=None):
        """Smart Money Concepts Strategy"""
        if mode == "indicators":
            data["swing_high"] = data["high"].rolling(5).max() == data["high"]
            data["swing_low"] = data["low"].rolling(5).min() == data["low"]
            data["fvg"] = ((data["low"] > data["high"].shift(2)) | 
                          (data["high"] < data["low"].shift(2))).astype(int)
            data["ob_bull"] = ((data["close"] > data["open"]) & 
                              (data["low"] < data["low"].shift(1))).astype(int)
            data["ob_bear"] = ((data["close"] < data["open"]) & 
                              (data["high"] > data["high"].shift(1))).astype(int)
            return data
        
        elif mode == "signal" and current is not None:
            if len(data) < 10:
                return None
            
            # Bullish order block
            if current["ob_bull"] and current["close"] > data["close"].tail(5).mean():
                return {
                    "action": "BUY",
                    "entry": current["close"],
                    "sl": current["low"] - 0.001,
                    "tp": current["close"] + 0.004
                }
            
            # Bearish order block
            if current["ob_bear"] and current["close"] < data["close"].tail(5).mean():
                return {
                    "action": "SELL",
                    "entry": current["close"],
                    "sl": current["high"] + 0.001,
                    "tp": current["close"] - 0.004
                }
        
        return None
    
    # ========== Technical Indicators ==========
    
    @staticmethod
    def _calculate_rsi(prices, period=14):
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def _calculate_atr(data, period=14):
        """Calculate Average True Range"""
        high_low = data["high"] - data["low"]
        high_close = abs(data["high"] - data["close"].shift())
        low_close = abs(data["low"] - data["close"].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean()
