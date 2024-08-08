import os
import shutil

# Define source and target folder paths
source_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results'
target_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\0_machine_results-behaviors-original-moved-here'

# Create the target folder if it doesn't exist
os.makedirs(target_folder, exist_ok=True)

# Loop over all files in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith('.csv'):
        # Define full file paths
        source_file = os.path.join(source_folder, file_name)
        target_file = os.path.join(target_folder, file_name)
        
        # Copy file from source to target
        shutil.copy2(source_file, target_file)

print("CSV files copied successfully.")

# 11.5.1-optional-2-copy machine_results CSVs to 0_machine_results-behaviors-original-moved-here.py
