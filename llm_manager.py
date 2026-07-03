"""
LYFE - Local LLM Manager
GGUF model support for offline AI inference
"""

import os
import json
import glob
from pathlib import Path
from typing import Optional, List, Dict, Callable


class LLMManager:
    """Manager for local GGUF language models"""
    
    def __init__(self):
        self.model = None
        self.model_path = None
        self.model_info = {}
        self.is_loaded = False
        self.models_dir = Path.home() / ".lyfe" / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.chat_history = []
        
        # Try to import llama-cpp-python
        self.llama_available = False
        try:
            from llama_cpp import Llama
            self.Llama = Llama
            self.llama_available = True
        except ImportError:
            print("llama-cpp-python not installed. GGUF support disabled.")
    
    def is_available(self):
        """Check if llama-cpp is available"""
        return self.llama_available
    
    def scan_models(self) -> List[Dict]:
        """Scan for available GGUF models"""
        models = []
        
        # Scan models directory
        for ext in ["*.gguf", "*.GGUF"]:
            for path in self.models_dir.rglob(ext):
                size_gb = path.stat().st_size / (1024**3)
                models.append({
                    "id": str(path.stem),
                    "name": path.stem,
                    "path": str(path),
                    "size_gb": round(size_gb, 2),
                    "parameters": self._estimate_parameters(path.stem),
                    "quantization": self._detect_quantization(path.stem),
                    "is_loaded": str(path) == self.model_path and self.is_loaded
                })
        
        return models
    
    def _estimate_parameters(self, name: str) -> str:
        """Estimate model parameters from filename"""
        name_lower = name.lower()
        param_map = {
            "7b": "7B", "8b": "8B", "13b": "13B", "14b": "14B",
            "30b": "30B", "34b": "34B", "70b": "70B", "72b": "72B",
            "110b": "110B", "120b": "120B", "180b": "180B",
            "1b": "1B", "2b": "2B", "3b": "3B", "4b": "4B",
        }
        for key, val in param_map.items():
            if key in name_lower:
                return val
        return "Unknown"
    
    def _detect_quantization(self, name: str) -> str:
        """Detect quantization from filename"""
        name_lower = name.lower()
        q_types = ["Q4_K_M", "Q4_K_S", "Q5_K_M", "Q5_K_S", "Q6_K", 
                   "Q8_0", "Q2_K", "Q3_K_M", "Q3_K_S", "Q4_0", "Q5_0"]
        for qt in q_types:
            if qt.lower() in name_lower:
                return qt
        return "Unknown"
    
    def load_model(self, model_path: str, n_ctx: int = 8192, 
                   n_gpu_layers: int = 0, callback: Optional[Callable] = None) -> bool:
        """Load a GGUF model"""
        if not self.llama_available:
            return False
        
        try:
            if self.model:
                self.unload_model()
            
            if callback:
                callback("loading", "Initializing model...")
            
            self.model = self.Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_gpu_layers=n_gpu_layers,
                verbose=False
            )
            
            self.model_path = model_path
            self.is_loaded = True
            self.model_info = {
                "path": model_path,
                "n_ctx": n_ctx,
                "n_gpu_layers": n_gpu_layers,
            }
            
            if callback:
                callback("loaded", "Model loaded successfully")
            
            return True
            
        except Exception as e:
            if callback:
                callback("error", str(e))
            return False
    
    def unload_model(self):
        """Unload current model"""
        if self.model:
            del self.model
            self.model = None
        self.model_path = None
        self.is_loaded = False
        self.model_info = {}
    
    def generate(self, prompt: str, max_tokens: int = 512, 
                 temperature: float = 0.7, top_p: float = 0.9,
                 stop: List[str] = None, stream: bool = False) -> str:
        """Generate text from prompt"""
        if not self.model or not self.is_loaded:
            return "Error: No model loaded"
        
        try:
            if stream:
                output = ""
                for chunk in self.model(prompt, max_tokens=max_tokens,
                                       temperature=temperature, top_p=top_p,
                                       stop=stop or [], stream=True):
                    delta = chunk["choices"][0]["text"]
                    output += delta
                    yield delta
                return output
            else:
                result = self.model(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    stop=stop or []
                )
                return result["choices"][0]["text"]
                
        except Exception as e:
            return f"Generation error: {str(e)}"
    
    def chat(self, message: str, system_prompt: str = None, 
             max_tokens: int = 512) -> str:
        """Chat completion with history"""
        if not self.model or not self.is_loaded:
            return "Error: No model loaded"
        
        # Add user message to history
        self.chat_history.append({"role": "user", "content": message})
        
        # Build prompt
        prompt = ""
        if system_prompt:
            prompt = f"<|system|>\n{system_prompt}\n"
        
        for msg in self.chat_history:
            role = msg["role"]
            content = msg["content"]
            prompt += f"<|{role}|>\n{content}\n"
        
        prompt += "<|assistant|>\n"
        
        try:
            response = self.model(prompt, max_tokens=max_tokens,
                                temperature=0.7, stop=["<|user|>", "<|system|>"])
            reply = response["choices"][0]["text"].strip()
            
            # Add assistant response to history
            self.chat_history.append({"role": "assistant", "content": reply})
            
            # Trim history if too long
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return reply
            
        except Exception as e:
            return f"Chat error: {str(e)}"
    
    def clear_chat_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    def analyze_chart(self, chart_data: str) -> str:
        """Analyze chart data using loaded model"""
        system_prompt = """You are an expert forex and synthetic indices analyst. 
Analyze the provided chart data and provide:
1. Current trend direction
2. Key support and resistance levels
3. Entry signals with confidence
4. Risk management suggestions
Be concise and actionable."""
        
        return self.chat(chart_data, system_prompt=system_prompt, max_tokens=1024)
    
    def generate_signal(self, market_data: Dict) -> Dict:
        """Generate trading signal from market data"""
        prompt = f"""Analyze this market data and provide a trading signal:
Symbol: {market_data.get('symbol', 'Unknown')}
Price: {market_data.get('price', 'N/A')}
Trend: {market_data.get('trend', 'N/A')}
RSI: {market_data.get('rsi', 'N/A')}
MACD: {market_data.get('macd', 'N/A')}

Respond ONLY in this JSON format:
{{
    "direction": "BUY" or "SELL" or "NEUTRAL",
    "confidence": 0-100,
    "entry": price,
    "sl": stop_loss_price,
    "tp": take_profit_price,
    "reasoning": "brief explanation"
}}"""
        
        response = self.generate(prompt, max_tokens=256, temperature=0.5)
        
        try:
            # Try to parse JSON from response
            import re
            json_match = re.search(r'\{[^}]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "direction": "NEUTRAL",
            "confidence": 0,
            "reasoning": response[:200]
        }
    
    def get_model_info(self) -> Dict:
        """Get loaded model info"""
        return {
            **self.model_info,
            "is_loaded": self.is_loaded,
            "llama_available": self.llama_available
        }
