
# works with
"""
    20230506_175959_conc_C_.deinterlaced.csv
    20230506_181000_conc_A.deinterlaced.csv
    20230506_181001_conc_B.deinterlaced.csv
    20230507_181000_conc_B.deinterlaced.csv
    20230507_181000_conc_C_.deinterlaced.csv
    20230508_181000_conc_C_.csv
    20230508_181000_conc_B_.csv
"""

# This is helper script 
# Agnieszka Potasiewicz circadian_1_usv_results.csv contain columns showing BOX, DATA and TIME
# In order to match these with SimBA machine_results, I had to fill the column Simba_file and could do this manualy
# This scrpit searches for files in machine_results-plus_usvs_true folder
# Matches specific row and FILLS (OVERRIDES !!!) column Simba_File

# Another script:
#   05.2-match-csvs-with-10.0.215 !.py
# is then to be run

# done 20240520 

import os
import shutil
import pandas as pd
from datetime import datetime

# Backup the original USV results CSV
# original_usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
# backup_usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results_original.csv'

original_usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
backup_usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results_original.csv'

if not os.path.exists(backup_usv_results_path):
    shutil.copyfile(original_usv_results_path, backup_usv_results_path)
    print("Original USV results CSV has been backed up successfully.")
else:
    print("Backup file already exists. Original USV results CSV has not been overwritten.")

# ---
    
#    print(f'{date_str}' f'{box_str}' f'{time_str}')

import os
import pandas as pd
from datetime import datetime

def wait_for_space():
    input("Press Space to continue...")

# usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'


usv_df = pd.read_csv(usv_results_path)

# Initialize 'Simba_file' as an empty string
usv_df['Simba_file'] = ''

# source_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'
source_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'

filenames = [f for f in os.listdir(source_folder) if f.endswith('.csv')]

def is_evening(file_time_str):
    hour = int(file_time_str[:2])
    return 17 <= hour <= 18

def is_morning(file_time_str):
#    return "061000" in file_time_str  # Check if "061000" is part of the time string, indicating morning
    return "0610" in file_time_str  # Check if "061000" is part of the time string, indicating morning

for index, row in usv_df.iterrows():
    date_str = datetime.strptime(row['DATA'], '%Y-%m-%d').strftime('%Y%m%d')
    box_str = row['BOX'].split('-')[-1].upper()

    for filename in filenames:
        file_parts = filename.split('_')
        if len(file_parts) < 4:
            continue

        file_date, file_time_str = file_parts[:2]
        file_box_letter = file_parts[3][0]

        # Determine if the row TIME should be matched with morning or evening filenames
        should_match_morning = row['TIME'] == '05-50' and is_morning(file_time_str)
        should_match_evening = row['TIME'] == '17-50' and is_evening(file_time_str)

        if not (should_match_morning or should_match_evening):
            continue  # Skip this filename if it doesn't match the expected morning/evening criteria

        print(f"Trying to match: Date: {date_str} with {file_date}, Box: {box_str} with {file_box_letter}")

        if date_str == file_date and box_str == file_box_letter:
            usv_df.at[index, 'Simba_file'] = filename
            print(f"Matched '{filename}' for row {index}.")
            break

#        wait_for_space()

usv_df.to_csv(usv_results_path, index=False)
print("USV entries have been processed for matching filenames.")

# 05.2-match-csvs-with-10.0.215 (helper 2023-file type)!.py
