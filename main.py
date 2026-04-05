#!/usr/bin/env python3
"""
AeroPrice Startup Script
Launches the enhanced satellite property valuation system
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'flask', 'flask_cors', 'tensorflow', 'pandas', 'numpy', 
        'PIL', 'matplotlib', 'seaborn', 'shap', 'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_model_files():
    """Check if required model files exist."""
    required_files = [
        'models/final_model_satellite.h5',
        'data/austin_master_dataset.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("Please ensure these files are in the current directory.")
        return False
    
    print("✅ All required model files found!")
    return True

def start_backend():
    """Start the Flask backend."""
    print("🚀 Starting Flask backend...")
    try:
        subprocess.Popen([sys.executable, os.path.join('backend', 'main.py')], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(3)  # Give backend time to start
        print("✅ Backend started on http://localhost:5000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_streamlit():
    """Start the Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    try:
        # Check if streamlit is available
        try:
            import streamlit
        except ImportError:
            print("❌ Streamlit not installed. Install with: pip install streamlit")
            return False
        
        subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', os.path.join('frontend', 'app.py')],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        time.sleep(5)  # Give Streamlit time to start
        print("✅ Streamlit started on http://localhost:8501")
        return True
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return False

def open_browser():
    """Open browser to the application."""
    time.sleep(2)
    print("🌐 Opening browser...")
    try:
        webbrowser.open('http://localhost:8501')  # Streamlit interface
        webbrowser.open('http://localhost:5000')  # API docs
        return True
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        return False

def main():
    """Main startup function."""
    print("🛰️ AeroPrice - Satellite Property Valuation System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check model files
    if not check_model_files():
        return 1
    
    print("\n📋 Starting AeroPrice services...")
    
    # Start backend
    if not start_backend():
        return 1
    
    # Start Streamlit frontend
    if not start_streamlit():
        print("⚠️  Streamlit frontend failed to start.")
        print("💡 You can still use the Flask API directly at http://localhost:5000")
        print("💡 Or open index.html in your browser for the basic interface.")
        return 0
    
    # Open browser
    open_browser()
    
    print("\n🎉 AeroPrice is now running!")
    print("📱 Streamlit Interface: http://localhost:8501")
    print("🔧 Flask API: http://localhost:5000")
    print("📄 Basic HTML Interface: Open index.html in your browser")
    print("\n💡 Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AeroPrice...")
        print("✅ Goodbye!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
