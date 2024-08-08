import os
import pandas as pd

# Define the folder path
folder_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results'

# Define the columns to remove
columns_to_remove = [
    'Probability_FLAT', 'FLAT', 'Probability_FRQ MODUL.', 'FRQ MODUL.',
    'Probability_SHORT', 'SHORT', 'Probability_ALARM', 'ALARM'
]

# Loop over all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Remove the columns if they exist
        df.drop(columns=[col for col in columns_to_remove if col in df.columns], inplace=True)
        
        # Save the modified CSV back to the same file
        df.to_csv(file_path, index=False)

print("Columns removed and files saved successfully.")

# 11.5.1-optional-1-remove last 8 columns from machine_results.py
