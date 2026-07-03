"""
LYFE - AI Signals View
Live trading signals with AI-generated analysis
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QPushButton, QComboBox, QProgressBar, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QGridLayout, QLineEdit, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class SignalsView(BaseView):
    """AI Signals view"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Filter bar
        filter_bar = self.create_filter_bar()
        layout.addWidget(filter_bar)
        
        # Signal stats
        stats = self.create_signal_stats()
        layout.addLayout(stats)
        
        # Signals list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.signals_container = QWidget()
        self.signals_layout = QVBoxLayout(self.signals_container)
        self.signals_layout.setSpacing(12)
        self.signals_layout.addStretch()
        
        scroll.setWidget(self.signals_container)
        layout.addWidget(scroll)
    
    def create_filter_bar(self):
        """Create filter controls"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("AI Trading Signals")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 700;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Filters
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Signals", "Active", "Pending", "Forex", "Crypto", "Synthetic"])
        self.filter_combo.setFixedWidth(160)
        layout.addWidget(self.filter_combo)
        
        # Refresh button
        refresh = QPushButton("\U0001F504 Refresh")
        refresh.setStyleSheet("""
            QPushButton {
                background: rgba(108,92,231,0.3);
                border: 1px solid rgba(108,92,231,0.5);
                border-radius: 10px;
                padding: 8px 16px;
                color: white;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(108,92,231,0.5);
            }
        """)
        refresh.clicked.connect(self.load_data)
        layout.addWidget(refresh)
        
        return widget
    
    def create_signal_stats(self):
        """Create signal statistics"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        stats = [
            ("Active", "5", "#00E6B4"),
            ("Win Rate", "73%", "#00D2FF"),
            ("Today", "12", "#6C5CE7"),
            ("Profit", "+$420", "#00E6B4"),
        ]
        
        for label, value, color in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px;
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(16, 12, 16, 12)
            
            lbl = QLabel(label)
            lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase; letter-spacing: 1px;")
            c_layout.addWidget(lbl)
            
            val = QLabel(value)
            val.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: 700;")
            c_layout.addWidget(val)
            
            layout.addWidget(card)
        
        return layout
    
    def load_data(self):
        """Load signals"""
        # Clear existing (except stretch)
        while self.signals_layout.count() > 1:
            item = self.signals_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Mock signals data
        signals = [
            {
                "pair": "EUR/USD",
                "direction": "BUY",
                "entry": 1.0824,
                "sl": 1.0798,
                "tp": 1.0876,
                "confidence": 87,
                "rr": 2.0,
                "strategies": ["TopDown", "APA", "SMT"],
                "status": "ACTIVE",
                "time": "2m ago"
            },
            {
                "pair": "XAU/USD",
                "direction": "SELL",
                "entry": 2342.5,
                "sl": 2351.2,
                "tp": 2320.1,
                "confidence": 92,
                "rr": 2.6,
                "strategies": ["MarketProfile", "Divergence"],
                "status": "ACTIVE",
                "time": "8m ago"
            },
            {
                "pair": "GBP/JPY",
                "direction": "BUY",
                "entry": 198.42,
                "sl": 197.85,
                "tp": 199.64,
                "confidence": 74,
                "rr": 2.1,
                "strategies": ["APA", "RSI Div"],
                "status": "PENDING",
                "time": "14m ago"
            },
            {
                "pair": "BTC/USD",
                "direction": "BUY",
                "entry": 67420,
                "sl": 66800,
                "tp": 68900,
                "confidence": 81,
                "rr": 2.4,
                "strategies": ["SMT", "TopDown"],
                "status": "ACTIVE",
                "time": "22m ago"
            },
            {
                "pair": "NAS100",
                "direction": "SELL",
                "entry": 18420,
                "sl": 18480,
                "tp": 18300,
                "confidence": 68,
                "rr": 2.0,
                "strategies": ["Breakout", "Volume"],
                "status": "PENDING",
                "time": "35m ago"
            },
        ]
        
        for sig in signals:
            card = self.create_signal_card(sig)
            self.signals_layout.insertWidget(self.signals_layout.count() - 1, card)
    
    def create_signal_card(self, signal):
        """Create individual signal card"""
        card = QFrame()
        is_buy = signal["direction"] == "BUY"
        dir_color = "#00E6B4" if is_buy else "#FF4757"
        
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-left: 3px solid {dir_color};
                border-radius: 16px;
            }}
            QFrame:hover {{
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(108,92,231,0.3);
                border-left: 3px solid {dir_color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Header row
        header = QHBoxLayout()
        
        # Direction badge
        badge = QLabel(signal["direction"])
        badge.setFixedSize(60, 28)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            background: {dir_color}22;
            color: {dir_color};
            border-radius: 8px;
            font-size: 11px;
            font-weight: 800;
        """)
        header.addWidget(badge)
        
        # Pair
        pair = QLabel(signal["pair"])
        pair.setStyleSheet("color: white; font-size: 18px; font-weight: 700;")
        header.addWidget(pair)
        
        header.addStretch()
        
        # Confidence
        conf = QLabel(f"{signal['confidence']}%")
        conf.setStyleSheet("color: #6C5CE7; font-size: 24px; font-weight: 800;")
        header.addWidget(conf)
        
        layout.addLayout(header)
        
        # Details row
        details = QHBoxLayout()
        
        for label, value in [("Entry", str(signal["entry"])), ("SL", str(signal["sl"])), ("TP", str(signal["tp"]))]:
            col = QVBoxLayout()
            
            lbl = QLabel(label)
            lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase;")
            col.addWidget(lbl)
            
            val = QLabel(value)
            color = "#FF4757" if label == "SL" else "#00E6B4" if label == "TP" else "white"
            val.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 600;")
            col.addWidget(val)
            
            details.addLayout(col)
        
        # R:R
        rr_col = QVBoxLayout()
        rr_lbl = QLabel("R:R")
        rr_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase;")
        rr_col.addWidget(rr_lbl)
        rr_val = QLabel(f"{signal['rr']}:1")
        rr_val.setStyleSheet("color: #00D2FF; font-size: 14px; font-weight: 600;")
        rr_col.addWidget(rr_val)
        details.addLayout(rr_col)
        
        layout.addLayout(details)
        
        # Confidence bar
        conf_bar = QProgressBar()
        conf_bar.setValue(signal["confidence"])
        conf_bar.setFixedHeight(4)
        conf_bar.setTextVisible(False)
        conf_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.05);
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00D2FF,
                    stop:0.5 #6C5CE7,
                    stop:1 #FF6B6B);
                border-radius: 2px;
            }
        """)
        layout.addWidget(conf_bar)
        
        # Strategies tags
        tags = QHBoxLayout()
        for strat in signal["strategies"]:
            tag = QLabel(strat)
            tag.setStyleSheet("""
                background: rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.8);
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 10px;
                font-weight: 600;
            """)
            tags.addWidget(tag)
        tags.addStretch()
        
        status = QLabel(signal["status"])
        status_color = "#00E6B4" if signal["status"] == "ACTIVE" else "#FFA502"
        status.setStyleSheet(f"color: {status_color}; font-size: 11px; font-weight: 700;")
        tags.addWidget(status)
        
        layout.addLayout(tags)
        
        # Action buttons
        actions = QHBoxLayout()
        
        copy_btn = QPushButton("Copy Trade")
        copy_btn.setStyleSheet(f"""
            QPushButton {{
                background: {dir_color}33;
                color: {dir_color};
                border: 1px solid {dir_color}44;
                border-radius: 10px;
                padding: 10px 24px;
                font-size: 12px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: {dir_color}55;
            }}
        """)
        actions.addWidget(copy_btn)
        
        details_btn = QPushButton("Details")
        details_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: rgba(255,255,255,0.8);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 10px 24px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.12);
            }
        """)
        actions.addWidget(details_btn)
        
        layout.addLayout(actions)
        
        return card
    
    def refresh_data(self):
        """Refresh signals"""
        pass
