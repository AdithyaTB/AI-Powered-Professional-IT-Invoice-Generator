# install.py
import subprocess
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {command}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🔧 Installing IT Invoice Generator for Python 3.12...")
    
    # Package installation order matters
    packages = [
       
        ("scikit-learn", "pip install scikit-learn==1.3.0"),

    ]
    
    all_success = True
    for package_name, command in packages:
        if not run_command(command):
            all_success = False
            print(f"⚠️  Failed to install {package_name}, but continuing...")
    
    if all_success:
        print("🎉 All packages installed successfully!")
    else:
        print("⚠️  Some packages had issues, but core functionality should work.")
    
    # Test imports
    print("\n🔍 Testing imports...")
    test_imports = [
        "streamlit", "pandas", "numpy", "sklearn", "joblib", 
        "reportlab", "plotly", "PIL"
    ]
    
    for package in test_imports:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - FAILED: {e}")

if __name__ == "__main__":
    main()