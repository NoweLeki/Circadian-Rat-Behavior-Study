# done 20240522

import pandas as pd
import os
import subprocess

# Define paths
# adjustments_csv_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv'
# source_audible_full_length_audio_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\3_audible-usv-to-add-to-videos-full-length"
# destination_adjusted_audible_audio_folder = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\4_audible-usv-to-add-to-videos-shortened"
adjustments_csv_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\usv\usv_csvs\circadian_1_usv_results-morning-36-rows-with-audio-and-video_09.992.1.csv'
source_audible_full_length_audio_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\3_audible-usv-to-add-to-videos-full-length"
destination_adjusted_audible_audio_folder = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\4_audible-usv-to-add-to-videos-shortened"


# Ensure the adjusted audio folder exists
os.makedirs(destination_adjusted_audible_audio_folder, exist_ok=True)

# Load the adjustments CSV
adjustments_df = pd.read_csv(adjustments_csv_path)

# Iterate over unique audio filenames
for simba_file in adjustments_df['Simba_file'].dropna().unique():
    source_audio_path = os.path.join(source_audible_full_length_audio_folder, simba_file.replace('.csv', '.aac'))
    adjusted_audio_path = os.path.join(destination_adjusted_audible_audio_folder, simba_file.replace('.csv', '.aac'))

    # Extract adjustment parameters
    adjustment_row = adjustments_df[adjustments_df['Simba_file'] == simba_file].iloc[0]
    shorten_start_s = adjustment_row['Cut Start of Audio (s)']
    cut_end_s = adjustment_row['Cut End of Audio (s)']

    print(f"Processing {source_audio_path}....")

    if not os.path.exists(source_audio_path):
        print(f"Could not open audio: {source_audio_path}")
        continue

    # Get the total duration of the audio using ffprobe
    try:
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                '-of', 'default=noprint_wrappers=1:nokey=1', source_audio_path],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        total_duration_s = float(probe.stdout.strip())
    except Exception as e:
        print(f"Error determining the total duration of the audio: {e}")
        continue

    # Calculate the duration to keep after the start cut
    duration_to_keep_s = total_duration_s - shorten_start_s - cut_end_s

    if duration_to_keep_s <= 0:
        print(f"No duration left to keep for audio: {source_audio_path}")
        continue

    # Command to convert WAV to AAC using FFmpeg
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', source_audio_path,
        '-ss', str(shorten_start_s),  # Start cutting from this point
        '-t', str(duration_to_keep_s),  # Duration of the audio to keep
        '-c:a', 'copy',  # Use the same audio codec to avoid re-encoding
        adjusted_audio_path
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Processed and adjusted audio saved to {adjusted_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to process file {source_audio_path}. FFmpeg Error: {e.stderr.decode('utf-8')}")

# 12.1.4-LATER-based on 09.992.1 -- CUTS start and end of  audible AUDIO  ----------------------.py
