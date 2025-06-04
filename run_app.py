#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the directory this script is in
    current_dir = Path(__file__).parent.absolute()
    
    # Create outputs directory if it doesn't exist
    outputs_dir = current_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    
    # List of scripts to run in order
    scripts = ["history.py", "news.py"]
    
    print("Preparing data for News Feed...")
    
    # Run each prerequisite script
    for script in scripts:
        print(f"\nRunning {script}...")
        try:
            subprocess.run([sys.executable, script], 
                         check=True,
                         cwd=current_dir)
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
            sys.exit(1)
    
    print("\nStarting Streamlit app...")
    # Run streamlit app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "News_Feed.py"],
                      check=True,
                      cwd=current_dir)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 