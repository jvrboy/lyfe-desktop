"""
LYFE - Database Manager
SQLite local storage for signals, trades, settings, and user data
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock


class DatabaseManager:
    """Thread-safe SQLite database manager"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            app_dir = Path.home() / ".lyfe"
            app_dir.mkdir(exist_ok=True)
            db_path = app_dir / "lyfe.db"
        
        self.db_path = str(db_path)
        self.lock = Lock()
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Signals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS signals (
                    id TEXT PRIMARY KEY,
                    pair TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    entry REAL NOT NULL,
                    sl REAL,
                    tp REAL,
                    confidence INTEGER,
                    rr REAL,
                    strategies TEXT,
                    status TEXT DEFAULT 'ACTIVE',
                    pnl REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id TEXT PRIMARY KEY,
                    ticket INTEGER,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    volume REAL NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    sl REAL,
                    tp REAL,
                    commission REAL DEFAULT 0,
                    swap REAL DEFAULT 0,
                    profit REAL DEFAULT 0,
                    status TEXT DEFAULT 'OPEN',
                    open_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    close_time TIMESTAMP,
                    strategy TEXT,
                    notes TEXT
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # API credentials (encrypted storage placeholder)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_credentials (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    api_key TEXT,
                    api_secret TEXT,
                    account_id TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Trade journal
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal (
                    id TEXT PRIMARY KEY,
                    trade_id TEXT,
                    entry TEXT,
                    lessons TEXT,
                    emotions TEXT,
                    setup_quality INTEGER,
                    result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trade_id) REFERENCES trades(id)
                )
            ''')
            
            # Market data cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_data (
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    timestamp TIMESTAMP,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    PRIMARY KEY (symbol, timeframe, timestamp)
                )
            ''')
            
            # News items
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    source TEXT,
                    content TEXT,
                    currency TEXT,
                    impact TEXT,
                    published_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Economic calendar
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS economic_calendar (
                    id TEXT PRIMARY KEY,
                    time TEXT,
                    currency TEXT,
                    event TEXT,
                    impact TEXT,
                    actual TEXT,
                    forecast TEXT,
                    previous TEXT,
                    date TEXT
                )
            ''')
            
            # LLM Models
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS llm_models (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    path TEXT,
                    size_gb REAL,
                    parameters TEXT,
                    quantization TEXT,
                    is_loaded INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Backtest results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backtest_results (
                    id TEXT PRIMARY KEY,
                    strategy_name TEXT,
                    symbol TEXT,
                    timeframe TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    total_trades INTEGER,
                    win_rate REAL,
                    profit_factor REAL,
                    max_drawdown REAL,
                    sharpe_ratio REAL,
                    net_profit REAL,
                    equity_curve TEXT,
                    trades_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Performance metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    total_pnl REAL,
                    win_count INTEGER,
                    loss_count INTEGER,
                    total_trades INTEGER,
                    win_rate REAL,
                    balance REAL,
                    equity REAL
                )
            ''')
            
            conn.commit()
            conn.close()
    
    # ========== Signals ==========
    
    def save_signal(self, signal_data):
        """Save trading signal"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            signal_id = signal_data.get('id', str(uuid.uuid4()))
            cursor.execute('''
                INSERT OR REPLACE INTO signals 
                (id, pair, direction, entry, sl, tp, confidence, rr, 
                 strategies, status, pnl, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                signal_id, signal_data.get('pair'), signal_data.get('direction'),
                signal_data.get('entry'), signal_data.get('sl'),
                signal_data.get('tp'), signal_data.get('confidence'),
                signal_data.get('rr'), json.dumps(signal_data.get('strategies', [])),
                signal_data.get('status', 'ACTIVE'), signal_data.get('pnl'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return signal_id
    
    def get_signals(self, status=None, limit=100):
        """Get signals with optional filter"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT * FROM signals 
                    WHERE status = ? 
                    ORDER BY created_at DESC LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT * FROM signals 
                    ORDER BY created_at DESC LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def update_signal_status(self, signal_id, status, pnl=None):
        """Update signal status"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if pnl is not None:
                cursor.execute('''
                    UPDATE signals SET status = ?, pnl = ?, updated_at = ?
                    WHERE id = ?
                ''', (status, pnl, datetime.now().isoformat(), signal_id))
            else:
                cursor.execute('''
                    UPDATE signals SET status = ?, updated_at = ?
                    WHERE id = ?
                ''', (status, datetime.now().isoformat(), signal_id))
            
            conn.commit()
            conn.close()
    
    # ========== Trades ==========
    
    def save_trade(self, trade_data):
        """Save trade to database"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            trade_id = trade_data.get('id', str(uuid.uuid4()))
            cursor.execute('''
                INSERT OR REPLACE INTO trades
                (id, ticket, symbol, direction, volume, entry_price, exit_price,
                 sl, tp, commission, swap, profit, status, open_time, close_time,
                 strategy, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_id, trade_data.get('ticket'), trade_data.get('symbol'),
                trade_data.get('direction'), trade_data.get('volume'),
                trade_data.get('entry_price'), trade_data.get('exit_price'),
                trade_data.get('sl'), trade_data.get('tp'),
                trade_data.get('commission', 0), trade_data.get('swap', 0),
                trade_data.get('profit', 0), trade_data.get('status', 'OPEN'),
                trade_data.get('open_time'), trade_data.get('close_time'),
                trade_data.get('strategy'), trade_data.get('notes')
            ))
            
            conn.commit()
            conn.close()
            return trade_id
    
    def get_trades(self, status=None, limit=200):
        """Get trades"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT * FROM trades WHERE status = ?
                    ORDER BY open_time DESC LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT * FROM trades ORDER BY open_time DESC LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
    
    def close_trade(self, trade_id, exit_price, profit, status='CLOSED'):
        """Close a trade"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE trades SET exit_price = ?, profit = ?, status = ?,
                close_time = ? WHERE id = ?
            ''', (exit_price, profit, status, datetime.now().isoformat(), trade_id))
            
            conn.commit()
            conn.close()
    
    # ========== Settings ==========
    
    def get_setting(self, key, default=None):
        """Get setting value"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                try:
                    return json.loads(row['value'])
                except:
                    return row['value']
            return default
    
    def set_setting(self, key, value):
        """Set setting value"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, json.dumps(value), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
    
    # ========== Backtest Results ==========
    
    def save_backtest_result(self, result):
        """Save backtest result"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            result_id = result.get('id', str(uuid.uuid4()))
            cursor.execute('''
                INSERT OR REPLACE INTO backtest_results
                (id, strategy_name, symbol, timeframe, start_date, end_date,
                 total_trades, win_rate, profit_factor, max_drawdown,
                 sharpe_ratio, net_profit, equity_curve, trades_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result_id, result.get('strategy_name'), result.get('symbol'),
                result.get('timeframe'), result.get('start_date'),
                result.get('end_date'), result.get('total_trades'),
                result.get('win_rate'), result.get('profit_factor'),
                result.get('max_drawdown'), result.get('sharpe_ratio'),
                result.get('net_profit'),
                json.dumps(result.get('equity_curve', [])),
                json.dumps(result.get('trades_data', []))
            ))
            
            conn.commit()
            conn.close()
            return result_id
    
    def get_backtest_results(self, limit=50):
        """Get backtest results"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM backtest_results ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
    
    # ========== LLM Models ==========
    
    def save_llm_model(self, model_data):
        """Save LLM model info"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            model_id = model_data.get('id', str(uuid.uuid4()))
            cursor.execute('''
                INSERT OR REPLACE INTO llm_models
                (id, name, path, size_gb, parameters, quantization,
                 is_loaded, last_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                model_id, model_data.get('name'), model_data.get('path'),
                model_data.get('size_gb'), model_data.get('parameters'),
                model_data.get('quantization'),
                model_data.get('is_loaded', 0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return model_id
    
    def get_llm_models(self):
        """Get all LLM models"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM llm_models ORDER BY last_used DESC')
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
    
    def update_llm_loaded(self, model_id, is_loaded):
        """Update model loaded status"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE llm_models SET is_loaded = ?, last_used = ? WHERE id = ?
            ''', (1 if is_loaded else 0, datetime.now().isoformat(), model_id))
            
            conn.commit()
            conn.close()
    
    # ========== Performance ==========
    
    def save_daily_performance(self, date, pnl, wins, losses, balance, equity):
        """Save daily performance"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            total = wins + losses
            win_rate = (wins / total * 100) if total > 0 else 0
            
            cursor.execute('''
                INSERT OR REPLACE INTO performance
                (date, total_pnl, win_count, loss_count, total_trades,
                 win_rate, balance, equity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, pnl, wins, losses, total, win_rate, balance, equity))
            
            conn.commit()
            conn.close()
    
    def get_performance_history(self, days=30):
        """Get performance history"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute('''
                SELECT * FROM performance WHERE date >= ? ORDER BY date ASC
            ''', (start_date,))
            
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
    
    # ========== News ==========
    
    def save_news(self, news_items):
        """Save news items"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            for item in news_items:
                news_id = item.get('id', str(uuid.uuid4()))
                cursor.execute('''
                    INSERT OR REPLACE INTO news
                    (id, title, source, content, currency, impact, published_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    news_id, item.get('title'), item.get('source'),
                    item.get('content'), item.get('currency'),
                    item.get('impact'), item.get('published_at')
                ))
            
            conn.commit()
            conn.close()
    
    def get_news(self, limit=50):
        """Get recent news"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM news ORDER BY published_at DESC LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
    
    def close(self):
        """Close database connections"""
        pass  # Connections are per-operation
