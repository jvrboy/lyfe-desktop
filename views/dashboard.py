"""
LYFE - Dashboard View
Main overview with stats, market overview, active signals
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QProgressBar, QScrollArea, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QFont

from views.base_view import BaseView


class DashboardView(BaseView):
    """Main dashboard overview"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4, 4, 4, 4)
        content_layout.setSpacing(20)
        
        # Welcome header
        header = self.create_header()
        content_layout.addWidget(header)
        
        # Stats row
        stats = self.create_stats_row()
        content_layout.addLayout(stats)
        
        # Performance + Active signals
        middle = QHBoxLayout()
        middle.setSpacing(20)
        
        # Performance card
        perf_card, perf_layout = self.create_card("PERFORMANCE", strong=True)
        self.perf_content = QVBoxLayout()
        perf_layout.addLayout(self.perf_content)
        middle.addWidget(perf_card, 1)
        
        # Active signals card
        sig_card, sig_layout = self.create_card("ACTIVE SIGNALS")
        self.sig_content = QVBoxLayout()
        sig_layout.addLayout(self.sig_content)
        middle.addWidget(sig_card, 1)
        
        content_layout.addLayout(middle)
        
        # Market overview
        market_card, market_layout = self.create_card("MARKET OVERVIEW")
        self.market_content = QHBoxLayout()
        market_layout.addLayout(self.market_content)
        content_layout.addWidget(market_card)
        
        # Quick tools
        tools_card, tools_layout = self.create_card("QUICK TOOLS")
        self.tools_content = QHBoxLayout()
        tools_layout.addLayout(self.tools_content)
        content_layout.addWidget(tools_card)
        
        # AI Confidence
        ai_card, ai_layout = self.create_card("AI CONFIDENCE INDEX", strong=True)
        self.ai_content = QVBoxLayout()
        ai_layout.addLayout(self.ai_content)
        content_layout.addWidget(ai_card)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def create_header(self):
        """Create welcome header"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        left = QVBoxLayout()
        
        welcome = QLabel("Welcome back")
        welcome.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 12px; letter-spacing: 3px; text-transform: uppercase;")
        left.addWidget(welcome)
        
        name = QLabel("Trader")
        name.setStyleSheet("color: white; font-size: 28px; font-weight: 700;")
        left.addWidget(name)
        
        layout.addLayout(left)
        layout.addStretch()
        
        # Avatar
        avatar = QLabel("L")
        avatar.setFixedSize(48, 48)
        avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(108,92,231,0.5),
                stop:1 rgba(0,210,255,0.3));
            border-radius: 24px;
            color: white;
            font-size: 20px;
            font-weight: 800;
            text-align: center;
        """)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(avatar)
        
        return widget
    
    def create_stats_row(self):
        """Create statistics row"""
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        self.stat_winrate = self.create_stat_card("WIN RATE", "73%", "+5.2% vs last week", "#00D2FF")
        self.stat_signals = self.create_stat_card("SIGNALS", "248", "12 this week", "white")
        self.stat_profit = self.create_stat_card("PROFIT", "$1,842", "+$320 this month", "#00E6B4")
        self.stat_rr = self.create_stat_card("AVG R:R", "2.1", "Above target", "#6C5CE7")
        
        layout.addWidget(self.stat_winrate)
        layout.addWidget(self.stat_signals)
        layout.addWidget(self.stat_profit)
        layout.addWidget(self.stat_rr)
        
        return layout
    
    def load_data(self):
        """Load dashboard data"""
        self.load_performance()
        self.load_signals()
        self.load_market()
        self.load_tools()
        self.load_ai_confidence()
    
    def load_performance(self):
        """Load performance section"""
        # Clear existing
        while self.perf_content.count():
            item = self.perf_content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Win rate circle (simplified as progress bar)
        win_layout = QHBoxLayout()
        
        win_label = QLabel("7-Day Win Rate")
        win_label.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 13px;")
        win_layout.addWidget(win_label)
        
        win_value = QLabel("73%")
        win_value.setStyleSheet("color: #00D2FF; font-size: 36px; font-weight: 800;")
        win_layout.addWidget(win_value)
        win_layout.addStretch()
        
        self.perf_content.addLayout(win_layout)
        
        # Progress bar for win rate
        progress = QProgressBar()
        progress.setValue(73)
        progress.setTextVisible(False)
        progress.setFixedHeight(8)
        progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.05);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00D2FF,
                    stop:1 #6C5CE7);
                border-radius: 4px;
            }
        """)
        self.perf_content.addWidget(progress)
        
        # Stats grid
        grid = QGridLayout()
        grid.setSpacing(8)
        
        metrics = [
            ("Total Trades", "156"),
            ("Winning", "114"),
            ("Losing", "42"),
            ("Best Streak", "8 wins"),
        ]
        
        for i, (label, value) in enumerate(metrics):
            card = QFrame()
            card.setStyleSheet("""
                background: rgba(255,255,255,0.04);
                border-radius: 12px;
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(12, 10, 12, 10)
            
            lbl = QLabel(label)
            lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase;")
            c_layout.addWidget(lbl)
            
            val = QLabel(value)
            val.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
            c_layout.addWidget(val)
            
            grid.addWidget(card, i // 2, i % 2)
        
        self.perf_content.addLayout(grid)
    
    def load_signals(self):
        """Load active signals"""
        while self.sig_content.count():
            item = self.sig_content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Mock active signals
        signals = [
            ("EUR/USD", "BUY", "1.0824", "87%", "#00E6B4"),
            ("XAU/USD", "SELL", "2342.5", "92%", "#FF4757"),
            ("GBP/JPY", "BUY", "198.42", "74%", "#00E6B4"),
        ]
        
        for pair, direction, price, conf, color in signals:
            row = QFrame()
            row.setStyleSheet("""
                background: rgba(255,255,255,0.04);
                border-radius: 12px;
            """)
            r_layout = QHBoxLayout(row)
            r_layout.setContentsMargins(12, 10, 12, 10)
            
            # Direction indicator
            dir_label = QLabel(direction)
            dir_label.setFixedSize(50, 28)
            dir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dir_label.setStyleSheet(f"""
                background: {color}22;
                color: {color};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 700;
            """)
            r_layout.addWidget(dir_label)
            
            # Pair
            pair_label = QLabel(pair)
            pair_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
            r_layout.addWidget(pair_label)
            
            r_layout.addStretch()
            
            # Price
            price_label = QLabel(price)
            price_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 13px;")
            r_layout.addWidget(price_label)
            
            # Confidence
            conf_label = QLabel(conf)
            conf_label.setStyleSheet("color: #6C5CE7; font-size: 13px; font-weight: 700;")
            r_layout.addWidget(conf_label)
            
            self.sig_content.addWidget(row)
    
    def load_market(self):
        """Load market overview"""
        while self.market_content.count():
            item = self.market_content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        tickers = [
            ("EUR/USD", "1.0824", "+0.18%", True),
            ("GBP/USD", "1.2715", "-0.09%", False),
            ("USD/JPY", "156.82", "+0.34%", True),
            ("XAU/USD", "2342.5", "+0.81%", True),
            ("BTC/USD", "67420", "+1.24%", True),
            ("NAS100", "18420", "-0.42%", False),
        ]
        
        for sym, price, change, is_up in tickers:
            card = QFrame()
            card.setFixedWidth(140)
            card.setStyleSheet("""
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px;
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(12, 10, 12, 10)
            
            sym_label = QLabel(sym)
            sym_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            c_layout.addWidget(sym_label)
            
            price_label = QLabel(price)
            price_label.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
            c_layout.addWidget(price_label)
            
            change_color = "#00E6B4" if is_up else "#FF4757"
            change_label = QLabel(change)
            change_label.setStyleSheet(f"color: {change_color}; font-size: 12px; font-weight: 600;")
            c_layout.addWidget(change_label)
            
            self.market_content.addWidget(card)
    
    def load_tools(self):
        """Load quick tools"""
        while self.tools_content.count():
            item = self.tools_content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        tools = [
            ("AI Analysis", "\U0001F916"),
            ("Top Down", "\U0001F4CA"),
            ("APA", "\U0001F3AF"),
            ("SMT", "\U000026A1"),
            ("Profile", "\U0001F4C8"),
            ("Calc", "\U0001F522"),
        ]
        
        for name, icon in tools:
            btn = QFrame()
            btn.setFixedSize(100, 80)
            btn.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,0.06);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 16px;
                }
                QFrame:hover {
                    background: rgba(255,255,255,0.12);
                    border: 1px solid rgba(108,92,231,0.3);
                }
            """)
            b_layout = QVBoxLayout(btn)
            b_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 24px;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b_layout.addWidget(icon_label)
            
            name_label = QLabel(name)
            name_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 10px; font-weight: 600;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b_layout.addWidget(name_label)
            
            self.tools_content.addWidget(btn)
    
    def load_ai_confidence(self):
        """Load AI confidence section"""
        while self.ai_content.count():
            item = self.ai_content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        layout = QHBoxLayout()
        
        # Left - confidence score
        left = QVBoxLayout()
        
        score_label = QLabel("85%")
        score_label.setStyleSheet("color: white; font-size: 48px; font-weight: 800;")
        left.addWidget(score_label)
        
        desc = QLabel("Model Confidence")
        desc.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 13px;")
        left.addWidget(desc)
        
        layout.addLayout(left)
        
        # Right - individual model confidences
        right = QVBoxLayout()
        
        models = [
            ("Neural Network", 92),
            ("Pattern Matcher", 78),
            ("Sentiment", 85),
            ("Technical", 88),
        ]
        
        for name, val in models:
            row = QHBoxLayout()
            
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 12px;")
            name_lbl.setFixedWidth(120)
            row.addWidget(name_lbl)
            
            bar = QProgressBar()
            bar.setValue(val)
            bar.setFixedHeight(6)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    background: rgba(255,255,255,0.05);
                    border-radius: 3px;
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6C5CE7,
                        stop:1 #00D2FF);
                    border-radius: 3px;
                }}
            """)
            row.addWidget(bar)
            
            val_lbl = QLabel(f"{val}%")
            val_lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            val_lbl.setFixedWidth(40)
            row.addWidget(val_lbl)
            
            right.addLayout(row)
        
        layout.addLayout(right)
        self.ai_content.addLayout(layout)
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # Update with live prices from Deriv API
        prices = self.deriv_api.get_all_prices()
        # Could update price displays here
