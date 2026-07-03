#!/usr/bin/env python3
"""
LYFE - AI-Powered Trading & Analytics Platform
Desktop Application (Windows)
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QScrollArea,
    QSizePolicy, QGraphicsDropShadowEffect, QProgressBar,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
    QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QSlider, QTabWidget, QMessageBox, QFileDialog, QGridLayout,
    QSpacerItem, QSplitter, QGroupBox, QRadioButton, QButtonGroup,
    QMenu, QSystemTrayIcon, QDialog, QDialogButtonBox, QFormLayout,
    QPlainTextEdit, QStatusBar, QToolButton, QLayout, QStackedLayout
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QPropertyAnimation,
    QEasingCurve, QPoint, QParallelAnimationGroup, QSequentialAnimationGroup,
    QRect, QPointF, pyqtProperty
)
from PyQt6.QtGui import (
    QColor, QPainter, QBrush, QLinearGradient, QRadialGradient,
    QFont, QIcon, QPixmap, QPalette, QFontDatabase, QAction,
    QCursor, QPen, QFontMetrics, QImage
)

# Local imports
from database import DatabaseManager
from deriv_api import DerivAPI
from llm_manager import LLMManager
from backtest_engine import BacktestEngine
from styles import GLASS_STYLES, ANIMATIONS
from views.dashboard import DashboardView
from views.signals import SignalsView
from views.trading import TradingView
from views.backtest import BacktestView
from views.news import NewsView
from views.llm_view import LLMView
from views.tools_view import ToolsView
from views.settings_view import SettingsView


class GlassButton(QPushButton):
    """Custom glass morphism button"""
    
    def __init__(self, text="", icon_text="", parent=None, variant="default"):
        super().__init__(text, parent)
        self.variant = variant
        self.icon_text = icon_text
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(40)
        self.update_style()
    
    def update_style(self):
        base = """
            QPushButton {
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.15),
                    stop:1 rgba(255,255,255,0.05));
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.25),
                    stop:1 rgba(255,255,255,0.1));
                border: 1px solid rgba(255,255,255,0.2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.1),
                    stop:1 rgba(255,255,255,0.02));
            }
            QPushButton:disabled {
                background: rgba(255,255,255,0.03);
                color: rgba(255,255,255,0.3);
                border: 1px solid rgba(255,255,255,0.05);
            }
        """
        
        if self.variant == "primary":
            base = base.replace(
                "rgba(255,255,255,0.15)", "rgba(108,92,231,0.5)"
            ).replace(
                "rgba(255,255,255,0.05)", "rgba(108,92,231,0.3)"
            ).replace(
                "rgba(255,255,255,0.25)", "rgba(108,92,231,0.7)"
            ).replace(
                "rgba(255,255,255,0.1)", "rgba(108,92,231,0.5)"
            )
        elif self.variant == "success":
            base = base.replace(
                "rgba(255,255,255,0.15)", "rgba(0,230,180,0.4)"
            ).replace(
                "rgba(255,255,255,0.05)", "rgba(0,230,180,0.2)"
            ).replace(
                "rgba(255,255,255,0.25)", "rgba(0,230,180,0.6)"
            ).replace(
                "rgba(255,255,255,0.1)", "rgba(0,230,180,0.4)"
            )
        elif self.variant == "danger":
            base = base.replace(
                "rgba(255,255,255,0.15)", "rgba(255,71,87,0.4)"
            ).replace(
                "rgba(255,255,255,0.05)", "rgba(255,71,87,0.2)"
            ).replace(
                "rgba(255,255,255,0.25)", "rgba(255,71,87,0.6)"
            ).replace(
                "rgba(255,255,255,0.1)", "rgba(255,71,87,0.4)"
            )
        
        self.setStyleSheet(base)


class GlassCard(QFrame):
    """Glass morphism card widget"""
    
    def __init__(self, parent=None, strong=False):
        super().__init__(parent)
        self.strong = strong
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            GlassCard {{
                background: {'rgba(255,255,255,0.12)' if strong else 'rgba(255,255,255,0.06)'};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 20px;
            }}
        """)
        
        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)


class SidebarButton(QPushButton):
    """Sidebar navigation button with glass effect"""
    
    def __init__(self, text, icon_text, parent=None):
        super().__init__(f"  {icon_text}  {text}", parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(48)
        self.setMaximumHeight(48)
        self.active = False
        self.update_style()
    
    def set_active(self, active):
        self.active = active
        self.update_style()
    
    def update_style(self):
        if self.active:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(108,92,231,0.5),
                        stop:1 rgba(0,210,255,0.3));
                    border: 1px solid rgba(108,92,231,0.4);
                    border-radius: 14px;
                    color: white;
                    font-weight: 700;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 16px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(108,92,231,0.6),
                        stop:1 rgba(0,210,255,0.4));
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 14px;
                    color: rgba(255,255,255,0.6);
                    font-weight: 500;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 16px;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.08);
                    color: rgba(255,255,255,0.9);
                }
            """)


class AnimatedStackedWidget(QStackedWidget):
    """Stacked widget with slide animation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
    
    def slide_in(self, index):
        if self.currentIndex() == index:
            return
        
        widget = self.widget(index)
        current = self.currentWidget()
        
        self.setCurrentIndex(index)
        
        # Fade animation effect
        widget.setGraphicsEffect(None)


class Sidebar(QWidget):
    """Glass morphism sidebar navigation"""
    
    nav_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setStyleSheet("""
            Sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a1a,
                    stop:0.5 #0d0d20,
                    stop:1 #0a0a1a);
                border-right: 1px solid rgba(255,255,255,0.05);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(4)
        
        # Logo area
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(8, 0, 0, 0)
        
        # Logo icon (using text-based logo)
        logo_icon = QLabel("L")
        logo_icon.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6C5CE7,
                    stop:1 #00D2FF);
                font-size: 28px;
                font-weight: 900;
                background: transparent;
            }
        """)
        logo_layout.addWidget(logo_icon)
        
        logo_text = QLabel("LYFE")
        logo_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 3px;
                background: transparent;
            }
        """)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        
        layout.addWidget(logo_widget)
        
        # Version
        version = QLabel("v3.0.0")
        version.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 10px; padding-left: 8px;")
        version.setContentsMargins(8, 0, 0, 16)
        layout.addWidget(version)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(255,255,255,0.08); max-height: 1px;")
        layout.addWidget(sep)
        layout.addSpacing(12)
        
        # Navigation items
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "Dashboard", "\u2302"),
            ("signals", "AI Signals", "\u26A1"),
            ("trading", "Trading", "\u25B3"),
            ("backtest", "Backtest", "\u25A0"),
            ("news", "News", "\u263D"),
            ("llm", "AI Models", "\u2605"),
            ("tools", "Tools", "\u2692"),
            ("settings", "Settings", "\u2699"),
        ]
        
        for key, label, icon in nav_items:
            btn = SidebarButton(label, icon)
            btn.clicked.connect(lambda checked, k=key: self.on_nav_click(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Bottom status
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(8, 0, 0, 0)
        status_layout.setSpacing(4)
        
        # API status
        self.api_status = QLabel("● Deriv API: Connected")
        self.api_status.setStyleSheet("color: #00E6B4; font-size: 11px; font-weight: 600;")
        status_layout.addWidget(self.api_status)
        
        # LLM status
        self.llm_status = QLabel("● Local LLM: Ready")
        self.llm_status.setStyleSheet("color: #6C5CE7; font-size: 11px; font-weight: 600;")
        status_layout.addWidget(self.llm_status)
        
        layout.addWidget(status_widget)
    
    def on_nav_click(self, key):
        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)
        self.nav_clicked.emit(key)
    
    def set_active(self, key):
        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)
    
    def update_api_status(self, connected, message=""):
        if connected:
            self.api_status.setText(f"● Deriv API: {message or 'Connected'}")
            self.api_status.setStyleSheet("color: #00E6B4; font-size: 11px; font-weight: 600;")
        else:
            self.api_status.setText(f"● Deriv API: {message or 'Disconnected'}")
            self.api_status.setStyleSheet("color: #FF4757; font-size: 11px; font-weight: 600;")
    
    def update_llm_status(self, status, message=""):
        color = "#6C5CE7" if status == "ready" else "#FF4757" if status == "error" else "#FFA502"
        self.llm_status.setText(f"● Local LLM: {message or status.title()}")
        self.llm_status.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 600;")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LYFE - AI Trading Platform")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 950)
        
        # Set application font
        font = QFont("Segoe UI", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        QApplication.setFont(font)
        
        # Initialize core systems
        self.db = DatabaseManager()
        self.deriv_api = DerivAPI()
        self.llm_manager = LLMManager()
        self.backtest_engine = BacktestEngine()
        
        # Set dark palette
        self.setup_dark_theme()
        
        # Build UI
        self.setup_ui()
        
        # Setup auto-refresh timer
        self.setup_timers()
        
        # Connect to Deriv API
        self.connect_deriv()
    
    def setup_dark_theme(self):
        """Configure dark theme with custom palette"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 26))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(15, 15, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 40))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(25, 25, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(palette)
    
    def setup_ui(self):
        """Build main UI layout"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.nav_clicked.connect(self.on_nav_changed)
        layout.addWidget(self.sidebar)
        
        # Main content area with gradient background
        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d0d1f,
                    stop:0.4 #0a0a18,
                    stop:1 #120d20);
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)
        
        # Top bar
        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)
        
        # Stacked widget for views
        self.stack = QStackedWidget()
        
        # Initialize views
        self.views = {}
        
        views_config = [
            ("dashboard", DashboardView, "Dashboard"),
            ("signals", SignalsView, "AI Signals"),
            ("trading", TradingView, "Trading Terminal"),
            ("backtest", BacktestView, "Backtest Engine"),
            ("news", NewsView, "Market News"),
            ("llm", LLMView, "AI Model Manager"),
            ("tools", ToolsView, "Trading Tools"),
            ("settings", SettingsView, "Settings"),
        ]
        
        for key, view_class, title in views_config:
            view = view_class(self.db, self.deriv_api, self.llm_manager, self.backtest_engine)
            view.setProperty("title", title)
            self.views[key] = view
            self.stack.addWidget(view)
        
        content_layout.addWidget(self.stack, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(0,0,0,0.3);
                color: rgba(255,255,255,0.5);
                font-size: 11px;
                border-top: 1px solid rgba(255,255,255,0.05);
            }
        """)
        self.status_bar.showMessage("LYFE v3.0.0 | Ready | All systems operational")
        content_layout.addWidget(self.status_bar)
        
        layout.addWidget(content, 1)
        
        # Set initial view
        self.sidebar.set_active("dashboard")
        self.stack.setCurrentWidget(self.views["dashboard"])
    
    def create_top_bar(self):
        """Create top navigation bar"""
        bar = QWidget()
        bar.setMaximumHeight(60)
        bar.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Page title
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 1px;
            }
        """)
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("\U0001F50E  Search symbols, signals...")
        search.setFixedWidth(300)
        search.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 10px 16px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(108,92,231,0.5);
                background: rgba(255,255,255,0.08);
            }
        """)
        layout.addWidget(search)
        
        layout.addSpacing(16)
        
        # Notification button
        notif_btn = QPushButton("\U0001F514")
        notif_btn.setFixedSize(42, 42)
        notif_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.12);
            }
        """)
        layout.addWidget(notif_btn)
        
        return bar
    
    def on_nav_changed(self, key):
        """Handle navigation change"""
        if key in self.views:
            self.stack.setCurrentWidget(self.views[key])
            title = self.views[key].property("title") or key.title()
            self.page_title.setText(title)
    
    def setup_timers(self):
        """Setup periodic refresh timers"""
        # Market data refresh every 5 seconds
        self.market_timer = QTimer()
        self.market_timer.timeout.connect(self.refresh_market_data)
        self.market_timer.start(5000)
        
        # Clock update every second
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
    
    def refresh_market_data(self):
        """Refresh market data from Deriv API"""
        try:
            # Update all views that need market data
            for key, view in self.views.items():
                if hasattr(view, 'refresh_data'):
                    view.refresh_data()
        except Exception as e:
            print(f"Refresh error: {e}")
    
    def update_clock(self):
        """Update status bar clock"""
        now = datetime.now()
        self.status_bar.showMessage(
            f"LYFE v3.0.0 | {now.strftime('%H:%M:%S')} UTC | All systems operational"
        )
    
    def connect_deriv(self):
        """Connect to Deriv API"""
        try:
            self.deriv_api.connect()
            self.sidebar.update_api_status(True, "Connected")
        except Exception as e:
            self.sidebar.update_api_status(False, str(e))
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.deriv_api.disconnect()
        self.db.close()
        event.accept()


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application metadata
    app.setApplicationName("LYFE")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("LYFE Trading")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
