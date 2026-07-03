# LYFE - AI Trading Platform (Desktop)

A professional AI-powered trading and analytics platform for Windows, featuring glass morphism UI, real-time Deriv API integration, local GGUF model support, and comprehensive trading tools.

## Features

- **Glass Morphism UI** - Modern translucent interface design
- **Sidebar Navigation** - 8 main sections: Dashboard, AI Signals, Trading, Backtest, News, AI Models, Tools, Settings
- **Deriv API Integration** - Real-time market data and trade execution
- **Automated Trading** - Custom API support for automated strategies
- **Local GGUF Models** - Offline AI inference with llama-cpp-python
- **Backtesting Engine** - 6 built-in strategies with performance analytics
- **Trading Tools** - Position sizer, pip calculator, risk/reward, Fibonacci, pivot points, compounding, currency converter
- **Local Storage** - SQLite database for signals, trades, and settings
- **Economic Calendar** - High-impact news events and market analysis

## Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- Internet connection for real-time data

## Installation

Download and run `LYFE-Setup-v3.0.0.exe` to install.

## Building from Source

```bash
pip install -r requirements.txt
python build.py
```

## Project Structure

```
python-desktop/
  main.py              - Application entry point
  database.py          - SQLite storage manager
  deriv_api.py         - Deriv WebSocket API client
  llm_manager.py       - GGUF model management
  backtest_engine.py   - Strategy backtesting
  styles.py            - Glass morphism QSS styles
  views/               - All UI view components
    base_view.py       - Base view class
    dashboard.py       - Main dashboard
    signals.py         - AI signals view
    trading.py         - Trading terminal
    backtest.py        - Backtesting interface
    news.py            - News & calendar
    llm_view.py        - AI model manager
    tools_view.py      - Trading tools
    settings_view.py   - App settings
```

## License

MIT License
