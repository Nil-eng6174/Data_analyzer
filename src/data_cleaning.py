import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path, encoding='latin1')
    
    print("\n--- PHASE 2: DATA UNDERSTANDING ---")
    print(f"Shape: {df.shape}")
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print(f"\nDuplicate Records: {df.duplicated().sum()}")
    
    print("\n--- PHASE 3: DATA CLEANING ---")
    # Handle column names (strip spaces, replace with underscores, lowercase)
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.lower()
    
    # Convert dates without dayfirst since pandas can usually infer M/D/Y or Y-M-D
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='mixed', errors='coerce')
    
    # Remove duplicates
    initial_shape = df.shape
    df = df.drop_duplicates()
    print(f"Dropped {initial_shape[0] - df.shape[0]} duplicate rows.")
    
    # Handle missing values (if any)
    if 'postal_code' in df.columns:
        df['postal_code'] = df['postal_code'].fillna('Unknown')
        
    # Clean numerical values
    for col in ['sales', 'profit', 'discount', 'shipping_cost']:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill remaining numerical NaNs with 0 (assuming they shouldn't be NaN)
    for col in ['sales', 'profit', 'discount', 'shipping_cost']:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    # Remove any rows with invalid order_date
    df = df.dropna(subset=['order_date'])
    
    print(f"Cleaned Data Shape: {df.shape}")
    
    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == '__main__':
    input_file = '../data/raw_dataset.csv'
    output_file = '../data/cleaned_dataset.csv'
    
    if not os.path.exists(input_file):
        input_file = 'data/raw_dataset.csv'
        output_file = 'data/cleaned_dataset.csv'
        
    clean_data(input_file, output_file)
