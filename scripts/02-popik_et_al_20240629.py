
import os
import pandas as pd

# Define the directory containing the CSV files
# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\csv\machine_results'

# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\features_extracted'
csv_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\features_extracted'

# Define the subdirectory for storing original files
original_dir = os.path.join(csv_dir, 'original')

# Create the subdirectory if it doesn't exist
if not os.path.exists(original_dir):
    os.makedirs(original_dir)

# Track replacements
replacements_made = []

# Iterate through each file in the CSV directory
for filename in os.listdir(csv_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_dir, filename)
        
        # Move the original file to the "original" subdirectory
        os.rename(file_path, os.path.join(original_dir, filename))
        
        # Read the CSV file, replacing 'NaN' with 0
        df = pd.read_csv(os.path.join(original_dir, filename), na_values=['NaN'])
        nan_count = df.isna().sum().sum()
        if nan_count > 0:
            df.fillna(0, inplace=True)
            replacements_made.append((filename, nan_count))
        
        # Save the corrected DataFrame back to the original directory
        df.to_csv(file_path, index=False)

# Report the replacements
if replacements_made:
    for filename, count in replacements_made:
        print(f"Replacements made in {filename}: {count} replacements")
else:
    print("No replacements were made in any files.")

print("All CSV files have been processed and corrected.")


# 002-replace_all_nans_with_zeroes.py
    ## not used yet - I replaced manualy NaNs with 0 in single file 
    ## 20230506_175959_conc_C_.deinterlaced.csv
