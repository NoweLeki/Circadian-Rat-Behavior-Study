# done 20240522

import pandas as pd
import os
from colorama import Fore, Style
import colorama

# Initialize colorama
colorama.init()

# Define paths
# usv_adjusted_folder = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/csv/3_machine_results-usv-adjusted"

# usv_adjusted_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows"
# behaviors_adjusted_folder = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/csv/1_machine_results-behaviors-adjusted"
usv_adjusted_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows"
behaviors_adjusted_folder = "D:/LEWIATAN/simb_circ_1_test_morning_12bp_all_33/project_folder/csv/1_machine_results-behaviors-adjusted"

# List CSV files in both folders
usv_adjusted_files = os.listdir(usv_adjusted_folder)
behaviors_adjusted_files = os.listdir(behaviors_adjusted_folder)

# Compare number of rows for each corresponding file
for file_name in usv_adjusted_files:
    if file_name in behaviors_adjusted_files:
        usv_path = os.path.join(usv_adjusted_folder, file_name)
        behavior_path = os.path.join(behaviors_adjusted_folder, file_name)
        
        # Load CSVs
        usv_df = pd.read_csv(usv_path)
        behavior_df = pd.read_csv(behavior_path)
        
        # Compare row counts
        row_diff = abs(len(behavior_df) - len(usv_df))
        time_diff = row_diff / 12  # Assuming 12 FPS for conversion to seconds
        video_duration_s = len(behavior_df) / 12
        audio_duration_s = len(usv_df) / 12

        if len(usv_df) == len(behavior_df):
            print(Fore.GREEN + f"Same N rows in {file_name}. Video duration: {video_duration_s:.2f} s, Audio duration: {audio_duration_s:.2f} s" + Style.RESET_ALL)
        else:
            color = Fore.RED if time_diff > 10 else Fore.YELLOW
            print(color + f"Video has {len(behavior_df)} rows and Audio has {len(usv_df)} rows in {file_name}. That is {row_diff} rows ~ {time_diff:.2f} seconds difference. Video duration: {video_duration_s:.2f} s, Audio duration: {audio_duration_s:.2f} s" + Style.RESET_ALL)
        
#        print("\n")  # New line for clarity

print("Row comparison completed.")


"""Video has 14391 rows and Audio has 14401 rows in 20230507_061000_conc_A.deinterlaced.csv. That is 10 rows ~ 0.83 seconds difference. Video duration: 1199.25 s, Audio duration: 1200.08 s
Video has 14390 rows and Audio has 14401 rows in 20230507_061001_conc_B.deinterlaced.csv. That is 11 rows ~ 0.92 seconds difference. Video duration: 1199.17 s, Audio duration: 1200.08 s
Video has 14389 rows and Audio has 14401 rows in 20230507_061001_conc_C_.deinterlaced.csv. That is 12 rows ~ 1.00 seconds difference. Video duration: 1199.08 s, Audio duration: 1200.08 s
Video has 14388 rows and Audio has 14401 rows in 20230508_061000_conc_B_.deinterlaced.csv. That is 13 rows ~ 1.08 seconds difference. Video duration: 1199.00 s, Audio duration: 1200.08 s
Video has 14398 rows and Audio has 14401 rows in 20230508_061000_conc_C_.deinterlaced.csv. That is 3 rows ~ 0.25 seconds difference. Video duration: 1199.83 s, Audio duration: 1200.08 s
Video has 14399 rows and Audio has 14401 rows in 20230508_061001_conc_A_.deinterlaced.csv. That is 2 rows ~ 0.17 seconds difference. Video duration: 1199.92 s, Audio duration: 1200.08 s
Video has 14397 rows and Audio has 14401 rows in 20230509_061000_conc_B_.deinterlaced.csv. That is 4 rows ~ 0.33 seconds difference. Video duration: 1199.75 s, Audio duration: 1200.08 s
Video has 14397 rows and Audio has 14401 rows in 20230509_061000_conc_C_.deinterlaced.csv. That is 4 rows ~ 0.33 seconds difference. Video duration: 1199.75 s, Audio duration: 1200.08 s
Video has 14399 rows and Audio has 14401 rows in box-a-23-05-09_05-49-56-49_00001.deinterlaced.csv. That is 2 rows ~ 0.17 seconds difference. Video duration: 1199.92 s, Audio duration: 1200.08 s
Video has 14411 rows and Audio has 14401 rows in box-a-23-05-10_05-49-56-58_00002.csv. That is 10 rows ~ 0.83 seconds difference. Video duration: 1200.92 s, Audio duration: 1200.08 s
Video has 14435 rows and Audio has 14426 rows in box-a-23-05-11_05-49-56-56_00003.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.17 s
Video has 14436 rows and Audio has 14427 rows in box-a-23-05-12_05-49-56-53_00004.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1203.00 s, Audio duration: 1202.25 s
Video has 14411 rows and Audio has 14401 rows in box-b-23-05-10_05-49-56-23_00001.csv. That is 10 rows ~ 0.83 seconds difference. Video duration: 1200.92 s, Audio duration: 1200.08 s
Video has 14435 rows and Audio has 14426 rows in box-b-23-05-11_05-49-56-27_00002.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.17 s
Video has 14435 rows and Audio has 14427 rows in box-b-23-05-12_05-49-56-23_00003.csv. That is 8 rows ~ 0.67 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.25 s
Video has 14410 rows and Audio has 14401 rows in box-c-23-05-10_05-49-56-15_00001.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1200.83 s, Audio duration: 1200.08 s
Video has 14435 rows and Audio has 14426 rows in box-c-23-05-11_05-49-55-99_00002.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.17 s
Video has 14435 rows and Audio has 14427 rows in box-c-23-05-12_05-49-56-08_00003.csv. That is 8 rows ~ 0.67 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.25 s
Video has 14410 rows and Audio has 14401 rows in box-d-23-05-10_05-49-56-55_00001.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1200.83 s, Audio duration: 1200.08 s
Video has 14435 rows and Audio has 14426 rows in box-d-23-05-11_05-49-56-53_00002.csv. That is 9 rows ~ 0.75 seconds difference. Video duration: 1202.92 s, Audio duration: 1202.17 s
Video has 14434 rows and Audio has 14427 rows in box-d-23-05-12_05-49-56-59_00003.csv. That is 7 rows ~ 0.58 seconds difference. Video duration: 1202.83 s, Audio duration: 1202.25 s
Video has 14434 rows and Audio has 14426 rows in box-d-23-05-13_05-49-56-58_00004.csv. That is 8 rows ~ 0.67 seconds difference. Video duration: 1202.83 s, Audio duration: 1202.17 s
Video has 14434 rows and Audio has 14426 rows in box-d-23-05-14_05-49-56-56_00005.csv. That is 8 rows ~ 0.67 seconds difference. Video duration: 1202.83 s, Audio duration: 1202.17 s
Same N rows in box-e-23-05-11_05-49-56-88_00002.csv. Video duration: 1201.92 s, Audio duration: 1201.92 s
Video has 14422 rows and Audio has 14420 rows in box-e-23-05-12_05-49-56-06_00003.csv. That is 2 rows ~ 0.17 seconds difference. Video duration: 1201.83 s, Audio duration: 1201.67 s
Video has 14422 rows and Audio has 14423 rows in box-e-23-05-13_05-49-56-04_00004.csv. That is 1 rows ~ 0.08 seconds difference. Video duration: 1201.83 s, Audio duration: 1201.92 s
Video has 14423 rows and Audio has 14420 rows in box-e-23-05-14_05-49-55-93_00005.csv. That is 3 rows ~ 0.25 seconds difference. Video duration: 1201.92 s, Audio duration: 1201.67 s
Same N rows in box-f-23-05-11_05-49-56-56_00002.csv. Video duration: 1201.92 s, Audio duration: 1201.92 s
Video has 14423 rows and Audio has 14420 rows in box-f-23-05-12_05-49-56-62_00003.csv. That is 3 rows ~ 0.25 seconds difference. Video duration: 1201.92 s, Audio duration: 1201.67 s
Same N rows in box-f-23-05-13_05-49-56-60_00004.csv. Video duration: 1201.92 s, Audio duration: 1201.92 s
Video has 14423 rows and Audio has 14420 rows in box-f-23-05-14_05-49-56-57_00005.csv. That is 3 rows ~ 0.25 seconds difference. Video duration: 1201.92 s, Audio duration: 1201.67 s
Row comparison completed."""

# 11.6-compare -- row lengths of machine CSVs for VIDEOS and AUDIOs.py
