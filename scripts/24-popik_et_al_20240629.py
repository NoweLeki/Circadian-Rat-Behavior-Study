# done 20240522

import os
import pandas as pd

# Define folder paths
    # original_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results'
    # usv_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'
    # expanded_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true_expanded'

# original_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\1_machine_results-behaviors-adjusted'
# usv_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows'
# expanded_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\6_machine_results--behaviors-plus-usv-adjusted-final'
original_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\1_machine_results-behaviors-adjusted'
usv_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows'
expanded_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\6_machine_results--behaviors-plus-usv-adjusted-final'

# Create expanded_folder if it doesn't exist
if not os.path.exists(expanded_folder):
    os.makedirs(expanded_folder)

# Variables to keep track of processing
processed = 0
not_processed = 0

# Iterate over CSVs in the usv_folder
for usv_file in os.listdir(usv_folder):
    if usv_file.endswith('.csv'):
        usv_path = os.path.join(usv_folder, usv_file)
        original_path = os.path.join(original_folder, usv_file)

        # Check if corresponding original CSV exists
        if os.path.exists(original_path):
            usv_df = pd.read_csv(usv_path)
            original_df = pd.read_csv(original_path)

            # Determine the smallest row count
            min_rows = min(len(usv_df), len(original_df))

            # Truncate dataframes to the smallest row count
            usv_df_truncated = usv_df.head(min_rows)
            original_df_truncated = original_df.head(min_rows)

            # Copy specified columns from truncated usv_df to truncated original_df
            columns_to_copy = usv_df_truncated.iloc[:, -8:]  # Adjust index as needed
            expanded_df = pd.concat([original_df_truncated, columns_to_copy], axis=1)

            # Save the expanded CSV
            expanded_path = os.path.join(expanded_folder, usv_file)
            expanded_df.to_csv(expanded_path, index=False)

            print(f"Processed and expanded {usv_file}. Truncated to {min_rows} rows.")
            processed += 1
        else:
            print(f"Corresponding original CSV for {usv_file} not found.")
            not_processed += 1

# Summary
print(f"Total CSVs processed: {processed}")
print(f"Total CSVs not processed: {not_processed}")

"""Processed and expanded 20230507_061000_conc_A.deinterlaced.csv. Truncated to 14391 rows.
Processed and expanded 20230507_061001_conc_B.deinterlaced.csv. Truncated to 14390 rows.
Processed and expanded 20230507_061001_conc_C_.deinterlaced.csv. Truncated to 14389 rows.
Processed and expanded 20230508_061000_conc_B_.deinterlaced.csv. Truncated to 14388 rows.
Processed and expanded 20230508_061000_conc_C_.deinterlaced.csv. Truncated to 14398 rows.
Processed and expanded 20230508_061001_conc_A_.deinterlaced.csv. Truncated to 14399 rows.
Processed and expanded 20230509_061000_conc_B_.deinterlaced.csv. Truncated to 14397 rows.
Processed and expanded 20230509_061000_conc_C_.deinterlaced.csv. Truncated to 14397 rows.
Processed and expanded box-a-23-05-09_05-49-56-49_00001.deinterlaced.csv. Truncated to 14399 rows.
Processed and expanded box-a-23-05-10_05-49-56-58_00002.csv. Truncated to 14401 rows.
Processed and expanded box-a-23-05-11_05-49-56-56_00003.csv. Truncated to 14426 rows.
Processed and expanded box-a-23-05-12_05-49-56-53_00004.csv. Truncated to 14427 rows.
Processed and expanded box-b-23-05-10_05-49-56-23_00001.csv. Truncated to 14401 rows.
Processed and expanded box-b-23-05-11_05-49-56-27_00002.csv. Truncated to 14426 rows.
Processed and expanded box-b-23-05-12_05-49-56-23_00003.csv. Truncated to 14427 rows.
Processed and expanded box-c-23-05-10_05-49-56-15_00001.csv. Truncated to 14401 rows.
Processed and expanded box-c-23-05-11_05-49-55-99_00002.csv. Truncated to 14426 rows.
Processed and expanded box-c-23-05-12_05-49-56-08_00003.csv. Truncated to 14427 rows.
Processed and expanded box-d-23-05-10_05-49-56-55_00001.csv. Truncated to 14401 rows.
Processed and expanded box-d-23-05-11_05-49-56-53_00002.csv. Truncated to 14426 rows.
Processed and expanded box-d-23-05-12_05-49-56-59_00003.csv. Truncated to 14427 rows.
Processed and expanded box-d-23-05-13_05-49-56-58_00004.csv. Truncated to 14426 rows.
Processed and expanded box-d-23-05-14_05-49-56-56_00005.csv. Truncated to 14426 rows.
Processed and expanded box-e-23-05-11_05-49-56-88_00002.csv. Truncated to 14423 rows.
Processed and expanded box-e-23-05-12_05-49-56-06_00003.csv. Truncated to 14420 rows.
Processed and expanded box-e-23-05-13_05-49-56-04_00004.csv. Truncated to 14422 rows.
Processed and expanded box-e-23-05-14_05-49-55-93_00005.csv. Truncated to 14420 rows.
Processed and expanded box-f-23-05-11_05-49-56-56_00002.csv. Truncated to 14423 rows.
Processed and expanded box-f-23-05-12_05-49-56-62_00003.csv. Truncated to 14420 rows.
Processed and expanded box-f-23-05-13_05-49-56-60_00004.csv. Truncated to 14423 rows.
Processed and expanded box-f-23-05-14_05-49-56-57_00005.csv. Truncated to 14420 rows.
Total CSVs processed: 31
Total CSVs not processed: 0"""

# 11.9 - was - 20.1-combine adjusted (shortened) CSV machine_results with detected USV in novel folder.py
