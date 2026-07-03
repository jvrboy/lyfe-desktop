"""
LYFE - Base View Class
All views inherit from this base class
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QFont


class BaseView(QWidget):
    """Base class for all views"""
    
    def __init__(self, db, deriv_api, llm_manager, backtest_engine, parent=None):
        super().__init__(parent)
        self.db = db
        self.deriv_api = deriv_api
        self.llm_manager = llm_manager
        self.backtest_engine = backtest_engine
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Override in subclass"""
        pass
    
    def load_data(self):
        """Override in subclass"""
        pass
    
    def refresh_data(self):
        """Override in subclass"""
        pass
    
    def paintEvent(self, event):
        """Custom paint for gradient background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Subtle gradient overlay
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(13, 13, 31, 50))
        gradient.setColorAt(0.5, QColor(10, 10, 24, 30))
        gradient.setColorAt(1, QColor(18, 13, 32, 50))
        
        painter.fillRect(self.rect(), gradient)
        painter.end()
    
    def create_card(self, title="", strong=False):
        """Create a glass card widget"""
        card = QFrame()
        bg = "rgba(255,255,255,0.10)" if strong else "rgba(255,255,255,0.06)"
        card.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                color: rgba(255,255,255,0.6);
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 2px;
            """)
            layout.addWidget(title_label)
        
        return card, layout
    
    def create_stat_card(self, label, value, change=None, color="white"):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            color: rgba(255,255,255,0.5);
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        """)
        layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(value_widget)
        
        if change:
            change_widget = QLabel(change)
            is_positive = "+" in change
            change_color = "#00E6B4" if is_positive else "#FF4757"
            change_widget.setStyleSheet(f"""
                color: {change_color};
                font-size: 12px;
                font-weight: 600;
            """)
            layout.addWidget(change_widget)
        
        return card
    
    def style_number(self, value, prefix="", suffix="", decimals=2):
        """Format number for display"""
        try:
            formatted = f"{float(value):,.{decimals}f}"
            return f"{prefix}{formatted}{suffix}"
        except:
            return f"{prefix}{value}{suffix}"
