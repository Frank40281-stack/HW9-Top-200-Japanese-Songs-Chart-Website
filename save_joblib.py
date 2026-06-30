import csv
import pandas as pd
import joblib

CSV_FILE = "top200_songs.csv"
JOBLIB_FILE = "top200_songs.joblib"

def main():
    try:
        print(f"Reading {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE)
        
        print(f"Saving to {JOBLIB_FILE} using joblib...")
        joblib.dump(df, JOBLIB_FILE)
        
        print("Success! top200_songs.joblib created successfully.")
    except Exception as e:
        print(f"Error creating joblib file: {e}")

if __name__ == "__main__":
    main()
