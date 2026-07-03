"""
LYFE - Settings View
Application settings and configuration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
    QSlider, QTabWidget, QFormLayout, QGroupBox, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class SettingsView(BaseView):
    """Settings view"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: 700;")
        layout.addWidget(title)
        
        # Settings tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
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
        
        # Account tab
        account_tab = self.create_account_tab()
        tabs.addTab(account_tab, "Account")
        
        # API tab
        api_tab = self.create_api_tab()
        tabs.addTab(api_tab, "API Keys")
        
        # Trading tab
        trading_tab = self.create_trading_tab()
        tabs.addTab(trading_tab, "Trading")
        
        # AI tab
        ai_tab = self.create_ai_tab()
        tabs.addTab(ai_tab, "AI Settings")
        
        # Notifications tab
        notif_tab = self.create_notifications_tab()
        tabs.addTab(notif_tab, "Notifications")
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        tabs.addTab(appearance_tab, "Appearance")
        
        # Storage tab
        storage_tab = self.create_storage_tab()
        tabs.addTab(storage_tab, "Storage")
        
        layout.addWidget(tabs)
    
    def create_account_tab(self):
        """Create account settings tab"""
        scroll = QWidget()
        layout = QVBoxLayout(scroll)
        layout.setSpacing(20)
        
        # Profile
        profile = QGroupBox("Profile")
        profile.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        form = QFormLayout(profile)
        form.setSpacing(14)
        
        name = QLineEdit("Trader")
        form.addRow("Display Name:", name)
        
        email = QLineEdit("trader@example.com")
        form.addRow("Email:", email)
        
        account_type = QLabel("PRO Plan")
        account_type.setStyleSheet("color: #00D2FF; font-weight: 700;")
        form.addRow("Account Type:", account_type)
        
        layout.addWidget(profile)
        
        # Security
        security = QGroupBox("Security")
        security.setStyleSheet(profile.styleSheet())
        s_form = QFormLayout(security)
        
        change_pass = QPushButton("Change Password")
        change_pass.setStyleSheet("""
            QPushButton {
                background: rgba(108,92,231,0.2);
                color: #6C5CE7;
                border: 1px solid rgba(108,92,231,0.3);
                border-radius: 10px;
                padding: 10px;
                font-size: 12px; font-weight: 600;
            }
        """)
        s_form.addRow(change_pass)
        
        two_fa = QCheckBox("Enable Two-Factor Authentication")
        two_fa.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 13px;")
        s_form.addRow(two_fa)
        
        layout.addWidget(security)
        layout.addStretch()
        
        return scroll
    
    def create_api_tab(self):
        """Create API settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # Deriv API
        deriv = QGroupBox("Deriv API Configuration")
        deriv.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        d_form = QFormLayout(deriv)
        d_form.setSpacing(14)
        
        use_default = QCheckBox("Use default public API (app_id=1089)")
        use_default.setChecked(True)
        use_default.setStyleSheet("color: rgba(255,255,255,0.8);")
        d_form.addRow(use_default)
        
        api_key = QLineEdit()
        api_key.setPlaceholderText("Enter your Deriv API token (optional)")
        api_key.setEchoMode(QLineEdit.EchoMode.Password)
        d_form.addRow("API Token:", api_key)
        
        app_id = QLineEdit("1089")
        d_form.addRow("App ID:", app_id)
        
        test_btn = QPushButton("Test Connection")
        test_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C5CE7, stop:1 #00D2FF);
                color: white; border: none;
                border-radius: 10px;
                padding: 10px 24px;
                font-size: 12px; font-weight: 700;
            }
        """)
        d_form.addRow(test_btn)
        
        layout.addWidget(deriv)
        
        # Custom API for automated trading
        auto = QGroupBox("Automated Trading API")
        auto.setStyleSheet(deriv.styleSheet())
        a_form = QFormLayout(auto)
        
        enable_auto = QCheckBox("Enable automated trading")
        enable_auto.setStyleSheet("color: rgba(255,255,255,0.8);")
        a_form.addRow(enable_auto)
        
        custom_api = QLineEdit()
        custom_api.setPlaceholderText("Your custom API endpoint")
        a_form.addRow("Custom API URL:", custom_api)
        
        webhook = QLineEdit()
        webhook.setPlaceholderText("Webhook URL for signals")
        a_form.addRow("Webhook URL:", webhook)
        
        layout.addWidget(auto)
        layout.addStretch()
        
        return widget
    
    def create_trading_tab(self):
        """Create trading settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # Risk settings
        risk = QGroupBox("Risk Management")
        risk.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        form = QFormLayout(risk)
        
        risk_per_trade = QDoubleSpinBox()
        risk_per_trade.setRange(0.1, 10)
        risk_per_trade.setValue(2.0)
        risk_per_trade.setSuffix(" %")
        form.addRow("Risk Per Trade:", risk_per_trade)
        
        max_daily_loss = QDoubleSpinBox()
        max_daily_loss.setRange(1, 50)
        max_daily_loss.setValue(5)
        max_daily_loss.setSuffix(" %")
        form.addRow("Max Daily Loss:", max_daily_loss)
        
        max_positions = QSpinBox()
        max_positions.setRange(1, 50)
        max_positions.setValue(10)
        form.addRow("Max Open Positions:", max_positions)
        
        default_sl = QSpinBox()
        default_sl.setRange(10, 1000)
        default_sl.setValue(50)
        default_sl.setSuffix(" pips")
        form.addRow("Default Stop Loss:", default_sl)
        
        default_tp = QSpinBox()
        default_tp.setRange(10, 5000)
        default_tp.setValue(100)
        default_tp.setSuffix(" pips")
        form.addRow("Default Take Profit:", default_tp)
        
        leverage = QComboBox()
        leverage.addItems(["1:30", "1:50", "1:100", "1:200", "1:500"])
        leverage.setCurrentText("1:100")
        form.addRow("Default Leverage:", leverage)
        
        layout.addWidget(risk)
        
        # Execution
        exec_group = QGroupBox("Execution Settings")
        exec_group.setStyleSheet(risk.styleSheet())
        e_form = QFormLayout(exec_group)
        
        one_click = QCheckBox("Enable one-click trading")
        one_click.setStyleSheet("color: rgba(255,255,255,0.8);")
        e_form.addRow(one_click)
        
        confirm = QCheckBox("Show trade confirmation dialog")
        confirm.setChecked(True)
        confirm.setStyleSheet("color: rgba(255,255,255,0.8);")
        e_form.addRow(confirm)
        
        partial_close = QCheckBox("Allow partial close")
        partial_close.setChecked(True)
        partial_close.setStyleSheet("color: rgba(255,255,255,0.8);")
        e_form.addRow(partial_close)
        
        layout.addWidget(exec_group)
        layout.addStretch()
        
        return widget
    
    def create_ai_tab(self):
        """Create AI settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # LLM Settings
        llm = QGroupBox("Local LLM Settings")
        llm.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        form = QFormLayout(llm)
        
        models_dir = QLineEdit()
        models_dir.setText(str(self.llm_manager.models_dir))
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet("""
            QPushButton {
                background: rgba(108,92,231,0.2);
                color: #6C5CE7;
                border: 1px solid rgba(108,92,231,0.3);
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 11px; font-weight: 600;
            }
        """)
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(models_dir)
        dir_layout.addWidget(browse_btn)
        form.addRow("Models Directory:", dir_layout)
        
        default_ctx = QSpinBox()
        default_ctx.setRange(512, 32768)
        default_ctx.setValue(8192)
        default_ctx.setSingleStep(512)
        form.addRow("Default Context:", default_ctx)
        
        gpu_layers = QSpinBox()
        gpu_layers.setRange(0, 100)
        gpu_layers.setValue(0)
        form.addRow("GPU Layers:", gpu_layers)
        
        layout.addWidget(llm)
        
        # Signal Generation
        signals = QGroupBox("AI Signal Generation")
        signals.setStyleSheet(llm.styleSheet())
        s_form = QFormLayout(signals)
        
        auto_signals = QCheckBox("Enable AI signal generation")
        auto_signals.setChecked(True)
        auto_signals.setStyleSheet("color: rgba(255,255,255,0.8);")
        s_form.addRow(auto_signals)
        
        confidence = QSlider(Qt.Orientation.Horizontal)
        confidence.setRange(50, 99)
        confidence.setValue(75)
        s_form.addRow("Min Confidence:", confidence)
        
        strategies = QCheckBox("Use TopDown Analysis")
        strategies.setChecked(True)
        strategies.setStyleSheet("color: rgba(255,255,255,0.8);")
        s_form.addRow(strategies)
        
        self_learn = QCheckBox("Enable self-learning feedback loop")
        self_learn.setChecked(True)
        self_learn.setStyleSheet("color: rgba(255,255,255,0.8);")
        s_form.addRow(self_learn)
        
        layout.addWidget(signals)
        layout.addStretch()
        
        return widget
    
    def create_notifications_tab(self):
        """Create notifications settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # Push Notifications
        push = QGroupBox("Push Notifications")
        push.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        form = QFormLayout(push)
        
        new_signals = QCheckBox("New AI signals")
        new_signals.setChecked(True)
        new_signals.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(new_signals)
        
        tp_sl = QCheckBox("Take Profit / Stop Loss hits")
        tp_sl.setChecked(True)
        tp_sl.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(tp_sl)
        
        news_events = QCheckBox("High-impact news events")
        news_events.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(news_events)
        
        price_alerts = QCheckBox("Price level alerts")
        price_alerts.setChecked(True)
        price_alerts.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(price_alerts)
        
        layout.addWidget(push)
        
        # Sound
        sound = QGroupBox("Sound Alerts")
        sound.setStyleSheet(push.styleSheet())
        s_form = QFormLayout(sound)
        
        enable_sound = QCheckBox("Enable sound notifications")
        enable_sound.setChecked(True)
        enable_sound.setStyleSheet("color: rgba(255,255,255,0.8);")
        s_form.addRow(enable_sound)
        
        volume = QSlider(Qt.Orientation.Horizontal)
        volume.setRange(0, 100)
        volume.setValue(70)
        s_form.addRow("Volume:", volume)
        
        layout.addWidget(sound)
        layout.addStretch()
        
        return widget
    
    def create_appearance_tab(self):
        """Create appearance settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        theme = QGroupBox("Theme")
        theme.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        form = QFormLayout(theme)
        
        theme_select = QComboBox()
        theme_select.addItems(["Dark (Default)", "Deep Purple", "Ocean Blue", "Midnight"])
        form.addRow("Theme:", theme_select)
        
        glass_effect = QCheckBox("Enable glass morphism effects")
        glass_effect.setChecked(True)
        glass_effect.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(glass_effect)
        
        animations = QCheckBox("Enable animations")
        animations.setChecked(True)
        animations.setStyleSheet("color: rgba(255,255,255,0.8);")
        form.addRow(animations)
        
        layout.addWidget(theme)
        layout.addStretch()
        
        return widget
    
    def create_storage_tab(self):
        """Create storage settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        storage = QGroupBox("Local Storage")
        storage.setStyleSheet("""
            QGroupBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                margin-top: 16px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 16px;
                color: rgba(255,255,255,0.7);
            }
        """)
        s_layout = QVBoxLayout(storage)
        
        usage = QLabel("Storage Usage: 128 MB")
        usage.setStyleSheet("color: white; font-size: 14px;")
        s_layout.addWidget(usage)
        
        breakdown = QLabel("Signals: 45 MB | History: 52 MB | Models: 0 MB | Cache: 31 MB")
        breakdown.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px;")
        s_layout.addWidget(breakdown)
        
        btn_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export Data")
        export_btn.setStyleSheet("""
            QPushButton {
                background: rgba(108,92,231,0.2);
                color: #6C5CE7;
                border: 1px solid rgba(108,92,231,0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 12px; font-weight: 600;
            }
        """)
        btn_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("Clear Cache")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,71,87,0.2);
                color: #FF4757;
                border: 1px solid rgba(255,71,87,0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 12px; font-weight: 600;
            }
        """)
        btn_layout.addWidget(clear_btn)
        
        s_layout.addLayout(btn_layout)
        
        layout.addWidget(storage)
        layout.addStretch()
        
        return widget
    
    def refresh_data(self):
        pass
