# 20240521 - __ - a better way is 
# 02.7-for AUDIO creates novel csvs in (4_csvs_with_frame_numbers_beg_end_and_zeroes).py

import pandas as pd

# Load the USV results data
# usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\20230508_181000_conc_B_.csv'  # Update with the actual file path

# usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'  # Update with the actual file path
usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'    # Update with the actual file path
usv_df = pd.read_csv(usv_results_path)

# Display the first few rows to understand its structure
# print(usv_df.head())

# works and produces
# Frame number from video analysis	Begin frame time (s)	End frame time (s)	Probability_ALARM	ALARM	Probability_FLAT	FLAT	Probability_FREQ MODUL.	FREQ MODUL.	Probability_SHORT	SHORT
# 0	0	0.090909091	0	0	0	0	0	0	0	0
# 1	0.090909091	0.181818182	0	0	0	0	0	0	0	0
# 2	0.181818182	0.272727273	0	0	0	0	0	0	0	0

# Fills cells with 0's:

# Reads CSVs in machine_results-plus_usvs folder
# Reads circadian_1_usv_results.csv Column Simba_file ... and Call typE Column.

# Saves CSVs to machine_results-plus_usvs_true, And
# fills the USV type columns with 0

# 2 So, we have all USV cells filled with 0
# done 20240520

import os

# Directory paths
# source_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs'
# dest_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'
source_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results-plus_usvs'
dest_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'


# Ensure the destination folder exists
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

# Iterate through each CSV file in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        # Construct the full path to the source CSV
        csv_path = os.path.join(source_folder, filename)
        
        # Load the source CSV
        df = pd.read_csv(csv_path)
        
        # Filter the USV data for the current Simba_file
        usv_subset = usv_df[usv_df['Simba_file'] == filename]
        
        # Initialize the new columns with default values
        for col in ['Probability_ALARM', 'ALARM', 'Probability_FLAT', 'FLAT', 'Probability_FRQ MODUL.', 'FRQ MODUL.', 'Probability_SHORT', 'SHORT']:
            df[col] = 0  # Or another default value as per requirements
        
        # Update the new columns based on the USV data
        # This step will require you to loop through `usv_subset` and update `df` based on the Begin Time (s), End Time (s), and Call typE
        # You'll need to decide how to calculate the "Probability" values
        
        # Save the modified DataFrame to the destination folder
        df.to_csv(os.path.join(dest_folder, filename), index=False)

print("Processing completed. Modified CSV files are saved in 'machine_results-plus_usvs_true' folder.")

# 03.1-__fill-usv-results-with-zeroes                                               !.py
