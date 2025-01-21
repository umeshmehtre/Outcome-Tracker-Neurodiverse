#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

def setup_virtual_environment():
    """Create and activate a virtual environment."""
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    
    # Determine the correct activation script based on the platform
    if sys.platform == 'win32':
        activate_script = 'venv\\Scripts\\activate'
    else:
        activate_script = 'venv/bin/activate'
    
    if not os.path.exists(activate_script):
        print(f"Error: Could not find virtual environment activation script at {activate_script}")
        sys.exit(1)
    
    print(f"To activate the virtual environment, run:\n")
    if sys.platform == 'win32':
        print(f"    {activate_script}")
    else:
        print(f"    source {activate_script}")

def install_dependencies():
    """Install project dependencies."""
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
    ], check=True)
    
    print("Installing project in development mode...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-e', '.'
    ], check=True)

def create_directories():
    """Create necessary project directories."""
    directories = ['data', 'data/raw', 'data/processed']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """Main setup function."""
    print("Setting up Outcome Tracker project...")
    
    # Check Python version
    check_python_version()
    
    try:
        # Setup virtual environment
        setup_virtual_environment()
        
        # Create necessary directories
        create_directories()
        
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Activate the virtual environment (see instructions above)")
        print("2. Run the application:")
        print("   streamlit run src/app/main.py")
        print("\nFor development:")
        print("- Run tests: pytest")
        print("- Format code: black .")
        print("- Check code style: flake8")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()