
# Reads CSVs in 4_csvs_with_frame_numbers_beg_end_and_zeroes folder
# Reads circadian_1_usv_results.csv Column Simba_file ... and Call typE Column.

    # Note: the Simba_file column in -----------------------------------------------------------------------------------------------
    # usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
    # must be filled with the use of 2 helper scripts in advance! ------------------------------------------------------------------

    # 05.2-match-csvs-with-10.0.215 (helper 2023-file type)!.py
    # 05.8-match-csvs-with-10.0.215 (helper box-a-file type) !.py

# Overrides CSVs IN 4_csvs_with_frame_numbers_beg_end_and_zeroes, And
# - if the file exists in Simba_file, fills the USV type columns with 1
# - if the file does not exist in Simba_file, IT DOES NOTHING

# 3 So, 4_csvs_with_frame_numbers_beg_end_and_zeroes have now "1" at rows where the call was detected
# done 20240521 

import pandas as pd
import os
import numpy as np  # For handling NaN

# Path to the USV results CSV
# usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'

# Load the USV results with specified data types
usv_df = pd.read_csv(usv_results_path, low_memory=False)
usv_df['Simba_file'] = usv_df['Simba_file'].astype(str)  # Convert 'Simba_file' entries to strings

# Directory path for machine_results-plus_usvs_true
    # source_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'
# source_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"
source_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"

# Iterate over unique 'Simba_file' entries in the USV DataFrame
for simba_file in usv_df['Simba_file'].unique():
    # Skip invalid 'Simba_file' entries
    if simba_file == 'nan' or not simba_file.endswith('.csv'):
        continue

    csv_file_path = os.path.join(source_folder, simba_file)
    
    # Check if the file exists in the directory
    if os.path.exists(csv_file_path):
        # Load the specific CSV file
        csv_df = pd.read_csv(csv_file_path, low_memory=False)

        # Initialize new columns if they don't exist
        for usv_type in ['ALARM', 'FLAT', 'FRQ MODUL.', 'SHORT']:
            if f'Probability_{usv_type}' not in csv_df.columns:
                csv_df[f'Probability_{usv_type}'] = 0
            if usv_type not in csv_df.columns:
                csv_df[usv_type] = 0

        # Filter the USV DataFrame for the current simba_file
        simba_usv_df = usv_df[usv_df['Simba_file'] == simba_file]

        # Iterate through each USV record in the filtered USV DataFrame
        for _, usv_row in simba_usv_df.iterrows():
            # Extract USV call details
            usv_type = usv_row['Call typE']
            begin_time = usv_row['Begin Time (s)']
            end_time = usv_row['End Time (s)']

            # Update the DataFrame for rows within the USV call time range
            csv_df.loc[(csv_df['Begin frame time (s)'] < end_time) & (csv_df['End frame time (s)'] > begin_time), [f'Probability_{usv_type}', usv_type]] = 1

        # Save the updated DataFrame
        csv_df.to_csv(csv_file_path, index=False)

        print(f"Updated {csv_file_path} with USV call probabilities and occurrences.")
    else:
        print(f"File {simba_file} not found in {source_folder}.")

# 04.4-for AUDIO updates (4_csvs_with_frame_numbers_beg_end_and_zeroes) with 1.py
