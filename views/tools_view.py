"""
LYFE - Trading Tools View
Collection of trading calculators and utilities
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QLineEdit, QDoubleSpinBox, QComboBox, QSpinBox, QTabWidget,
    QFormLayout, QGroupBox, QGridLayout, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class ToolsView(BaseView):
    """Trading tools view"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Trading Tools")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: 700;")
        layout.addWidget(title)
        
        # Tools tabs
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
        
        # Position Sizer
        sizer_tab = self.create_position_sizer()
        tabs.addTab(sizer_tab, "Position Sizer")
        
        # Pip Calculator
        pip_tab = self.create_pip_calculator()
        tabs.addTab(pip_tab, "Pip Calculator")
        
        # Risk/Reward
        rr_tab = self.create_risk_reward_calculator()
        tabs.addTab(rr_tab, "Risk/Reward")
        
        # Margin Calculator
        margin_tab = self.create_margin_calculator()
        tabs.addTab(margin_tab, "Margin Calculator")
        
        # Fibonacci
        fib_tab = self.create_fibonacci_tool()
        tabs.addTab(fib_tab, "Fibonacci")
        
        # Pivot Points
        pivot_tab = self.create_pivot_points()
        tabs.addTab(pivot_tab, "Pivot Points")
        
        # Compounding
        compound_tab = self.create_compounding_calculator()
        tabs.addTab(compound_tab, "Compounding")
        
        # Currency Converter
        converter_tab = self.create_currency_converter()
        tabs.addTab(converter_tab, "Converter")
        
        layout.addWidget(tabs)
    
    def create_position_sizer(self):
        """Create position sizing calculator"""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)
        
        # Inputs
        input_group = QGroupBox("Account & Risk Parameters")
        input_group.setStyleSheet("""
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
        form = QFormLayout(input_group)
        form.setSpacing(14)
        
        self.balance_input = QDoubleSpinBox()
        self.balance_input.setRange(100, 10000000)
        self.balance_input.setValue(10000)
        self.balance_input.setDecimals(2)
        self.balance_input.setPrefix("$ ")
        self.balance_input.valueChanged.connect(self.calc_position_size)
        form.addRow("Account Balance:", self.balance_input)
        
        self.risk_input = QDoubleSpinBox()
        self.risk_input.setRange(0.1, 10)
        self.risk_input.setValue(2)
        self.risk_input.setDecimals(1)
        self.risk_input.setSuffix(" %")
        self.risk_input.valueChanged.connect(self.calc_position_size)
        form.addRow("Risk %:", self.risk_input)
        
        self.stop_pips = QDoubleSpinBox()
        self.stop_pips.setRange(1, 10000)
        self.stop_pips.setValue(50)
        self.stop_pips.setDecimals(1)
        self.stop_pips.setSuffix(" pips")
        self.stop_pips.valueChanged.connect(self.calc_position_size)
        form.addRow("Stop Loss:", self.stop_pips)
        
        self.pair_combo = QComboBox()
        self.pair_combo.addItems(["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "BTC/USD"])
        self.pair_combo.currentTextChanged.connect(self.calc_position_size)
        form.addRow("Pair:", self.pair_combo)
        
        layout.addWidget(input_group, 0, 0)
        
        # Results
        result_group = QGroupBox("Position Size Result")
        result_group.setStyleSheet(input_group.styleSheet())
        result_layout = QVBoxLayout(result_group)
        
        self.position_size_result = QLabel("0.40 lots")
        self.position_size_result.setStyleSheet("color: #00D2FF; font-size: 36px; font-weight: 800;")
        self.position_size_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.position_size_result)
        
        self.risk_amount_result = QLabel("Risk: $200.00")
        self.risk_amount_result.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 14px;")
        self.risk_amount_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.risk_amount_result)
        
        self.margin_result = QLabel("Margin required: ~$400")
        self.margin_result.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px;")
        self.margin_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.margin_result)
        
        layout.addWidget(result_group, 0, 1)
        
        # Quick presets
        presets = QGroupBox("Quick Presets")
        presets.setStyleSheet(input_group.styleSheet())
        p_layout = QHBoxLayout(presets)
        
        for preset in ["Conservative (1%)", "Moderate (2%)", "Aggressive (3%)", "Scalper (5%)"]:
            btn = QPushButton(preset)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(108,92,231,0.15);
                    color: rgba(108,92,231,0.9);
                    border: 1px solid rgba(108,92,231,0.2);
                    border-radius: 10px;
                    padding: 10px 16px;
                    font-size: 11px; font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(108,92,231,0.3);
                }
            """)
            p_layout.addWidget(btn)
        
        layout.addWidget(presets, 1, 0, 1, 2)
        
        layout.setRowStretch(2, 1)
        
        return widget
    
    def calc_position_size(self):
        """Calculate position size"""
        balance = self.balance_input.value()
        risk_pct = self.risk_input.value()
        stop_pips = self.stop_pips.value()
        
        # Simplified calculation
        risk_amount = balance * (risk_pct / 100)
        
        # Approximate pip value (simplified)
        pair_pip_values = {
            "EUR/USD": 10, "GBP/USD": 10, "USD/JPY": 9.5,
            "XAU/USD": 10, "BTC/USD": 1
        }
        pip_value = pair_pip_values.get(self.pair_combo.currentText(), 10)
        
        if stop_pips > 0:
            lots = risk_amount / (stop_pips * pip_value)
            lots = round(lots, 2)
        else:
            lots = 0
        
        self.position_size_result.setText(f"{lots:.2f} lots")
        self.risk_amount_result.setText(f"Risk: ${risk_amount:.2f}")
        self.margin_result.setText(f"Margin required: ~${lots * 1000:.0f}")
    
    def create_pip_calculator(self):
        """Create pip calculator"""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)
        
        input_group = QGroupBox("Pip Calculator")
        input_group.setStyleSheet("""
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
        """)
        form = QFormLayout(input_group)
        
        pair = QComboBox()
        pair.addItems(["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "BTC/USD"])
        form.addRow("Pair:", pair)
        
        lot_size = QDoubleSpinBox()
        lot_size.setRange(0.01, 100)
        lot_size.setValue(1.0)
        lot_size.setDecimals(2)
        form.addRow("Lot Size:", lot_size)
        
        pips = QDoubleSpinBox()
        pips.setRange(1, 10000)
        pips.setValue(50)
        form.addRow("Pips:", pips)
        
        layout.addWidget(input_group, 0, 0)
        
        result = QGroupBox("Result")
        result.setStyleSheet(input_group.styleSheet())
        r_layout = QVBoxLayout(result)
        
        val = QLabel("$500.00")
        val.setStyleSheet("color: #00E6B4; font-size: 36px; font-weight: 800;")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(val)
        
        layout.addWidget(result, 0, 1)
        layout.setRowStretch(1, 1)
        
        return widget
    
    def create_risk_reward_calculator(self):
        """Create risk/reward calculator"""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)
        
        input_group = QGroupBox("Trade Parameters")
        input_group.setStyleSheet("""
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
        """)
        form = QFormLayout(input_group)
        
        entry = QDoubleSpinBox()
        entry.setRange(0.00001, 999999)
        entry.setValue(1.0824)
        entry.setDecimals(5)
        form.addRow("Entry Price:", entry)
        
        sl = QDoubleSpinBox()
        sl.setRange(0.00001, 999999)
        sl.setValue(1.0798)
        sl.setDecimals(5)
        form.addRow("Stop Loss:", sl)
        
        tp = QDoubleSpinBox()
        tp.setRange(0.00001, 999999)
        tp.setValue(1.0876)
        tp.setDecimals(5)
        form.addRow("Take Profit:", tp)
        
        layout.addWidget(input_group, 0, 0)
        
        result = QGroupBox("Risk/Reward Analysis")
        result.setStyleSheet(input_group.styleSheet())
        r_layout = QVBoxLayout(result)
        
        rr_label = QLabel("R:R = 1:2.0")
        rr_label.setStyleSheet("color: #00D2FF; font-size: 28px; font-weight: 800;")
        rr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(rr_label)
        
        risk_pips = QLabel("Risk: 26.0 pips")
        risk_pips.setStyleSheet("color: #FF4757; font-size: 14px;")
        risk_pips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(risk_pips)
        
        reward_pips = QLabel("Reward: 52.0 pips")
        reward_pips.setStyleSheet("color: #00E6B4; font-size: 14px;")
        reward_pips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(reward_pips)
        
        layout.addWidget(result, 0, 1)
        layout.setRowStretch(1, 1)
        
        return widget
    
    def create_margin_calculator(self):
        """Create margin calculator"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Margin Calculator")
        group.setStyleSheet("""
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
        """)
        form = QFormLayout(group)
        
        pair = QComboBox()
        pair.addItems(["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "BTC/USD"])
        form.addRow("Pair:", pair)
        
        lots = QDoubleSpinBox()
        lots.setRange(0.01, 100)
        lots.setValue(1.0)
        lots.setDecimals(2)
        form.addRow("Lots:", lots)
        
        leverage = QComboBox()
        leverage.addItems(["1:30", "1:50", "1:100", "1:200", "1:500"])
        leverage.setCurrentText("1:100")
        form.addRow("Leverage:", leverage)
        
        result = QLabel("Required Margin: $1,082.40")
        result.setStyleSheet("color: #00D2FF; font-size: 24px; font-weight: 800;")
        result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addRow(result)
        
        layout.addWidget(group)
        layout.addStretch()
        return widget
    
    def create_fibonacci_tool(self):
        """Create Fibonacci retracement tool"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Fibonacci Retracement")
        group.setStyleSheet("""
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
        """)
        form = QFormLayout(group)
        
        high = QDoubleSpinBox()
        high.setRange(0, 999999)
        high.setValue(1.0950)
        high.setDecimals(5)
        form.addRow("Swing High:", high)
        
        low = QDoubleSpinBox()
        low.setRange(0, 999999)
        low.setValue(1.0700)
        low.setDecimals(5)
        form.addRow("Swing Low:", low)
        
        layout.addWidget(group)
        
        # Fib levels
        levels = QGroupBox("Fibonacci Levels")
        levels.setStyleSheet(group.styleSheet())
        l_layout = QVBoxLayout(levels)
        
        fib_data = [
            ("0%", "1.0950"), ("23.6%", "1.0891"), ("38.2%", "1.0855"),
            ("50%", "1.0825"), ("61.8%", "1.0795"), ("78.6%", "1.0753"), ("100%", "1.0700")
        ]
        
        for level, price in fib_data:
            row = QHBoxLayout()
            
            lbl = QLabel(level)
            lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 13px; width: 60px;")
            row.addWidget(lbl)
            
            bar = QProgressBar()
            bar.setValue(100 - int(float(level.replace("%", ""))))
            bar.setTextVisible(False)
            bar.setFixedHeight(20)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    background: rgba(255,255,255,0.05);
                    border-radius: 4px;
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6C5CE7, stop:1 #00D2FF);
                    border-radius: 4px;
                }}
            """)
            row.addWidget(bar, 1)
            
            val = QLabel(price)
            val.setStyleSheet("color: white; font-size: 13px; font-weight: 600; width: 70px;")
            val.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(val)
            
            l_layout.addLayout(row)
        
        layout.addWidget(levels)
        layout.addStretch()
        return widget
    
    def create_pivot_points(self):
        """Create pivot points calculator"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Pivot Points (Classic)")
        group.setStyleSheet("""
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
        """)
        form = QFormLayout(group)
        
        high = QDoubleSpinBox()
        high.setValue(1.0850)
        high.setDecimals(5)
        form.addRow("Previous High:", high)
        
        low = QDoubleSpinBox()
        low.setValue(1.0750)
        low.setDecimals(5)
        form.addRow("Previous Low:", low)
        
        close = QDoubleSpinBox()
        close.setValue(1.0824)
        close.setDecimals(5)
        form.addRow("Previous Close:", close)
        
        layout.addWidget(group)
        
        # Results
        result = QGroupBox("Calculated Levels")
        result.setStyleSheet(group.styleSheet())
        r_layout = QVBoxLayout(result)
        
        levels = [
            ("R3", "1.0983", "#FF4757"), ("R2", "1.0933", "#FF6B6B"),
            ("R1", "1.0878", "#FFA502"), ("PP", "1.0824", "#00D2FF"),
            ("S1", "1.0770", "#FFA502"), ("S2", "1.0715", "#FF6B6B"),
            ("S3", "1.0665", "#FF4757"),
        ]
        
        for name, price, color in levels:
            row = QHBoxLayout()
            
            lbl = QLabel(name)
            lbl.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 700; width: 40px;")
            row.addWidget(lbl)
            
            row.addStretch()
            
            val = QLabel(price)
            val.setStyleSheet(f"color: white; font-size: 14px; font-weight: 600;")
            row.addWidget(val)
            
            r_layout.addLayout(row)
        
        layout.addWidget(result)
        layout.addStretch()
        return widget
    
    def create_compounding_calculator(self):
        """Create compounding calculator"""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)
        
        input_group = QGroupBox("Compounding Parameters")
        input_group.setStyleSheet("""
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
        """)
        form = QFormLayout(input_group)
        
        initial = QDoubleSpinBox()
        initial.setRange(100, 10000000)
        initial.setValue(1000)
        initial.setPrefix("$ ")
        form.addRow("Initial Capital:", initial)
        
        monthly_return = QDoubleSpinBox()
        monthly_return.setRange(0.1, 100)
        monthly_return.setValue(10)
        monthly_return.setSuffix(" %")
        form.addRow("Monthly Return:", monthly_return)
        
        months = QSpinBox()
        months.setRange(1, 120)
        months.setValue(12)
        form.addRow("Months:", months)
        
        layout.addWidget(input_group, 0, 0)
        
        result = QGroupBox("Projected Results")
        result.setStyleSheet(input_group.styleSheet())
        r_layout = QVBoxLayout(result)
        
        final_balance = QLabel("$3,138.43")
        final_balance.setStyleSheet("color: #00E6B4; font-size: 32px; font-weight: 800;")
        final_balance.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(final_balance)
        
        profit = QLabel("Total Profit: $2,138.43")
        profit.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 14px;")
        profit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(profit)
        
        roi = QLabel("ROI: 213.8%")
        roi.setStyleSheet("color: #00D2FF; font-size: 16px; font-weight: 700;")
        roi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(roi)
        
        layout.addWidget(result, 0, 1)
        layout.setRowStretch(1, 1)
        
        return widget
    
    def create_currency_converter(self):
        """Create currency converter"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Currency Converter")
        group.setStyleSheet("""
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
        """)
        form = QFormLayout(group)
        
        amount = QDoubleSpinBox()
        amount.setRange(0, 999999999)
        amount.setValue(1000)
        amount.setDecimals(2)
        form.addRow("Amount:", amount)
        
        from_currency = QComboBox()
        from_currency.addItems(["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"])
        form.addRow("From:", from_currency)
        
        to_currency = QComboBox()
        to_currency.addItems(["EUR", "USD", "GBP", "JPY", "AUD", "CAD", "CHF"])
        to_currency.setCurrentText("EUR")
        form.addRow("To:", to_currency)
        
        result = QLabel("\u20AC 920.50")
        result.setStyleSheet("color: #00D2FF; font-size: 28px; font-weight: 800;")
        result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addRow("Result:", result)
        
        rate = QLabel("1 USD = 0.9205 EUR")
        rate.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px;")
        rate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addRow(rate)
        
        layout.addWidget(group)
        layout.addStretch()
        return widget
    
    def refresh_data(self):
        pass
