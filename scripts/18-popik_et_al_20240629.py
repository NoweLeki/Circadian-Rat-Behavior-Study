# Reads
# ----------------------------------------------------------------
# circadian_1_usv_results-evening-36-rows-with-audio-and-video.csv
# ----------------------------------------------------------------

# Analyzes and Saves
# -------------------------------------------------------------------------
# circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv
# -------------------------------------------------------------------------

# With
# Cut Start of Audio (s)	
# Cut Start of Video (s)	
# Cut End of Audio (s)	
# Cut End of Video (s)

# done 20240522

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Specify the paths to CSV files
# csv_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video.csv'
# updated_csv_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv'
csv_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-morning-36-rows-with-audio-and-video.csv'
updated_csv_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-morning-36-rows-with-audio-and-video_09.992.1.csv'

def update_csv_with_sync_info(csv_file_path, updated_csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.iloc[:, :-4]  # Remove the last 4 columns if needed

    # Initialize new columns with default NaN values and convert to type 'object'
    new_cols = ['Cut Start of Audio (s)', 'Cut Start of Video (s)', 'Cut End of Audio (s)', 'Cut End of Video (s)', 'Updated Audio Start Date', 'Updated Audio Start Time', 'Updated Video Start Date', 'Updated Video Start Time', 'Updated Audio End Date', 'Updated Audio End Time', 'Updated Video End Date', 'Updated Video End Time', 'Calculated Original Audio Duration (s)', 'Calculated Original Video Duration (s)', 'Calculated Updated Audio Duration (s)', 'Calculated Updated Video Duration (s)']
    for col in new_cols:
        df[col] = np.nan
        df[col] = df[col].astype('object')

    for index, row in df.iterrows():
        audio_start, audio_end, video_start, video_end = get_datetime_objects(row)

        if None in [audio_start, audio_end, video_start, video_end]:
            continue  # Skip rows with missing data

        original_audio_duration = (audio_end - audio_start).total_seconds()
        original_video_duration = (video_end - video_start).total_seconds()

        cut_start_audio = max(0, (video_start - audio_start).total_seconds())
        cut_start_video = max(0, (audio_start - video_start).total_seconds())

        updated_audio_duration = original_audio_duration - cut_start_audio
        updated_video_duration = original_video_duration - cut_start_video

        cut_end_audio = max(0, updated_audio_duration - updated_video_duration)
        cut_end_video = max(0, updated_video_duration - updated_audio_duration)

        final_updated_audio_duration = updated_audio_duration - cut_end_audio
        final_updated_video_duration = updated_video_duration - cut_end_video

        # Update DataFrame with calculated values
        df.at[index, new_cols] = [
            cut_start_audio, cut_start_video, cut_end_audio, cut_end_video,
            (audio_start + timedelta(seconds=cut_start_audio)).strftime('%Y-%m-%d'),
            (audio_start + timedelta(seconds=cut_start_audio)).strftime('%H:%M:%S'),
            (video_start + timedelta(seconds=cut_start_video)).strftime('%Y-%m-%d'),
            (video_start + timedelta(seconds=cut_start_video)).strftime('%H:%M:%S'),
            (audio_end - timedelta(seconds=cut_end_audio)).strftime('%Y-%m-%d'),
            (audio_end - timedelta(seconds=cut_end_audio)).strftime('%H:%M:%S'),
            (video_end - timedelta(seconds=cut_end_video)).strftime('%Y-%m-%d'),
            (video_end - timedelta(seconds=cut_end_video)).strftime('%H:%M:%S'),
            original_audio_duration, original_video_duration, final_updated_audio_duration, final_updated_video_duration
        ]

    # Save the updated DataFrame to a new CSV file
    df.to_csv(updated_csv_file_path, index=False)

def get_datetime_objects(row):
    def to_datetime(date, time):
        if pd.isna(date) or pd.isna(time):
            return None
        return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    
    audio_start = to_datetime(row['AUDIO_START_DATE'], row['AUDIO_START_TIME'])
    audio_end = to_datetime(row['AUDIO_END_DATE'], row['AUDIO_END_TIME'])
    video_start = to_datetime(row['VIDEO_START_DATE'], row['VIDEO_START_TIME'])
    video_end = to_datetime(row['VIDEO_END_DATE'], row['VIDEO_END_TIME'])

    return audio_start, audio_end, video_start, video_end

# Execute the function with the specified CSV file paths
update_csv_with_sync_info(csv_file_path, updated_csv_file_path)

# 09.992.1-analyzes START and END - saves 09.992.1 for further AUDIO and VIDEO cuts -----------.py
