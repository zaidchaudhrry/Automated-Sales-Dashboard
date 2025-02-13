import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANSFORMED_FILE_PATH = os.path.join(BASE_DIR, "data", "transformed_superstore.csv")

df = pd.read_csv(TRANSFORMED_FILE_PATH)
print(df.dtypes)