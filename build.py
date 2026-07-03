#!/usr/bin/env python3
"""
LYFE - Build Script
Builds Windows EXE using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build():
    """Build LYFE Windows executable"""
    print("=" * 60)
    print("LYFE - Building Windows Executable")
    print("=" * 60)
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")
    
    # Create assets directory with icon
    os.makedirs("assets", exist_ok=True)
    
    # Build with PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LYFE",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--hidden-import=PyQt6.sip",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=sqlite3",
        "--hidden-import=websocket",
        "--hidden-import=requests",
        "--hidden-import=numpy",
        "--hidden-import=pandas",
        "--hidden-import=views.dashboard",
        "--hidden-import=views.signals",
        "--hidden-import=views.trading",
        "--hidden-import=views.backtest",
        "--hidden-import=views.news",
        "--hidden-import=views.llm_view",
        "--hidden-import=views.tools_view",
        "--hidden-import=views.settings_view",
        "--hidden-import=views.base_view",
        "--add-data=views:views",
        "--exclude-module=matplotlib",
        "--exclude-module=tkinter",
        "--exclude-module=PIL",
        "main.py"
    ]
    
    print("\nRunning PyInstaller...")
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("Build successful!")
        print(f"Output: {os.path.abspath('dist/LYFE.exe')}")
        print("=" * 60)
    else:
        print("\nBuild failed!")
        sys.exit(1)


if __name__ == "__main__":
    build()
