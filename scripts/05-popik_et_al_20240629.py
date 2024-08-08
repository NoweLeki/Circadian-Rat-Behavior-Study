import os
import pandas as pd

# Define the directory containing the CSV files
# csv_dir = r'D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\features_extracted'
# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\csv\fe-piotr-amber-109-feats'

# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\fe-piotr-amber-109-feats'
csv_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\fe-piotr-amber-109-feats'

# Define the directory to save the original CSV files
original_dir = os.path.join(csv_dir, 'original')

# Create the 'original' subdirectory if it doesn't exist
if not os.path.exists(original_dir):
    os.makedirs(original_dir)

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

for file in csv_files:
    # Construct the full file path
    file_path = os.path.join(csv_dir, file)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Move the original file to the 'original' subdirectory
    os.rename(file_path, os.path.join(original_dir, file))
    
    # Remove the first 73 columns
    modified_df = df.iloc[:, 73:]
    
    # Save the modified DataFrame back to the original directory, ensuring 32-bit format
    modified_df.to_csv(file_path, index=False, float_format='%g')  # '%g' removes unnecessary decimal places, potentially reducing file size

print("Processing completed.")

# 005-C_remove_columns_1-73_from_features_extracted.py
