import pandas as pd

try:
    # Using the path to your CSV file
    df = pd.read_csv("METABRIC_RNA_Mutation.csv")
    print("Successfully loaded data!")
    print(f"Number of rows: {len(df)}")
    print("\nFirst few column names:")
    print(df.columns[:5])
    print("\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error loading file: {e}")