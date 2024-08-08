# done 20240522

import pandas as pd
import os
import cv2

# Define paths

# source_csv_folder = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\6_machine_results--behaviors-plus-usv-adjusted-final'
source_csv_folder = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\6_machine_results--behaviors-plus-usv-adjusted-final'

# adjustments_csv_path = r'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv'
adjustments_csv_path = r'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-morning-36-rows-with-audio-and-video_09.992.1.csv'

# source_video_folder = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/videos"
# adjusted_video_folder = "D:/LEWIATAN/simb_circ_1_test_evening_12bp_all_33/project_folder/frames/output/1_machine_results-behaviors-adjusted"
source_video_folder = "D:/LEWIATAN/simb_circ_1_test_morning_12bp_all_33/project_folder/videos"
adjusted_video_folder = "D:/LEWIATAN/simb_circ_1_test_morning_12bp_all_33/project_folder/frames/output/1_machine_results-behaviors-adjusted"


# Ensure the adjusted video folder exists
os.makedirs(adjusted_video_folder, exist_ok=True)

# Load the adjustments CSV
adjustments_df = pd.read_csv(adjustments_csv_path)

# Iterate over unique video filenames
for simba_file in adjustments_df['Simba_file'].dropna().unique():
    source_video_path = os.path.join(source_video_folder, simba_file.replace('.csv', '.mp4'))
    adjusted_video_path = os.path.join(adjusted_video_folder, simba_file.replace('.csv', '.mp4'))

    # Extract adjustment parameters
    adjustment_row = adjustments_df[adjustments_df['Simba_file'] == simba_file].iloc[0]
    shorten_start_s = adjustment_row['Cut Start of Video (s)']
    cut_end_s = adjustment_row['Cut End of Video (s)']
    fps = adjustment_row['FPS']

    print(f"Processing {source_video_path}....")

    # Load video
    cap = cv2.VideoCapture(source_video_path)
    if not cap.isOpened():
        print(f"Could not open video: {source_video_path}")
        continue

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(adjusted_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Check if frame should be skipped or added
        if frame_count <= shorten_start_s * fps or (cap.get(cv2.CAP_PROP_FRAME_COUNT) - frame_count) <= cut_end_s * fps:
            continue

        # Add frame number in small font in the lower left corner
        cv2.putText(frame, f'Frame: {frame_count}', (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        out.write(frame)

    # Release resources
    cap.release()
    out.release()

    print(f"Processed and adjusted video saved to {adjusted_video_path}")

# 12.0-LATER-based on 09.992.1 -- CUTS start and end of  VIDEO ----------------------------------.py
