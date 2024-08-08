# Reads files like
# S:\dummy\-2023\circadian\USV\2023-05-14\BOX-F_2023-05-14_17-50-00.wav for box-f-23-05-14_17-49-56-56_00006.csv
# In
# --------------------------------------------
# circadian_1_usv_results-evening-36-rows.csv
# --------------------------------------------
# Because columns
# AUDIO_PATH	AUDIO_FILE_NAME
# Already exist

# Updates Columns
# AUDIO_START_DATE	AUDIO_START_TIME	AUDIO_END_DATE	AUDIO_END_TIME	AUDIO_DURATION
# In
# --------------------------------------------
# circadian_1_usv_results-evening-36-rows.csv
# --------------------------------------------

# Start: 2023-05-14 17:50:00
# End: 2023-05-14 18:10:00
# Duration: 1200.23 seconds
# Processing S:\dummy\-2023\circadian\USV\2023-05-14\BOX-F_2023-05-14_17-50-00.wav for box-f-23-05-14_17-49-56-56_00006.csv
# ffprobe output:
# [STREAM]
# duration=1200.234784
# [/STREAM]
# [FORMAT]
# TAG:date=2023-05-14
# TAG:creation_time=17:50:00
# [/FORMAT]

# done 20240521

import pandas as pd
import os
import subprocess
import re
from datetime import datetime, timedelta
import shutil

def run_ffprobe(file_path):
    command = [
        'ffprobe',
        '-hide_banner',
        '-v', 'quiet',
        '-print_format', 'default',
        '-show_entries', 'format_tags=date,creation_time',
        '-show_entries', 'stream=duration',
        file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.decode()

# csv_path = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/usv/usv_csvs/circadian_1_usv_results-evening-36-rows.csv"
csv_path = "D:/LEWIATAN/simb_circ_1_test_morning_12bp_all_33/project_folder/usv/usv_csvs/circadian_1_usv_results-morning-36-rows.csv"
original_csv_path = csv_path.replace('.csv', '_original_before_adding_audio_info_by_02.6.csv')

if not os.path.exists(original_csv_path):
    shutil.copy(csv_path, original_csv_path)
    print(f"Copied original CSV to {original_csv_path}")

df = pd.read_csv(csv_path)
print("CSV loaded.")

# Ensure the relevant columns are of object (string) type to avoid conversion issues
for column in ['AUDIO_START_DATE', 'AUDIO_START_TIME', 'AUDIO_END_DATE', 'AUDIO_END_TIME']:
    if column in df.columns:
        df[column] = df[column].astype(object)
    else:
        df[column] = pd.Series(dtype=object)

for index, row in df.iterrows():
    if pd.notna(row['Simba_file']):
        audio_file_path = row['AUDIO_FILE_NAME']
        if pd.notna(audio_file_path) and os.path.exists(audio_file_path):
            print(f"Processing {audio_file_path} for {row['Simba_file']}")
            ffprobe_output = run_ffprobe(audio_file_path)
            print(f"ffprobe output:\n{ffprobe_output}")

            date_match = re.search(r"TAG:date=([\d-]+)", ffprobe_output)
            creation_time_match = re.search(r"TAG:creation_time=([\d:]+)", ffprobe_output)
            duration_match = re.search(r"duration=([\d.]+)", ffprobe_output)

            if date_match and creation_time_match and duration_match:
                date_str = date_match.group(1)
                creation_time_str = creation_time_match.group(1)
                duration_seconds = float(duration_match.group(1))

                datetime_format = "%Y-%m-%d %H:%M:%S"
                start_datetime_str = f"{date_str} {creation_time_str}"
                start_datetime = datetime.strptime(start_datetime_str, datetime_format)
                end_datetime = start_datetime + timedelta(seconds=duration_seconds)

                print(f"Start: {start_datetime.strftime(datetime_format)}")
                print(f"End: {end_datetime.strftime(datetime_format)}")
                print(f"Duration: {duration_seconds:.2f} seconds")

                df.at[index, 'AUDIO_START_DATE'] = start_datetime.strftime('%Y-%m-%d')
                df.at[index, 'AUDIO_START_TIME'] = start_datetime.strftime('%H:%M:%S')
                df.at[index, 'AUDIO_END_DATE'] = end_datetime.strftime('%Y-%m-%d')
                df.at[index, 'AUDIO_END_TIME'] = end_datetime.strftime('%H:%M:%S')
                df.at[index, 'AUDIO_DURATION'] = duration_seconds
            else:
                print(f"Could not extract audio info for {audio_file_path}.")
        else:
            print(f"No audio file found or inaccessible for {row['Simba_file']}. If path is provided: {audio_file_path}")

df.to_csv(csv_path, index=False)
print("CSV updated.")

# 02.6-reads info on AUDIO based on ffprobe - alters - circadian_1_usv_results-evening-36-rows.csv !.py
