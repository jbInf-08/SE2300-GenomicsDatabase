import pandas as pd
import os

def verify_system():
    # Check Python version
    import sys
    print(f"Python version: {sys.version}")
    
    # Check required packages
    packages = ['pandas', 'numpy', 'matplotlib', 'seaborn']
    for package in packages:
        try:
            __import__(package)
            print(f"{package}: ✓")
        except ImportError:
            print(f"{package}: ✗ (not installed)")
    
    # Check file access
    file_path = "METABRIC_RNA_Mutation.csv"  # Replace with your path
    if os.path.exists(file_path):
        print(f"Data file: ✓")
        # Try loading the file
        try:
            df = pd.read_csv(file_path)
            print(f"Data loading: ✓ ({len(df)} rows)")
        except Exception as e:
            print(f"Data loading: ✗ (Error: {e})")
    else:
        print(f"Data file: ✗ (not found)")

if __name__ == "__main__":
    verify_system()