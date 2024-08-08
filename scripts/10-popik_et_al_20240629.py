# 20240521 - ___ - a better way is 
# 02.7-for AUDIO creates novel csvs in (4_csvs_with_frame_numbers_beg_end_and_zeroes).py

# works and produces

# Frame number from video analysis	Begin frame time (s)	End frame time (s)
# 0	0	0.083333333
# 1	0.083333333	0.166666667
# 2	0.166666667	0.25
# 3	0.25	0.333333333
# 4	0.333333333	0.416666667

# Reads videos in sklearn_results-ini-v3-custom folder
# Analyzes their duration and based on fps from video_info.csv file, outputs
# Frame number from video analysis	Begin frame time (s)	End frame time (s)
# In the machine_results-plus_usvs folder

# 1 We know the videos, and their BEG and END times for every frame
# done 20240520 but inspect videos and cut them !!!!

import os
import pandas as pd
from moviepy.editor import VideoFileClip

# Directory paths
# video_folder_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom'
# video_info_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\logs\video_info.csv'
video_folder_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom'
video_info_path = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\logs\video_info.csv'

# Destination folder for new CSVs
# dest_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results-plus_usvs'
dest_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results-plus_usvs'

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

# Video info CSV path
video_info_df = pd.read_csv(video_info_path)

# Iterate through each video in the video_folder_path
for video_filename in os.listdir(video_folder_path):
    if video_filename.endswith('.mp4'):
        clean_name = video_filename.replace('_custom', '').replace('.mp4', '')
        matched_row = video_info_df[video_info_df['Video'].str.contains(clean_name, regex=False)]
        
        if not matched_row.empty:
            fps = matched_row['fps'].iloc[0]

            video_path = os.path.join(video_folder_path, video_filename)
            if os.path.exists(video_path):
                clip = VideoFileClip(video_path)
                video_duration = clip.duration  # Duration in seconds
                clip.close()

                # Calculate the number of frames (excluding the last frame for now)
                num_frames = int(fps * video_duration)

                # Prepare data for the new columns
                frame_numbers = range(num_frames)
                begin_times = [frame / fps for frame in frame_numbers]
                end_times = [(frame + 1) / fps for frame in frame_numbers]

                # Create a DataFrame for the new columns
                new_df = pd.DataFrame({
                    'Frame number from video analysis': frame_numbers,
                    'Begin frame time (s)': begin_times,
                    'End frame time (s)': end_times
                })

                # Append the last frame manually
                last_frame = pd.DataFrame({
                    'Frame number from video analysis': [num_frames],
                    'Begin frame time (s)': [end_times[-1]],
                    'End frame time (s)': [video_duration]
                })
                new_df = pd.concat([new_df, last_frame], ignore_index=True)

                # Define the filename for the new CSV
                new_file_path = os.path.join(dest_folder, f"{clean_name}.csv")

                # Save the DataFrame as a CSV
                new_df.to_csv(new_file_path, index=False)

print("Processing completed. New CSV files are saved in 'machine_results-plus_usvs' folder.")

# 02.6-__list-sklearn-VIDEO-with-their-fps--adds-new-column !!.py