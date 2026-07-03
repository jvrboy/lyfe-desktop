"""
LYFE - News & Economic Calendar View
Market news and economic events
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class NewsView(BaseView):
    """News and economic calendar view"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: transparent; }
            QTabBar::tab {
                background: transparent; color: rgba(255,255,255,0.5);
                padding: 10px 24px; border: none;
                border-bottom: 2px solid transparent;
                font-size: 12px; font-weight: 600;
            }
            QTabBar::tab:selected {
                color: #6C5CE7; border-bottom: 2px solid #6C5CE7;
            }
        """)
        
        # Economic Calendar tab
        cal_tab = self.create_calendar_tab()
        self.tabs.addTab(cal_tab, "Economic Calendar")
        
        # News Headlines tab
        news_tab = self.create_news_tab()
        self.tabs.addTab(news_tab, "News Headlines")
        
        # Analysis tab
        analysis_tab = self.create_analysis_tab()
        self.tabs.addTab(analysis_tab, "Market Analysis")
        
        layout.addWidget(self.tabs)
    
    def create_calendar_tab(self):
        """Create economic calendar tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Filter bar
        filter_bar = QHBoxLayout()
        
        date_label = QLabel("Today - July 3, 2025")
        date_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
        filter_bar.addWidget(date_label)
        
        filter_bar.addStretch()
        
        currency_filter = QComboBox()
        currency_filter.addItems(["All Currencies", "USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
        filter_bar.addWidget(currency_filter)
        
        impact_filter = QComboBox()
        impact_filter.addItems(["All Impacts", "High", "Medium", "Low"])
        filter_bar.addWidget(impact_filter)
        
        layout.addLayout(filter_bar)
        
        # Calendar table
        self.calendar_table = QTableWidget()
        self.calendar_table.setColumnCount(7)
        self.calendar_table.setHorizontalHeaderLabels([
            "Time", "Currency", "Event", "Impact", "Actual", "Forecast", "Previous"
        ])
        self.calendar_table.setStyleSheet("""
            QTableWidget {
                background: transparent; border: none;
                color: white; font-size: 12px;
            }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.03); }
            QHeaderView::section {
                background: transparent; color: rgba(255,255,255,0.5);
                padding: 12px; border: none; border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 10px; font-weight: 600; text-transform: uppercase;
            }
        """)
        self.calendar_table.horizontalHeader().setStretchLastSection(True)
        self.calendar_table.verticalHeader().setVisible(False)
        
        # Load mock data
        events = [
            ("08:30", "USD", "Non-Farm Payrolls", "High", "272K", "180K", "165K"),
            ("10:00", "EUR", "ECB Interest Rate Decision", "High", "-", "4.25%", "4.50%"),
            ("12:30", "GBP", "GDP m/m", "Medium", "-", "0.2%", "0.4%"),
            ("14:00", "USD", "Crude Oil Inventories", "Low", "-", "-2.1M", "-1.4M"),
            ("16:30", "USD", "FOMC Meeting Minutes", "High", "-", "-", "-"),
            ("21:00", "AUD", "RBA Rate Statement", "Medium", "-", "4.35%", "4.35%"),
            ("23:50", "JPY", "BoJ Policy Meeting Minutes", "Medium", "-", "-", "-"),
        ]
        
        self.calendar_table.setRowCount(len(events))
        for i, (time, curr, event, impact, actual, forecast, prev) in enumerate(events):
            self.calendar_table.setItem(i, 0, QTableWidgetItem(time))
            
            curr_item = QTableWidgetItem(curr)
            curr_item.setForeground(QColor("#00D2FF"))
            self.calendar_table.setItem(i, 1, curr_item)
            
            self.calendar_table.setItem(i, 2, QTableWidgetItem(event))
            
            impact_item = QTableWidgetItem(impact)
            impact_colors = {"High": "#FF4757", "Medium": "#FFA502", "Low": "#00E6B4"}
            impact_item.setForeground(QColor(impact_colors.get(impact, "white")))
            self.calendar_table.setItem(i, 3, impact_item)
            
            self.calendar_table.setItem(i, 4, QTableWidgetItem(actual))
            self.calendar_table.setItem(i, 5, QTableWidgetItem(forecast))
            self.calendar_table.setItem(i, 6, QTableWidgetItem(prev))
        
        layout.addWidget(self.calendar_table)
        return widget
    
    def create_news_tab(self):
        """Create news headlines tab"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        
        # Filter
        filter_bar = QHBoxLayout()
        title = QLabel("Latest Market News")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 700;")
        filter_bar.addWidget(title)
        filter_bar.addStretch()
        
        source_filter = QComboBox()
        source_filter.addItems(["All Sources", "Reuters", "Bloomberg", "FXStreet", "CNBC"])
        filter_bar.addWidget(source_filter)
        
        layout.addLayout(filter_bar)
        
        # News cards
        headlines = [
            ("Dollar slips as traders price in earlier Fed cuts", "Reuters", "3m ago", 
             "The U.S. dollar weakened against major currencies on Thursday as traders increased bets on earlier Federal Reserve rate cuts following softer economic data."),
            ("Gold hits fresh record on safe-haven demand", "Bloomberg", "18m ago",
             "Gold prices surged to a new all-time high as geopolitical tensions and inflation concerns drove investors toward safe-haven assets."),
            ("BoE signals patience on rate path as inflation cools", "FXStreet", "42m ago",
             "Bank of England policymakers indicated they will maintain current interest rates as inflation shows signs of cooling toward the 2% target."),
            ("Bitcoin reclaims $67K as ETF inflows surge", "CNBC", "1h ago",
             "Bitcoin climbed back above $67,000 as spot Bitcoin ETFs saw record inflows, signaling strong institutional demand."),
            ("ECB holds rates steady, hints at September cut", "Reuters", "2h ago",
             "The European Central Bank kept interest rates unchanged but opened the door to a potential rate cut in September."),
            ("Oil prices rise on Middle East supply concerns", "Bloomberg", "3h ago",
             "Crude oil futures gained 2% as tensions in the Middle East raised concerns about potential supply disruptions."),
            ("Tech stocks lead NASDAQ to new highs", "CNBC", "4h ago",
             "Technology stocks pushed the NASDAQ Composite to fresh record highs as AI-related companies continued their rally."),
        ]
        
        for title_text, source, time, content in headlines:
            card = self.create_news_card(title_text, source, time, content)
            layout.addWidget(card)
        
        layout.addStretch()
        scroll.setWidget(container)
        return scroll
    
    def create_news_card(self, title, source, time, content):
        """Create a news card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
            }
            QFrame:hover {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(108,92,231,0.3);
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # Header
        header = QHBoxLayout()
        
        source_lbl = QLabel(source)
        source_lbl.setStyleSheet("color: #6C5CE7; font-size: 11px; font-weight: 700; text-transform: uppercase;")
        header.addWidget(source_lbl)
        
        header.addStretch()
        
        time_lbl = QLabel(time)
        time_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
        header.addWidget(time_lbl)
        
        layout.addLayout(header)
        
        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: white; font-size: 15px; font-weight: 700;")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)
        
        # Content
        content_lbl = QLabel(content)
        content_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px;")
        content_lbl.setWordWrap(True)
        layout.addWidget(content_lbl)
        
        return card
    
    def create_analysis_tab(self):
        """Create market analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Sentiment overview
        sentiment = QFrame()
        sentiment.setStyleSheet("""
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
        """)
        s_layout = QVBoxLayout(sentiment)
        
        title = QLabel("Market Sentiment Analysis")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 700;")
        s_layout.addWidget(title)
        
        # Sentiment meters
        meters = QHBoxLayout()
        
        for market, bullish in [("Forex", 62), ("Crypto", 78), ("Synthetic", 45), ("Stocks", 71)]:
            m_frame = QFrame()
            m_frame.setStyleSheet("background: rgba(0,0,0,0.2); border-radius: 14px;")
            m_layout = QVBoxLayout(m_frame)
            
            lbl = QLabel(market)
            lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px; font-weight: 600;")
            m_layout.addWidget(lbl)
            
            val = QLabel(f"{bullish}% Bullish")
            color = "#00E6B4" if bullish > 50 else "#FF4757"
            val.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: 800;")
            m_layout.addWidget(val)
            
            meters.addWidget(m_frame)
        
        s_layout.addLayout(meters)
        layout.addWidget(sentiment)
        
        # AI Analysis
        ai_frame = QFrame()
        ai_frame.setStyleSheet("""
            background: rgba(108,92,231,0.08);
            border: 1px solid rgba(108,92,231,0.2);
            border-radius: 20px;
        """)
        ai_layout = QVBoxLayout(ai_frame)
        
        ai_title = QLabel("\U0001F916 AI Market Analysis")
        ai_title.setStyleSheet("color: #6C5CE7; font-size: 16px; font-weight: 700;")
        ai_layout.addWidget(ai_title)
        
        ai_content = QLabel(
            "Current market conditions suggest a cautiously bullish outlook for major currency pairs. "
            "The EUR/USD is testing key resistance at 1.0850 with momentum indicators supporting a potential breakout. "
            "Gold remains in an uptrend channel with support at $2,320. Synthetic indices show ranging behavior "
            "across most volatility measures, favoring mean-reversion strategies. Risk sentiment is improving "
            "as Treasury yields stabilize, supporting carry trades in JPY crosses."
        )
        ai_content.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 13px;")
        ai_content.setWordWrap(True)
        ai_layout.addWidget(ai_content)
        
        layout.addWidget(ai_frame)
        layout.addStretch()
        
        return widget
    
    def refresh_data(self):
        pass
