"""
LYFE - Backtesting View
Strategy backtesting with performance analytics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QTabWidget,
    QFormLayout, QGroupBox, QFileDialog, QTextEdit, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class BacktestThread(QThread):
    """Background thread for running backtests"""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)
    
    def __init__(self, engine, strategy, data, symbol, timeframe):
        super().__init__()
        self.engine = engine
        self.strategy = strategy
        self.data = data
        self.symbol = symbol
        self.timeframe = timeframe
    
    def run(self):
        try:
            self.progress.emit(10)
            result = self.engine.run_backtest(
                self.strategy, self.data, self.symbol, self.timeframe
            )
            self.progress.emit(100)
            self.finished.emit({"success": True, "result": result})
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})


class BacktestView(BaseView):
    """Backtesting engine view"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Control panel
        controls = self.create_control_panel()
        layout.addWidget(controls)
        
        # Results tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: transparent; }
            QTabBar::tab {
                background: transparent; color: rgba(255,255,255,0.5);
                padding: 10px 20px; border: none;
                border-bottom: 2px solid transparent;
                font-size: 12px; font-weight: 600;
            }
            QTabBar::tab:selected {
                color: #6C5CE7; border-bottom: 2px solid #6C5CE7;
            }
        """)
        
        # Results tab
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(10)
        self.results_table.setHorizontalHeaderLabels([
            "Strategy", "Symbol", "Trades", "Win %", "Profit Factor",
            "Max DD %", "Sharpe", "Return %", "Expectancy", "Actions"
        ])
        self.results_table.setStyleSheet("""
            QTableWidget {
                background: transparent; border: none;
                color: white; font-size: 12px;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.03); }
            QHeaderView::section {
                background: transparent; color: rgba(255,255,255,0.5);
                padding: 10px; border: none; border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 10px; font-weight: 600; text-transform: uppercase;
            }
        """)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.results_table)
        
        self.tabs.addTab(results_tab, "Results")
        
        # Equity curve tab
        equity_tab = QWidget()
        equity_layout = QVBoxLayout(equity_tab)
        
        equity_placeholder = QLabel("Equity Curve Visualization\n(Interactive chart will render here)")
        equity_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        equity_placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 16px; padding: 60px;")
        equity_layout.addWidget(equity_placeholder)
        
        self.tabs.addTab(equity_tab, "Equity Curve")
        
        # Trades tab
        trades_tab = QWidget()
        trades_layout = QVBoxLayout(trades_tab)
        
        self.trades_table = QTableWidget()
        self.trades_table.setColumnCount(9)
        self.trades_table.setHorizontalHeaderLabels([
            "ID", "Dir", "Entry", "Exit", "P/L", "Pips", "Status", "Duration", "Strategy"
        ])
        self.trades_table.setStyleSheet(self.results_table.styleSheet())
        trades_layout.addWidget(self.trades_table)
        
        self.tabs.addTab(trades_tab, "Trade Log")
        
        layout.addWidget(self.tabs)
        
        # Load mock results
        self.load_mock_results()
    
    def create_control_panel(self):
        """Create backtest control panel"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
            }
        """)
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Strategy
        strat_layout = QVBoxLayout()
        strat_label = QLabel("Strategy")
        strat_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase;")
        strat_layout.addWidget(strat_label)
        
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            "EMA Crossover", "RSI Divergence", "Bollinger Bounce",
            "MACD Momentum", "Breakout", "Smart Money Concepts"
        ])
        strat_layout.addWidget(self.strategy_combo)
        layout.addLayout(strat_layout)
        
        # Symbol
        sym_layout = QVBoxLayout()
        sym_label = QLabel("Symbol")
        sym_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase;")
        sym_layout.addWidget(sym_label)
        
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD", "R_75", "R_100"])
        sym_layout.addWidget(self.symbol_combo)
        layout.addLayout(sym_layout)
        
        # Timeframe
        tf_layout = QVBoxLayout()
        tf_label = QLabel("Timeframe")
        tf_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase;")
        tf_layout.addWidget(tf_label)
        
        self.tf_combo = QComboBox()
        self.tf_combo.addItems(["M1", "M5", "M15", "H1", "H4", "D1"])
        tf_layout.addWidget(self.tf_combo)
        layout.addLayout(tf_layout)
        
        # Period
        period_layout = QVBoxLayout()
        period_label = QLabel("Period (months)")
        period_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase;")
        period_layout.addWidget(period_label)
        
        self.period_spin = QSpinBox()
        self.period_spin.setRange(1, 60)
        self.period_spin.setValue(6)
        period_layout.addWidget(self.period_spin)
        layout.addLayout(period_layout)
        
        layout.addStretch()
        
        # Run button
        run_btn = QPushButton("\u25B6 Run Backtest")
        run_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C5CE7,
                    stop:1 #00D2FF);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7D6DF8,
                    stop:1 #11E3FF);
            }
        """)
        run_btn.clicked.connect(self.run_backtest)
        layout.addWidget(run_btn)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(4)
        self.progress.setStyleSheet("""
            QProgressBar { background: rgba(255,255,255,0.05); border-radius: 2px; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6C5CE7, stop:1 #00D2FF); border-radius: 2px; }
        """)
        layout.addWidget(self.progress)
        
        return panel
    
    def load_mock_results(self):
        """Load mock backtest results"""
        results = [
            ("EMA Crossover", "EURUSD", 47, 61.7, 2.34, 14.2, 1.87, 18.5, 12.3),
            ("RSI Divergence", "XAUUSD", 32, 68.8, 3.12, 11.5, 2.15, 24.2, 18.7),
            ("Bollinger Bounce", "GBPUSD", 56, 58.9, 1.89, 16.8, 1.45, 14.3, 8.9),
            ("MACD Momentum", "BTCUSD", 28, 64.3, 2.78, 22.1, 1.92, 31.5, 22.4),
            ("Breakout", "NAS100", 41, 56.1, 1.65, 19.4, 1.23, 11.8, 6.5),
        ]
        
        self.results_table.setRowCount(len(results))
        for i, (strat, sym, trades, wr, pf, dd, sr, ret, exp) in enumerate(results):
            items = [strat, sym, str(trades), f"{wr}%", f"{pf}", f"{dd}%", f"{sr}", f"{ret}%", f"{exp}"]
            for j, val in enumerate(items):
                item = QTableWidgetItem(val)
                if j in [3, 4, 6, 7]:  # Color positive metrics
                    try:
                        v = float(val.replace("%", ""))
                        if v > 0:
                            item.setForeground(QColor("#00E6B4"))
                    except:
                        pass
                self.results_table.setItem(i, j, item)
            
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(108,92,231,0.3);
                    color: #6C5CE7;
                    border: 1px solid rgba(108,92,231,0.4);
                    border-radius: 6px;
                    padding: 4px 12px;
                    font-size: 10px; font-weight: 700;
                }
            """)
            self.results_table.setCellWidget(i, 9, view_btn)
    
    def run_backtest(self):
        """Run backtest"""
        self.progress.setVisible(True)
        self.progress.setValue(0)
        
        # In a real implementation, this would load historical data
        # and run the backtest in a background thread
        import random
        for i in range(101):
            self.progress.setValue(i)
            # Simulate work
            if i < 100:
                pass
    
    def refresh_data(self):
        pass
