import os
import pandas as pd

# Path to folder where all your CSV files are kept
folder_path = "data/"

# Read all CSV files from the folder and combine them
all_dfs = []
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        print(f"Loading {file_path} ...")
        df = pd.read_csv(file_path)
        all_dfs.append(df)

# Merge all datasets into one big dataframe
final_df = pd.concat(all_dfs, ignore_index=True)

# Check what columns exist
print(final_df.columns)
print(final_df.head())
print("Total rows:", len(final_df))
