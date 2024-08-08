# works with

"""
box-a-23-05-08_17-49-56-78_00001.deinterlaced.csv
box-a-23-05-09_17-49-56-59_00002.deinterlaced.csv
box-a-23-05-10_17-49-56-57_00003.csv
box-a-23-05-11_17-49-56-54_00004.csv
box-b-23-05-09_17-49-56-33_00001.deinterlaced.csv
box-b-23-05-10_17-49-56-21_00002.csv
box-b-23-05-11_17-49-56-25_00003.csv
box-c-23-05-09_17-49-56-46_00001.deinterlaced.csv
box-c-23-05-10_17-49-56-07_00002.deinterlaced.csv
box-c-23-05-11_17-49-56-00_00003.csv
box-d-23-05-09_17-49-57-19_00001.deinterlaced.csv
box-d-23-05-10_17-49-56-58_00002.csv
box-d-23-05-11_17-49-56-56_00003.csv
box-d-23-05-12_17-49-56-54_00004.csv
box-d-23-05-13_17-49-56-53_00005.csv
box-d-23-05-14_17-49-56-51_00006.csv
box-e-23-05-10_17-49-57-01_00002.csv
box-e-23-05-11_17-49-56-99_00003.csv
box-e-23-05-12_17-49-55-97_00004.csv
box-e-23-05-13_17-49-55-94_00005.csv
box-e-23-05-14_17-49-56-92_00006.csv
box-f-23-05-09_17-49-56-84_00001.deinterlaced.csv
box-f-23-05-10_17-49-56-57_00002.deinterlaced.csv
box-f-23-05-12_17-49-56-61_00004.csv
box-f-23-05-13_17-49-56-58_00005.csv
box-f-23-05-14_17-49-56-56_00006.csv
"""

# This is helper script 
# Agnieszka Potasiewicz circadian_1_usv_results.csv contain columns showing BOX, DATA and TIME
# In order to match these with SimBA machine_results, I had to fill the column Simba_file and could do this manualy
# This scrpit searches for files in machine_results-plus_usvs_true folder
# Matches specific row and UPDATES column Simba_File IF IT IS NOT EMPTY BECAUSE in the former step, a similar scrript
#   05.2-match-csvs-with-10.0.215 !.py
# Was run and analyzed CSV files with different file names


import os
import pandas as pd

# Load the USV results CSV
# usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'
usv_results_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results.csv'

usv_df = pd.read_csv(usv_results_path)

# Ensure 'Simba_file' column is of type string and initialize empty strings where needed
if 'Simba_file' not in usv_df.columns:
    usv_df['Simba_file'] = ''  # Initialize column if it doesn't exist
usv_df['Simba_file'] = usv_df['Simba_file'].fillna('').astype(str)

# Directory path for machine_results-plus_usvs_true
# source_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'
source_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results-plus_usvs_true'

filenames = [f for f in os.listdir(source_folder) if f.startswith('box-') and f.endswith('.csv')]

def is_evening_or_morning(time_str):
    """Determines if the given time string indicates evening or morning."""
    hour = int(time_str.split('-')[0])
    return "Evening" if 17 <= hour <= 23 else "Morning"

for index, row in usv_df.iterrows():
    # Skip rows where 'Simba_file' is already populated
    if row['Simba_file']:
        continue

    csv_time_slot = row['TIME']
    csv_morning_or_evening = "Evening" if csv_time_slot.startswith("17") else "Morning"
    csv_box = row['BOX'].replace("BOX-", "")  # Remove 'BOX-' prefix to match the filename format
    csv_date = row['DATA'].replace("-", "")[2:]  # Convert 'YYYY-MM-DD' to 'YYMMDD'

    for filename in filenames:
        parts = filename.split('_')
        file_box = parts[0].split('-')[1].upper()  # Get the box part and convert to uppercase
        file_date = ''.join(parts[0].split('-')[2:5])  # Combine 'YY', 'MM', and 'DD' parts
        time_part = parts[1]
        file_morning_or_evening = is_evening_or_morning(time_part)

        if csv_morning_or_evening == file_morning_or_evening and csv_box == file_box and csv_date == file_date:
            usv_df.at[index, 'Simba_file'] = filename
            print(f"Matched '{filename}' for row {index}.")

# Uncomment the line below to save the updated DataFrame
usv_df.to_csv(usv_results_path, index=False)

print("Simba_file column update attempt completed.")

# 05.8-match-csvs-with-10.0.215 (helper box-a-file type) !.py
