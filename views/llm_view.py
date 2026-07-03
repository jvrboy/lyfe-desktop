"""
LYFE - AI Model Manager View
GGUF model management and chat interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QComboBox, QSpinBox, QLineEdit, QTextEdit, QFileDialog,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QListWidget, QListWidgetItem, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor

from views.base_view import BaseView


class ModelLoadThread(QThread):
    """Thread for loading models"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, llm_manager, model_path, n_ctx, n_gpu_layers):
        super().__init__()
        self.llm_manager = llm_manager
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
    
    def run(self):
        self.progress.emit("Loading model...")
        def callback(status, message):
            self.progress.emit(message)
        
        success = self.llm_manager.load_model(
            self.model_path, self.n_ctx, self.n_gpu_layers, callback
        )
        self.finished.emit(success, "Model loaded" if success else "Failed")


class LLMView(BaseView):
    """AI Model Manager view"""
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Model management
        left = self.create_model_panel()
        splitter.addWidget(left)
        
        # Right panel - Chat interface
        right = self.create_chat_panel()
        splitter.addWidget(right)
        
        splitter.setSizes([400, 800])
        layout.addWidget(splitter)
    
    def create_model_panel(self):
        """Create model management panel"""
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
        title = QLabel("AI MODEL MANAGER")
        title.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)
        
        # Status
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("""
            background: rgba(0,230,180,0.1);
            border: 1px solid rgba(0,230,180,0.3);
            border-radius: 12px;
        """)
        sf_layout = QHBoxLayout(self.status_frame)
        sf_layout.setContentsMargins(16, 12, 16, 12)
        
        self.status_label = QLabel("\u25CF No Model Loaded")
        self.status_label.setStyleSheet("color: #00E6B4; font-size: 13px; font-weight: 600;")
        sf_layout.addWidget(self.status_label)
        sf_layout.addStretch()
        
        layout.addWidget(self.status_frame)
        
        # Model list
        models_title = QLabel("Installed Models")
        models_title.setStyleSheet("color: white; font-size: 14px; font-weight: 700;")
        layout.addWidget(models_title)
        
        self.models_list = QTableWidget()
        self.models_list.setColumnCount(4)
        self.models_list.setHorizontalHeaderLabels(["Name", "Size", "Quant", "Status"])
        self.models_list.setStyleSheet("""
            QTableWidget {
                background: transparent; border: none;
                color: white; font-size: 12px;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.03); }
            QHeaderView::section {
                background: transparent; color: rgba(255,255,255,0.5);
                padding: 8px; border: none; border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 10px; font-weight: 600; text-transform: uppercase;
            }
        """)
        self.models_list.horizontalHeader().setStretchLastSection(True)
        self.load_models_list()
        layout.addWidget(self.models_list)
        
        # Add model button
        add_btn = QPushButton("+ Add GGUF Model")
        add_btn.setStyleSheet("""
            QPushButton {
                background: rgba(108,92,231,0.3);
                color: #6C5CE7;
                border: 1px solid rgba(108,92,231,0.5);
                border-radius: 12px;
                padding: 12px;
                font-size: 12px; font-weight: 700;
            }
            QPushButton:hover {
                background: rgba(108,92,231,0.5);
            }
        """)
        add_btn.clicked.connect(self.add_model)
        layout.addWidget(add_btn)
        
        # Load/Unload
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Selected")
        load_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C5CE7, stop:1 #00D2FF);
                color: white; border: none; border-radius: 10px;
                padding: 10px 20px; font-size: 12px; font-weight: 700;
            }
        """)
        load_btn.clicked.connect(self.load_selected_model)
        btn_layout.addWidget(load_btn)
        
        unload_btn = QPushButton("Unload")
        unload_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,71,87,0.3);
                color: #FF4757; border: 1px solid rgba(255,71,87,0.4);
                border-radius: 10px;
                padding: 10px 20px; font-size: 12px; font-weight: 700;
            }
        """)
        unload_btn.clicked.connect(self.unload_model)
        btn_layout.addWidget(unload_btn)
        
        layout.addLayout(btn_layout)
        
        # Settings
        settings = QFrame()
        settings.setStyleSheet("background: rgba(0,0,0,0.2); border-radius: 12px;")
        st_layout = QVBoxLayout(settings)
        st_layout.setContentsMargins(16, 16, 16, 16)
        
        ctx_label = QLabel("Context Length")
        ctx_label.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
        st_layout.addWidget(ctx_label)
        
        self.ctx_spin = QSpinBox()
        self.ctx_spin.setRange(512, 32768)
        self.ctx_spin.setValue(8192)
        self.ctx_spin.setSingleStep(512)
        st_layout.addWidget(self.ctx_spin)
        
        gpu_label = QLabel("GPU Layers")
        gpu_label.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
        st_layout.addWidget(gpu_label)
        
        self.gpu_spin = QSpinBox()
        self.gpu_spin.setRange(0, 100)
        self.gpu_spin.setValue(0)
        st_layout.addWidget(self.gpu_spin)
        
        layout.addWidget(settings)
        layout.addStretch()
        
        return panel
    
    def create_chat_panel(self):
        """Create chat interface panel"""
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
        
        # Header
        header = QHBoxLayout()
        
        chat_title = QLabel("AI Chat Assistant")
        chat_title.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
        header.addWidget(chat_title)
        
        header.addStretch()
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: rgba(255,255,255,0.5);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; padding: 6px 16px;
                font-size: 11px; font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.08);
                color: white;
            }
        """)
        clear_btn.clicked.connect(self.clear_chat)
        header.addWidget(clear_btn)
        
        layout.addLayout(header)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background: rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 16px;
                color: white;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.chat_history, 1)
        
        # Quick prompts
        prompts = QHBoxLayout()
        for prompt in ["Analyze EUR/USD", "Trading Strategy", "Risk Assessment", "Market Outlook"]:
            p_btn = QPushButton(prompt)
            p_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(108,92,231,0.15);
                    color: rgba(108,92,231,0.9);
                    border: 1px solid rgba(108,92,231,0.2);
                    border-radius: 10px;
                    padding: 8px 16px;
                    font-size: 11px; font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(108,92,231,0.3);
                }
            """)
            p_btn.clicked.connect(lambda checked, p=prompt: self.send_quick(p))
            prompts.addWidget(p_btn)
        prompts.addStretch()
        layout.addLayout(prompts)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask the AI about markets, strategies, analysis...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 14px;
                padding: 14px 20px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(108,92,231,0.5);
            }
        """)
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        send_btn = QPushButton("\u2192")
        send_btn.setFixedSize(48, 48)
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6C5CE7, stop:1 #00D2FF);
                color: white; border: none;
                border-radius: 14px;
                font-size: 20px; font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7D6DF8, stop:1 #11E3FF);
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        return panel
    
    def load_models_list(self):
        """Load available models"""
        models = self.llm_manager.scan_models()
        
        if not models:
            # Add placeholder
            models = [
                {"name": "llama-3.1-8b-instruct-Q4_K_M", "size_gb": 4.7, "quantization": "Q4_K_M", "is_loaded": False},
                {"name": "mistral-7b-instruct-v0.3-Q5_K_M", "size_gb": 5.4, "quantization": "Q5_K_M", "is_loaded": False},
                {"name": "codellama-13b-python-Q4_K_M", "size_gb": 8.2, "quantization": "Q4_K_M", "is_loaded": False},
            ]
        
        self.models_list.setRowCount(len(models))
        for i, model in enumerate(models):
            self.models_list.setItem(i, 0, QTableWidgetItem(model["name"]))
            self.models_list.setItem(i, 1, QTableWidgetItem(f"{model['size_gb']} GB"))
            self.models_list.setItem(i, 2, QTableWidgetItem(model["quantization"]))
            
            status = "Loaded" if model.get("is_loaded") else "Ready"
            status_item = QTableWidgetItem(status)
            if model.get("is_loaded"):
                status_item.setForeground(QColor("#00E6B4"))
            self.models_list.setItem(i, 3, status_item)
    
    def add_model(self):
        """Add a GGUF model file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select GGUF Model", "", "GGUF Files (*.gguf)"
        )
        if file_path:
            # Copy to models directory
            import shutil
            dest = self.llm_manager.models_dir / Path(file_path).name
            shutil.copy2(file_path, dest)
            self.load_models_list()
    
    def load_selected_model(self):
        """Load selected model"""
        row = self.models_list.currentRow()
        if row < 0:
            self.chat_history.append("<p style='color: #FF4757'>Please select a model first.</p>")
            return
        
        model_name = self.models_list.item(row, 0).text()
        models_dir = self.llm_manager.models_dir
        model_path = str(models_dir / f"{model_name}.gguf")
        
        self.status_label.setText("\u25CF Loading...")
        self.status_label.setStyleSheet("color: #FFA502; font-size: 13px; font-weight: 600;")
        
        # Start loading thread
        self.load_thread = ModelLoadThread(
            self.llm_manager, model_path,
            self.ctx_spin.value(), self.gpu_spin.value()
        )
        self.load_thread.progress.connect(self.on_load_progress)
        self.load_thread.finished.connect(self.on_load_finished)
        self.load_thread.start()
    
    def on_load_progress(self, message):
        """Handle load progress"""
        self.chat_history.append(f"<p style='color: #6C5CE7'>[System] {message}</p>")
    
    def on_load_finished(self, success, message):
        """Handle load completion"""
        if success:
            self.status_label.setText("\u25CF Model Ready")
            self.status_label.setStyleSheet("color: #00E6B4; font-size: 13px; font-weight: 600;")
            self.status_frame.setStyleSheet("""
                background: rgba(0,230,180,0.1);
                border: 1px solid rgba(0,230,180,0.3);
                border-radius: 12px;
            """)
        else:
            self.status_label.setText(f"\u25CF Error")
            self.status_label.setStyleSheet("color: #FF4757; font-size: 13px; font-weight: 600;")
        
        self.load_models_list()
    
    def unload_model(self):
        """Unload current model"""
        self.llm_manager.unload_model()
        self.status_label.setText("\u25CF No Model Loaded")
        self.status_label.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 13px; font-weight: 600;")
        self.status_frame.setStyleSheet("""
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
        """)
        self.load_models_list()
    
    def send_message(self):
        """Send chat message"""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        self.chat_input.clear()
        
        # Add user message
        self.chat_history.append(f"<p style='color: #00D2FF; font-weight: 700'>You:</p>")
        self.chat_history.append(f"<p style='color: white'>{message}</p>")
        
        if self.llm_manager.is_loaded:
            # Get response from model
            response = self.llm_manager.chat(message)
            self.chat_history.append(f"<p style='color: #6C5CE7; font-weight: 700'>LYFE AI:</p>")
            self.chat_history.append(f"<p style='color: rgba(255,255,255,0.85)'>{response}</p>")
        else:
            # Mock response
            self.chat_history.append(f"<p style='color: #6C5CE7; font-weight: 700'>LYFE AI:</p>")
            self.chat_history.append(f"<p style='color: rgba(255,255,255,0.85)'>I'm running in demo mode. Please load a GGUF model to enable AI responses. Based on your question about '{message[:50]}...', I would analyze the current market conditions, technical indicators, and provide actionable trading insights.</p>")
    
    def send_quick(self, prompt):
        """Send quick prompt"""
        self.chat_input.setText(prompt)
        self.send_message()
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_history.clear()
        self.llm_manager.clear_chat_history()
    
    def refresh_data(self):
        pass
