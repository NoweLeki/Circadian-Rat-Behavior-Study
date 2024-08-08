# print(f"Updated information saved to {updated_csv_path} - NOTE: DO NOT CONSIDER THE LAST 4 COLUMNS - AND NOT DELETE THEM .... ")

# Reads
# --------------------------------------------
# circadian_1_usv_results-evening-36-rows.csv
# --------------------------------------------

# Loops over *.mp4 in
# video_dir = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/frames/output/sklearn_results-ini-v3-custom-usv"
# works also with
# video_dir = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\videos"
# Constructs START, END and video duration based on file names

# saves     circadian_1_usv_results-evening-36-rows-with-audio-and-video.csv
# done 20240522

import pandas as pd
import os
import re
import cv2  # Import OpenCV
from datetime import datetime, timedelta

# Paths
    # video_dir = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/frames/output/sklearn_results-ini-v3-custom-usv"
    # works also with
# video_dir = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\videos"
video_dir = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\videos"

# csv_path = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/usv/usv_csvs/circadian_1_usv_results-evening-36-rows.csv"
csv_path = "D:/LEWIATAN/simb_circ_1_test_morning_12bp_all_33/project_folder/usv/usv_csvs/circadian_1_usv_results-morning-36-rows.csv"
# updated_csv_path = csv_path.replace('.csv', '-with-audio-and-video_original_videos.csv')
updated_csv_path = csv_path.replace('.csv', '-with-audio-and-video.csv') # next script doesn't like "_original_videos"


# Load the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Ensure new columns exist
for column in ['VIDEO_FILE_NAME', 'VIDEO_START_DATE', 'VIDEO_START_TIME', 'VIDEO_END_DATE', 'VIDEO_END_TIME', 'VIDEO_DURATION', 'FPS', 
               'Shorten_video_START_by_s', 'Cut_video_END_by_s', 'Shorten_audio_START_by_s', 'Cut_audio_END_by_s']:
    if column not in df.columns:
        df[column] = None  # Initialize new columns with None

# Function to parse start datetime for box- format videos
def parse_start_datetime_from_box_filename(filename):
    parts = filename.split('_')
    if len(parts) > 1 and parts[0].startswith('box-'):
        date_parts = parts[0].split('-')[2:5]
        year = '20' + date_parts[0]
        month, day = date_parts[1:3]
        time_parts = parts[1].split('-')[:3]
        hour, minute, second = time_parts
        datetime_str = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return None

# Function to get video duration and fps
def get_video_details(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, 'N/A'
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    return duration, fps

# Function to calculate end datetime
def calculate_end_datetime(start_datetime, duration_seconds):
    return start_datetime + timedelta(seconds=duration_seconds)

# Iterate over the DataFrame
for index, row in df.iterrows():
    if pd.notna(row['Simba_file']):

#       video_filename = row['Simba_file'].replace('.csv', '_custom_usv.mp4')
# works also with
        video_filename = row['Simba_file'].replace('.csv', '.mp4')

        video_path = os.path.join(video_dir, video_filename)

        if os.path.exists(video_path):
            duration, fps = get_video_details(video_path)
            if video_filename.startswith("box-"):
                start_datetime = parse_start_datetime_from_box_filename(video_filename)
            else:
                match = re.search(r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', video_filename)
                if match:
                    start_datetime = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6))) - timedelta(seconds=duration)
            end_datetime = calculate_end_datetime(start_datetime, duration)

            # Update the DataFrame
            df.at[index, ['VIDEO_FILE_NAME', 'VIDEO_START_DATE', 'VIDEO_START_TIME', 'VIDEO_END_DATE', 'VIDEO_END_TIME', 'VIDEO_DURATION', 'FPS']] = [video_filename, start_datetime.strftime('%Y-%m-%d'), start_datetime.strftime('%H:%M:%S'), end_datetime.strftime('%Y-%m-%d'), end_datetime.strftime('%H:%M:%S'), duration, fps]

            # Logic for calculating and updating the new columns
            audio_start = datetime.strptime(f"{row['AUDIO_START_DATE']} {row['AUDIO_START_TIME']}", '%Y-%m-%d %H:%M:%S') if pd.notna(row['AUDIO_START_DATE']) and pd.notna(row['AUDIO_START_TIME']) else None
            audio_end = datetime.strptime(f"{row['AUDIO_END_DATE']} {row['AUDIO_END_TIME']}", '%Y-%m-%d %H:%M:%S') if pd.notna(row['AUDIO_END_DATE']) and pd.notna(row['AUDIO_END_TIME']) else None
            video_start = start_datetime
            video_end = end_datetime

            # Compare audio and video start times
            if audio_start and video_start:
                delta_start = (video_start - audio_start).total_seconds()
                df.at[index, 'Shorten_video_START_by_s'] = max(delta_start, 0)  # Video starts after audio
                df.at[index, 'Shorten_audio_START_by_s'] = max(-delta_start, 0)  # Audio starts after video

            # Compare audio and video end times
            if audio_end and video_end:
                delta_end = (audio_end - video_end).total_seconds()
                df.at[index, 'Cut_video_END_by_s'] = max(-delta_end, 0)  # Video ends after audio
                df.at[index, 'Cut_audio_END_by_s'] = max(delta_end, 0)  # Audio ends after video

        print(f"Corresponding video found: {video_filename} -> START Date: {start_datetime.strftime('%Y-%m-%d')} START Time: {start_datetime.strftime('%H:%M:%S')} END Date: {end_datetime.strftime('%Y-%m-%d')} END Time: {end_datetime.strftime('%H:%M:%S')} Duration: {duration:.2f} seconds FPS: {fps}")
    
# Save the updated DataFrame
df.to_csv(updated_csv_path, index=False)
print(f"Updated information saved to {updated_csv_path} - NOTE: DO NOT CONSIDER THE LAST 4 COLUMNS - AND NOT DELETE THEM .... ")

# 09.94-BAD-COLS-BUT MUST- reads OpenCV VIDEO info and saves as audio-and-video csv -----.py
