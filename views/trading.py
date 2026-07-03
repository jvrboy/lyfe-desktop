"""
LYFE - Trading Terminal View
Full trading interface with order execution and position management
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
    QGroupBox, QFormLayout, QCheckBox, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer

from views.base_view import BaseView


class TradingView(BaseView):
    """Trading terminal view"""
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Order entry
        left = self.create_order_panel()
        splitter.addWidget(left)
        
        # Center - Price chart placeholder
        center = self.create_chart_panel()
        splitter.addWidget(center)
        
        # Right panel - Positions & Orders
        right = self.create_positions_panel()
        splitter.addWidget(right)
        
        splitter.setSizes([300, 600, 350])
        layout.addWidget(splitter)
    
    def create_order_panel(self):
        """Create order entry panel"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("ORDER ENTRY")
        title.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)
        
        # Symbol selector
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems([
            "EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", 
            "BTC/USD", "NAS100", "R_75", "R_100"
        ])
        layout.addWidget(self.symbol_combo)
        
        # Current price display
        price_layout = QHBoxLayout()
        self.bid_label = QLabel("1.0823")
        self.bid_label.setStyleSheet("color: #FF4757; font-size: 24px; font-weight: 800;")
        price_layout.addWidget(QLabel("BID:"))
        price_layout.addWidget(self.bid_label)
        
        self.ask_label = QLabel("1.0825")
        self.ask_label.setStyleSheet("color: #00E6B4; font-size: 24px; font-weight: 800;")
        price_layout.addWidget(QLabel("ASK:"))
        price_layout.addWidget(self.ask_label)
        
        layout.addLayout(price_layout)
        
        # Spread
        spread = QLabel("Spread: 0.2 pips")
        spread.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
        layout.addWidget(spread)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(255,255,255,0.08); max-height: 1px;")
        layout.addWidget(sep)
        
        # Order form
        form = QFormLayout()
        form.setSpacing(12)
        
        # Volume
        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0.01, 100)
        self.volume_spin.setValue(0.1)
        self.volume_spin.setDecimals(2)
        self.volume_spin.setSingleStep(0.01)
        form.addRow("Volume:", self.volume_spin)
        
        # SL
        self.sl_input = QDoubleSpinBox()
        self.sl_input.setRange(0, 999999)
        self.sl_input.setDecimals(5)
        self.sl_input.setValue(1.0798)
        form.addRow("Stop Loss:", self.sl_input)
        
        # TP
        self.tp_input = QDoubleSpinBox()
        self.tp_input.setRange(0, 999999)
        self.tp_input.setDecimals(5)
        self.tp_input.setValue(1.0876)
        form.addRow("Take Profit:", self.tp_input)
        
        layout.addLayout(form)
        
        # Risk info
        risk_info = QFrame()
        risk_info.setStyleSheet("background: rgba(255,255,255,0.03); border-radius: 12px;")
        ri_layout = QVBoxLayout(risk_info)
        
        margin = QLabel("Margin: $108.24")
        margin.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px;")
        ri_layout.addWidget(margin)
        
        risk = QLabel("Risk: $24.50 (2.45%)")
        risk.setStyleSheet("color: #FFA502; font-size: 12px;")
        ri_layout.addWidget(risk)
        
        layout.addWidget(risk_info)
        
        # Buy/Sell buttons
        btn_layout = QHBoxLayout()
        
        buy_btn = QPushButton("BUY")
        buy_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0,230,180,0.5),
                    stop:1 rgba(0,230,180,0.3));
                color: white;
                border: 1px solid rgba(0,230,180,0.4);
                border-radius: 14px;
                padding: 16px;
                font-size: 16px;
                font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0,230,180,0.7),
                    stop:1 rgba(0,230,180,0.5));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0,230,180,0.3),
                    stop:1 rgba(0,230,180,0.2));
            }
        """)
        btn_layout.addWidget(buy_btn)
        
        sell_btn = QPushButton("SELL")
        sell_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,71,87,0.5),
                    stop:1 rgba(255,71,87,0.3));
                color: white;
                border: 1px solid rgba(255,71,87,0.4);
                border-radius: 14px;
                padding: 16px;
                font-size: 16px;
                font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,71,87,0.7),
                    stop:1 rgba(255,71,87,0.5));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,71,87,0.3),
                    stop:1 rgba(255,71,87,0.2));
            }
        """)
        btn_layout.addWidget(sell_btn)
        
        layout.addLayout(btn_layout)
        
        # One-click trading toggle
        oct = QCheckBox("One-Click Trading")
        oct.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px;")
        layout.addWidget(oct)
        
        layout.addStretch()
        
        return panel
    
    def create_chart_panel(self):
        """Create price chart panel"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Chart header
        header = QHBoxLayout()
        
        chart_title = QLabel("EUR/USD - M5")
        chart_title.setStyleSheet("color: white; font-size: 14px; font-weight: 700;")
        header.addWidget(chart_title)
        
        # Timeframe buttons
        for tf in ["M1", "M5", "M15", "H1", "H4", "D1"]:
            tf_btn = QPushButton(tf)
            tf_btn.setFixedSize(40, 28)
            is_active = tf == "M5"
            tf_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'rgba(108,92,231,0.4)' if is_active else 'transparent'};
                    color: {'white' if is_active else 'rgba(255,255,255,0.5)'};
                    border: 1px solid {'rgba(108,92,231,0.5)' if is_active else 'rgba(255,255,255,0.1)'};
                    border-radius: 6px;
                    font-size: 10px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background: rgba(108,92,231,0.3);
                    color: white;
                }}
            """)
            header.addWidget(tf_btn)
        
        header.addStretch()
        layout.addLayout(header)
        
        # Chart placeholder
        chart_area = QFrame()
        chart_area.setStyleSheet("""
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
        """)
        chart_layout = QVBoxLayout(chart_area)
        
        placeholder = QLabel("Interactive Chart\n(TradingView integration)\n\nCandlestick visualization\nwith indicators overlay")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 14px;")
        chart_layout.addWidget(placeholder)
        
        layout.addWidget(chart_area, 1)
        
        # Indicator toggle bar
        ind_bar = QHBoxLayout()
        for ind in ["EMA", "MACD", "RSI", "BB", "Volume"]:
            ind_btn = QPushButton(ind)
            ind_btn.setCheckable(True)
            ind_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.06);
                    color: rgba(255,255,255,0.6);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
                QPushButton:checked {
                    background: rgba(108,92,231,0.3);
                    color: white;
                    border: 1px solid rgba(108,92,231,0.5);
                }
            """)
            ind_bar.addWidget(ind_btn)
        ind_bar.addStretch()
        layout.addLayout(ind_bar)
        
        return panel
    
    def create_positions_panel(self):
        """Create positions and orders panel"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: transparent;
                color: rgba(255,255,255,0.5);
                padding: 10px 16px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 12px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                color: #6C5CE7;
                border-bottom: 2px solid #6C5CE7;
            }
        """)
        
        # Positions tab
        positions_tab = QWidget()
        pos_layout = QVBoxLayout(positions_tab)
        
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(6)
        self.positions_table.setHorizontalHeaderLabels(["Symbol", "Dir", "Volume", "Entry", "P/L", "Actions"])
        self.positions_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                color: white;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255,255,255,0.03);
            }
            QHeaderView::section {
                background: transparent;
                color: rgba(255,255,255,0.5);
                padding: 8px;
                border: none;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
            }
        """)
        self.positions_table.horizontalHeader().setStretchLastSection(True)
        self.load_positions()
        pos_layout.addWidget(self.positions_table)
        
        tabs.addTab(positions_tab, "Positions (3)")
        
        # Pending orders tab
        pending_tab = QWidget()
        pend_layout = QVBoxLayout(pending_tab)
        
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(5)
        self.pending_table.setHorizontalHeaderLabels(["Symbol", "Type", "Price", "Volume", "Actions"])
        self.pending_table.setStyleSheet(self.positions_table.styleSheet())
        self.pending_table.horizontalHeader().setStretchLastSection(True)
        pend_layout.addWidget(self.pending_table)
        
        tabs.addTab(pending_tab, "Pending (2)")
        
        # Account summary
        acct = QFrame()
        acct.setStyleSheet("background: rgba(0,0,0,0.2); border-radius: 12px;")
        acct_layout = QVBoxLayout(acct)
        
        balance = QLabel("Balance: $10,842.50")
        balance.setStyleSheet("color: white; font-size: 14px; font-weight: 700;")
        acct_layout.addWidget(balance)
        
        equity = QLabel("Equity: $10,920.30")
        equity.setStyleSheet("color: #00E6B4; font-size: 13px;")
        acct_layout.addWidget(equity)
        
        margin = QLabel("Used Margin: $324.80 | Free: $10,595.50")
        margin.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
        acct_layout.addWidget(margin)
        
        pos_layout.addWidget(acct)
        
        layout.addWidget(tabs)
        
        return panel
    
    def load_positions(self):
        """Load positions into table"""
        positions = [
            ("EUR/USD", "BUY", "0.5", "1.0810", "+$62.50"),
            ("XAU/USD", "SELL", "0.2", "2345.0", "+$48.00"),
            ("NAS100", "BUY", "1.0", "18380", "+$120.00"),
        ]
        
        self.positions_table.setRowCount(len(positions))
        for i, (sym, dir, vol, entry, pl) in enumerate(positions):
            self.positions_table.setItem(i, 0, QTableWidgetItem(sym))
            
            dir_item = QTableWidgetItem(dir)
            dir_item.setForeground(QColor("#00E6B4" if dir == "BUY" else "#FF4757"))
            self.positions_table.setItem(i, 1, dir_item)
            
            self.positions_table.setItem(i, 2, QTableWidgetItem(vol))
            self.positions_table.setItem(i, 3, QTableWidgetItem(entry))
            
            pl_item = QTableWidgetItem(pl)
            pl_item.setForeground(QColor("#00E6B4" if "+" in pl else "#FF4757"))
            self.positions_table.setItem(i, 4, pl_item)
            
            close_btn = QPushButton("Close")
            close_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,71,87,0.3);
                    color: #FF4757;
                    border: 1px solid rgba(255,71,87,0.4);
                    border-radius: 6px;
                    padding: 4px 10px;
                    font-size: 10px;
                    font-weight: 700;
                }
            """)
            self.positions_table.setCellWidget(i, 5, close_btn)
    
    def refresh_data(self):
        """Refresh trading data"""
        pass
