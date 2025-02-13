import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "superstore.csv")  

def extract_from_csv(file_path):
    try:
        print("Extracting data..")
        df = pd.read_csv(file_path)
        print(f"Data extracted with {len(df)} rows.")
        return df
    except Exception as e:
        print("Error extracting: ", e)
        return None

df = extract_from_csv(DATA_FILE_PATH)