#!/usr/bin/env python3
"""
Script to run the Book API Dashboard.
Make sure the API is running on http://localhost:8080 before starting the dashboard.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit dashboard."""
    print("🚀 Starting Book API Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("⚠️  Make sure the API is running on http://localhost:8080")
    print("-" * 50)
    
    try:
        # Run streamlit dashboard using poetry
        subprocess.run([
            "poetry", "run", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user.")
    except FileNotFoundError:
        print("❌ Poetry not found. Please install Poetry first:")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        print("💡 Make sure you have installed the dependencies:")
        print("   poetry install")

if __name__ == "__main__":
    main() 