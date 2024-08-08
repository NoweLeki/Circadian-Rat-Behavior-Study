# works and produces

# Frame number from AUDIO analysis	Begin frame time (s)	End frame time (s)
# 0	0	0.083333333
# 1	0.083333333	0.166666667
# 2	0.166666667	0.25
# 3	0.25	0.333333333
# 4	0.333333333	0.416666667

# This script
# Reads 
# D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-evening-36-rows.csv

# --------------------------------------------------------------------------------
# Analyzes their AUDIO duration and based on fps from video_info.csv file, outputs
# Frame number from AUDIO analysis	Begin frame time (s)	End frame time (s)
# In the
# D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes
# folder
# --------------------------------------------------------------------------------

# 02.7 -- We know the AUDIOS, and their BEG and END times for every frame

import os
import pandas as pd

# Define the folder where the new CSVs will be saved
# folder_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"
folder_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\4_csvs_with_frame_numbers_beg_end_and_zeroes"

# Check if the folder exists, if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Define the paths to the source CSVs
# source_csv_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-evening-36-rows.csv"
# video_info_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\logs\video_info.csv"
source_csv_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-morning-36-rows.csv" # twice !
video_info_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\logs\video_info.csv"

# Read the source CSV and get unique Simba_file entries
source_df = pd.read_csv(source_csv_path).drop_duplicates(subset='Simba_file')

# Read the video_info CSV
video_info_df = pd.read_csv(video_info_path)

# Initialize a counter for processed files
processed_files_count = 0

# Iterate over each row in the source DataFrame
for index, row in source_df.iterrows():
    simba_file = str(row['Simba_file'])  # Convert to string to handle any non-string entries
    if simba_file == 'nan':  # Check for 'nan' which is the string representation of NaN in pandas
        print("Skipping a row due to missing Simba_file information.")
        continue

    audio_duration = row['AUDIO_DURATION']

    # Extract the video name from simba_file to match with the video_info_df
    video_name = simba_file.rsplit('.', 1)[0]  # Remove the file extension

    # Find the corresponding FPS from video_info_df
    fps_info = video_info_df[video_info_df['Video'] == video_name]
    if fps_info.empty:
        print(f"No FPS was found in video_info.csv for the file {simba_file}")
        continue  # Skip this file and move to the next iteration
    else:
        fps = fps_info.iloc[0]['fps']

    # Check if audio_duration is NaN
    if pd.isnull(audio_duration):
        print(f"Skipping file {simba_file} due to NaN audio duration")
        continue  # Skip this iteration

    # Calculate the number of frames based on the audio duration and FPS
    num_frames = int(audio_duration * fps)

    # Print debugging info including the FPS
    print(f"Processing file {simba_file} - of {audio_duration} s duration - that is {num_frames + 1} rows - FPS = {fps}")

    # Create a DataFrame for the new CSV
    new_df = pd.DataFrame({
        'Frame number from audio analysis': range(num_frames + 1),
        'Begin frame time (s)': [i / fps for i in range(num_frames + 1)],
        'End frame time (s)': [(i + 1) / fps for i in range(num_frames)] + [audio_duration],
        'Probability_ALARM': [0] * (num_frames + 1),
        'ALARM': [0] * (num_frames + 1),
        'Probability_FLAT': [0] * (num_frames + 1),
        'FLAT': [0] * (num_frames + 1),
        'Probability_FRQ MODUL.': [0] * (num_frames + 1),
        'FRQ MODUL.': [0] * (num_frames + 1),
        'Probability_SHORT': [0] * (num_frames + 1),
        'SHORT': [0] * (num_frames + 1),
    })

    # Define the path for the new CSV without adding an extra .csv extension
    new_csv_path = os.path.join(folder_path, simba_file)

    # Save the new DataFrame as a CSV
    new_df.to_csv(new_csv_path, index=False)

    # Increment the processed files counter
    processed_files_count += 1

# Print the number of processed files
print(f"Total files processed: {processed_files_count}")


# 02.7-for AUDIO creates novel csvs in (4_csvs_with_frame_numbers_beg_end_and_zeroes).py
