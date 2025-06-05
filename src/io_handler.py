import pandas as pd
import os

def read_questions(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == '.xlsx':
        return pd.read_excel(file_path)
    elif file_ext == '.csv':
        return pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Please use .xlsx or .csv files.")

def save_questions(df, output_path):
    file_ext = os.path.splitext(output_path)[1].lower()
    if file_ext == '.xlsx':
        df.to_excel(output_path, index=False)
    elif file_ext == '.csv':
        df.to_csv(output_path, index=False)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Please use .xlsx or .csv files.")
