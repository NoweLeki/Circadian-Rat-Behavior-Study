# works
# done 20240522

import pandas as pd
import os

# Load video adjustment info
    # adjustments_df = pd.read_csv("D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/usv/usv_csvs/circadian_1_usv_results-evening-36-rows-with-audio-and-video_novel_99991.csv")
    # adjustments_df = pd.read_csv('D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.csv')

# adjustments_df = pd.read_csv('D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv')
adjustments_df = pd.read_csv('D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-morning-36-rows-with-audio-and-video_09.992.1.csv')


# source_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"
source_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"

    # destination_folder = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/csv/3_machine_results-usv-adjusted"

# dest_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows"
dest_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\5_csvs_with_frame_numbers_filled_01_adjusted_rows"

# Ensure the destination folder exists
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

# Process only unique 'Simba_file' entries to avoid processing duplicates
for simba_file in adjustments_df['Simba_file'].unique():
    if not isinstance(simba_file, str):  # Skip over non-string entries
        continue

    source_file_path = os.path.join(source_folder, simba_file)
    dest_file_path = os.path.join(dest_folder, simba_file)

    if os.path.exists(source_file_path):
        # Load the behavior CSV
        behavior_df = pd.read_csv(source_file_path)

        # Retrieve adjustment info for the current file
        file_adjustments = adjustments_df[adjustments_df['Simba_file'] == simba_file].iloc[0]
        fps = file_adjustments['FPS']
        shorten_start_s = file_adjustments['Cut Start of Audio (s)']
        cut_end_s = file_adjustments['Cut End of Audio (s)']


# -------------------------------------------------------------------------------------------
        # Calculate the number of rows to skip at the start and end based on FPS
        rows_to_skip_at_start = int(fps * shorten_start_s) if not pd.isna(shorten_start_s) else 0
        rows_to_skip_at_end = int(fps * cut_end_s) if not pd.isna(cut_end_s) else 0
# -------------------------------------------------------------------------------------------

        # Adjust the DataFrame
        adjusted_df = behavior_df.iloc[rows_to_skip_at_start : len(behavior_df) - rows_to_skip_at_end]


        # Save adjusted DataFrame
        adjusted_df.to_csv(dest_file_path, index=False)

        print(f"Adjusted {simba_file}: Shortened start by {rows_to_skip_at_start} rows,  {rows_to_skip_at_start / fps} (s) - cut end by {rows_to_skip_at_end} rows = {rows_to_skip_at_end / fps} (s).")
    else:
        print(f"{simba_file} not found in source directory.")


"""Adjusted 20230507_061000_conc_A.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230507_061001_conc_B.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230507_061001_conc_C_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230508_061001_conc_A_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230508_061000_conc_B_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230508_061000_conc_C_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-a-23-05-09_05-49-56-49_00001.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230509_061000_conc_B_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted 20230509_061000_conc_C_.deinterlaced.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-a-23-05-10_05-49-56-58_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-b-23-05-10_05-49-56-23_00001.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-c-23-05-10_05-49-56-15_00001.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-d-23-05-10_05-49-56-55_00001.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-a-23-05-11_05-49-56-56_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-b-23-05-11_05-49-56-27_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-c-23-05-11_05-49-55-99_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-d-23-05-11_05-49-56-53_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-e-23-05-11_05-49-56-88_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-f-23-05-11_05-49-56-56_00002.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-a-23-05-12_05-49-56-53_00004.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-b-23-05-12_05-49-56-23_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-c-23-05-12_05-49-56-08_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-d-23-05-12_05-49-56-59_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-e-23-05-12_05-49-56-06_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-f-23-05-12_05-49-56-62_00003.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-d-23-05-13_05-49-56-58_00004.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-e-23-05-13_05-49-56-04_00004.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-f-23-05-13_05-49-56-60_00004.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-d-23-05-14_05-49-56-56_00005.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-e-23-05-14_05-49-55-93_00005.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s).
Adjusted box-f-23-05-14_05-49-56-57_00005.csv: Shortened start by 0 rows,  0.0 (s) - cut end by 0 rows = 0.0 (s)."""

# 11.5.1-based on 09.992.1 -- cuts AUDIO machine CSV - saves in 5_ folder ------------------------.py
