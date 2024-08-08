
# done 20240522

import pandas as pd
import os
import subprocess

# Path to the CSV file containing the list of filenames and corresponding audio files
# list_csv_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-evening-36-rows.csv'
list_csv_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-morning-36-rows.csv'

# Directory where the output AAC files will be saved
# output_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\3_audible-usv-to-add-to-videos-full-length'
output_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\3_audible-usv-to-add-to-videos-full-length'


def process_audio_files(list_csv_path, output_dir):
    # Load the CSV file containing the list of filenames
    df = pd.read_csv(list_csv_path)

    if 'Simba_file' not in df.columns or 'AUDIO_FILE_NAME' not in df.columns:
        print("The necessary columns are missing in the CSV file.")
        return

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for index, row in df.iterrows():
        simba_file = row['Simba_file']
        audio_file = row['AUDIO_FILE_NAME']

        if pd.isna(simba_file) or pd.isna(audio_file):
            print(f"Skipping row {index} due to missing data.")
            continue

        audio_file_path = os.path.join(os.path.dirname(list_csv_path), audio_file)
        output_file_path = os.path.join(output_dir, os.path.splitext(simba_file)[0] + '.aac')

        if not os.path.exists(audio_file_path):
            print(f"Audio file does not exist: {audio_file_path}")
            continue

        # Generate the FFmpeg command to convert WAV to AAC
        command = [
            'ffmpeg',
            '-y',  # Overwrite output files without asking
            '-i', audio_file_path,
            '-af', 'lowpass=65000,highpass=20000,asetrate=25000,atempo=2,atempo=2,atempo=2,atempo=1.25,volume=3',
            '-hide_banner',
            output_file_path
        ]

        # Execute the command and print the FFmpeg output directly to the console
        try:
            subprocess.run(command, check=True)
            print(f"Successfully processed and saved: {output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to process file {audio_file}. Error: {str(e)}")

# Call the function with the specified paths
process_audio_files(list_csv_path, output_dir)

# 12.1.0-LATER-convert WAV USV from disk S to audible AAC in disk D - works  ------------------.py
