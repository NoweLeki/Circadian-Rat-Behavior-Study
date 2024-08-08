# Reads CSVs in machine_results folder to show probabilities that a given classifier/behavior have occured and to mark RED those that are > threshold

# Reads videos in videos folder
# Reads INI file and all classifiers together with their thresholds

# Adds my interesting info to the videos and saves in the 
# sklearn folder
# D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom
# folder

# ABSOLUTELY NECESSARY FOR 
# 02.6-list-sklearn-videos-with-their-fps--adds-new-column !!.py

# done 20240520

import os
import cv2
import pandas as pd
import configparser

# Path to .ini file
    # ini_path = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v2.ini'
    # ini_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v2.ini"
    # ini_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v3.ini"

# ini_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v3-usv.ini"
ini_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v3-usv.ini"

# Directories
    # csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\csv\machine_results'
    # video_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\videos'
    # output_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp\project_folder\frames\output\sklearn_results'

# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\machine_results'
# video_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\videos'
    #
    #
    #
# output_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom-usv'

csv_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\machine_results'
video_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\videos'
    # Script 02.6-__list-sklearn-VIDEO-with-their-fps--adds-new-column !!.py reads "custom", not "custom-usv", so I changed here -------------
    # output_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom-usv'
    # Script 02.6-__list-sklearn-VIDEO-with-their-fps--adds-new-column !!.py reads "custom", not "custom-usv", so I changed here -------------
output_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\sklearn_results-ini-v3-custom'

# Create a ConfigParser object and read the .ini file
config = configparser.ConfigParser()
config.read(ini_path)

# Extract critical values from the 'threshold_settings' section
threshold_settings = {key: float(value) for key, value in config['threshold_settings'].items()}

# Columns of interest
columns = [
    "Probability_nosing", "Probability_following", "Probability_grooming",
    "Probability_anogenital sniffing", "Probability_mounting", "Probability_sniffing",
    "Probability_crawling", "Probability_fighting", "Probability_adjacent lying",
    "Probability_rearing", "Probability_self-grooming"
]

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Assuming 'cap', 'out', and 'df' are already defined
# Map columns to their corresponding threshold setting

threshold_mapping = {
    "Probability_nosing": "threshold_1",
    "Probability_following": "threshold_2",
    "Probability_grooming": "threshold_3",
    "Probability_anogenital sniffing": "threshold_4",
    "Probability_mounting": "threshold_5",
    "Probability_sniffing": "threshold_6",
    "Probability_crawling": "threshold_7",
    "Probability_fighting": "threshold_8",
    "Probability_adjacent lying": "threshold_9",
    "Probability_rearing": "threshold_10",
    "Probability_self-grooming": "threshold_11"
}

# Iterate through each frame in the videoimport os
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_dir, csv_file)
        video_name = csv_file.replace('.csv', '.mp4')
        video_path = os.path.join(video_dir, video_name)
        output_video_name = video_name.replace('.mp4', '_custom.mp4')
        output_video_path = os.path.join(output_dir, output_video_name)

        df = pd.read_csv(csv_path)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Could not open video: {video_path}")
            continue

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx < len(df):
                row = df.iloc[frame_idx]
                text_y = height - 20

                for col in columns:
                    if col in df.columns:
                        prob_value = row[col] if not pd.isna(row[col]) else 0.00
                        color = (0, 0, 255) if prob_value >= threshold_settings[threshold_mapping[col]] else (255, 255, 255)
                        # text = f"{prob_value:.2f} {col}"
                        # Determine text color based on the critical value
                        critical_value = threshold_settings[threshold_mapping[col]]
                        text = f"{critical_value:.3f} {prob_value:.3f} {col}" #

                        cv2.putText(frame, text, (width - 400, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                        text_y -= 20

                out.write(frame)
                frame_idx += 1

        cap.release()
        out.release()

print("Processing completed.")

# 008-sklearn_custom_v4 !.py
