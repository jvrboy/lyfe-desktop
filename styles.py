"""
LYFE - Glass Morphism Styles & Animations
"""

# Main QSS stylesheet for glass morphism
GLASS_STYLES = """
/* Global */
QMainWindow {
    background: #0a0a1a;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255,255,255,0.2);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 6px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(255,255,255,0.2);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Line Edit */
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

QLineEdit::placeholder {
    color: rgba(255,255,255,0.3);
}

/* Combo Box */
QComboBox {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px 16px;
    color: white;
    font-size: 13px;
    min-width: 120px;
}

QComboBox:hover {
    background: rgba(255,255,255,0.1);
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background: #1a1a2e;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    color: white;
    selection-background-color: rgba(108,92,231,0.4);
    padding: 8px;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px;
    color: white;
    font-size: 13px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid rgba(108,92,231,0.5);
}

/* Text Edit */
QTextEdit, QPlainTextEdit {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 16px;
    color: white;
    font-size: 13px;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid rgba(108,92,231,0.4);
}

/* Table */
QTableWidget {
    background: transparent;
    border: none;
    gridline-color: rgba(255,255,255,0.03);
    color: white;
    font-size: 12px;
}

QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}

QTableWidget::item:selected {
    background: rgba(108,92,231,0.2);
    color: white;
}

QHeaderView::section {
    background: transparent;
    color: rgba(255,255,255,0.5);
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

QHeaderView::section:hover {
    color: white;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background: transparent;
}

QTabBar::tab {
    background: transparent;
    color: rgba(255,255,255,0.5);
    padding: 12px 24px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
    font-weight: 500;
}

QTabBar::tab:selected {
    color: white;
    border-bottom: 2px solid #6C5CE7;
}

QTabBar::tab:hover:!selected {
    color: rgba(255,255,255,0.8);
    border-bottom: 2px solid rgba(108,92,231,0.3);
}

/* Check Box */
QCheckBox {
    color: white;
    font-size: 13px;
    spacing: 10px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #6C5CE7,
        stop:1 #00D2FF);
    border: 2px solid #6C5CE7;
}

QCheckBox::indicator:hover {
    border: 2px solid rgba(108,92,231,0.5);
}

/* Slider */
QSlider::groove:horizontal {
    height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6C5CE7,
        stop:1 #00D2FF);
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: white;
    width: 18px;
    height: 18px;
    border-radius: 9px;
    margin: -6px 0;
}

QSlider::handle:horizontal:hover {
    background: #6C5CE7;
}

/* Group Box */
QGroupBox {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    margin-top: 16px;
    padding: 20px;
    color: white;
    font-size: 13px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 16px;
    color: rgba(255,255,255,0.7);
}

/* Menu */
QMenu {
    background: #1a1a2e;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 8px;
    color: white;
}

QMenu::item {
    padding: 10px 24px;
    border-radius: 8px;
}

QMenu::item:selected {
    background: rgba(108,92,231,0.3);
}

QMenu::separator {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 6px 12px;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    height: 8px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    border-radius: 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6C5CE7,
        stop:1 #00D2FF);
}

/* Dialog */
QDialog {
    background: #0f0f1f;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
}

QDialogButtonBox QPushButton {
    min-width: 100px;
}
"""

# Animation configuration
ANIMATIONS = {
    "fade_duration": 300,
    "slide_duration": 400,
    "pulse_duration": 2000,
    "glow_duration": 3000,
}

# Color palette
COLORS = {
    "primary": "#6C5CE7",
    "secondary": "#00D2FF",
    "accent": "#FF6B6B",
    "success": "#00E6B4",
    "danger": "#FF4757",
    "warning": "#FFA502",
    "bg_dark": "#0a0a1a",
    "bg_card": "rgba(255,255,255,0.06)",
    "bg_card_strong": "rgba(255,255,255,0.12)",
    "text_primary": "#FFFFFF",
    "text_secondary": "rgba(255,255,255,0.6)",
    "text_muted": "rgba(255,255,255,0.3)",
    "border": "rgba(255,255,255,0.1)",
    "gradient_primary": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6C5CE7, stop:1 #00D2FF)",
}

# Glass card stylesheet generators
def glass_card(strong=False, radius=20):
    """Generate glass card stylesheet"""
    bg = "rgba(255,255,255,0.12)" if strong else "rgba(255,255,255,0.06)"
    return f"""
        background: {bg};
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: {radius}px;
    """

def glass_button(variant="default", radius=12):
    """Generate glass button stylesheet"""
    colors = {
        "default": ("rgba(255,255,255,0.15)", "rgba(255,255,255,0.25)", "rgba(255,255,255,0.1)"),
        "primary": ("rgba(108,92,231,0.5)", "rgba(108,92,231,0.7)", "rgba(108,92,231,0.6)"),
        "success": ("rgba(0,230,180,0.4)", "rgba(0,230,180,0.6)", "rgba(0,230,180,0.5)"),
        "danger": ("rgba(255,71,87,0.4)", "rgba(255,71,87,0.6)", "rgba(255,71,87,0.5)"),
    }
    
    normal, hover, pressed = colors.get(variant, colors["default"])
    
    return f"""
        QPushButton {{
            background: {normal};
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: {radius}px;
            padding: 10px 20px;
            color: white;
            font-weight: 600;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: {hover};
            border: 1px solid rgba(255,255,255,0.2);
        }}
        QPushButton:pressed {{
            background: {pressed};
        }}
    """
