# needs folder 2_sklearn

import pandas as pd
import os
import subprocess
import cv2
from pydub import AudioSegment

# Define paths
# video_dir = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\2_sklearn_results-ini-v3-custom-usv"
# audio_dir = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\4_audible-usv-to-add-to-videos-shortened"
# output_dir = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\6_videos-with_audible-usv-shortened-pydub_cv2"
video_dir = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\2_sklearn_results-ini-v3-custom-usv"
audio_dir = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\4_audible-usv-to-add-to-videos-shortened"
output_dir = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\6_videos-with_audible-usv-shortened-pydub_cv2"

# done 20240522

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return audio.duration_seconds

def get_video_duration(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0
    video.release()
    return duration

def process_files(video_dir, audio_dir, output_dir):
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    results = []

    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        audio_path = os.path.join(audio_dir, video_file.replace('.mp4', '.aac'))

        if not os.path.exists(audio_path):
            continue

        video_duration = get_video_duration(video_path)
        audio_duration = get_audio_duration(audio_path)
        shortest_duration = min(video_duration, audio_duration)
        difference = abs(video_duration - audio_duration)
        shortest_source = 'video' if video_duration < audio_duration else 'audio'

        output_path = os.path.join(output_dir, video_file.replace('.mp4', '_audio.mp4'))

        command = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-i', audio_path,
            '-map', '0:v', '-map', '1:a',
            '-c:v', 'copy',
            '-t', f"{shortest_duration:.2f}",
            output_path
        ]
        subprocess.run(command, check=True)

        results.append(f"{video_file}\t{video_file.replace('.mp4', '.aac')}\t{video_duration:.2f}s\t{audio_duration:.2f}s\t{shortest_source} was shortest by {difference:.2f}s")

    print("\n".join(results))
    print(f"Total files processed: {len(results)}")

# Run the function
process_files(video_dir, audio_dir, output_dir)

"""20230506_175959_conc_C_.deinterlaced.mp4        20230506_175959_conc_C_.deinterlaced.aac        598.08s 652.59s video was shortest by 54.50s
20230506_181000_conc_A.deinterlaced.mp4 20230506_181000_conc_A.deinterlaced.aac 1199.33s        1200.13s        video was shortest by 0.79s
20230506_181001_conc_B.deinterlaced.mp4 20230506_181001_conc_B.deinterlaced.aac 1199.08s        1200.09s        video was shortest by 1.00s
20230507_181000_conc_A.deinterlaced.mp4 20230507_181000_conc_A.deinterlaced.aac 1199.75s        1200.13s        video was shortest by 0.38s
20230507_181000_conc_B.deinterlaced.mp4 20230507_181000_conc_B.deinterlaced.aac 1199.42s        1200.09s        video was shortest by 0.67s
20230507_181000_conc_C_.deinterlaced.mp4        20230507_181000_conc_C_.deinterlaced.aac        1199.17s        1200.09s        video was shortest by 0.92s
20230508_181000_conc_B_.mp4     20230508_181000_conc_B_.aac     1199.67s        1200.13s        video was shortest by 0.46s
20230508_181000_conc_C_.mp4     20230508_181000_conc_C_.aac     1199.75s        1200.09s        video was shortest by 0.34s
box-a-23-05-08_17-49-56-78_00001.deinterlaced.mp4       box-a-23-05-08_17-49-56-78_00001.deinterlaced.aac       1200.08s        1200.09s        video was shortest by 0.00s
box-a-23-05-09_17-49-56-59_00002.deinterlaced.mp4       box-a-23-05-09_17-49-56-59_00002.deinterlaced.aac       1200.08s        1200.09s        video was shortest by 0.00s
box-a-23-05-10_17-49-56-57_00003.mp4    box-a-23-05-10_17-49-56-57_00003.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-a-23-05-11_17-49-56-54_00004.mp4    box-a-23-05-11_17-49-56-54_00004.aac    1127.75s        1127.81s        video was shortest by 0.06s
box-b-23-05-09_17-49-56-33_00001.deinterlaced.mp4       box-b-23-05-09_17-49-56-33_00001.deinterlaced.aac       1200.08s        1200.09s        video was shortest by 0.00s
box-b-23-05-10_17-49-56-21_00002.mp4    box-b-23-05-10_17-49-56-21_00002.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-b-23-05-11_17-49-56-25_00003.mp4    box-b-23-05-11_17-49-56-25_00003.aac    1127.75s        1127.81s        video was shortest by 0.06s
box-c-23-05-09_17-49-56-46_00001.deinterlaced.mp4       box-c-23-05-09_17-49-56-46_00001.deinterlaced.aac       1200.08s        1200.09s        video was shortest by 0.00s
box-c-23-05-10_17-49-56-07_00002.deinterlaced.mp4       box-c-23-05-10_17-49-56-07_00002.deinterlaced.aac       1202.25s        1202.26s        video was shortest by 0.01s
box-c-23-05-11_17-49-56-00_00003.mp4    box-c-23-05-11_17-49-56-00_00003.aac    1127.75s        1127.81s        video was shortest by 0.06s
box-d-23-05-09_17-49-57-19_00001.deinterlaced.mp4       box-d-23-05-09_17-49-57-19_00001.deinterlaced.aac       1200.08s        1200.09s        video was shortest by 0.00s
box-d-23-05-10_17-49-56-58_00002.mp4    box-d-23-05-10_17-49-56-58_00002.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-d-23-05-11_17-49-56-56_00003.mp4    box-d-23-05-11_17-49-56-56_00003.aac    1127.75s        1127.85s        video was shortest by 0.10s
box-d-23-05-12_17-49-56-54_00004.mp4    box-d-23-05-12_17-49-56-54_00004.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-d-23-05-13_17-49-56-53_00005.mp4    box-d-23-05-13_17-49-56-53_00005.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-d-23-05-14_17-49-56-51_00006.mp4    box-d-23-05-14_17-49-56-51_00006.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-e-23-05-10_17-49-57-01_00002.mp4    box-e-23-05-10_17-49-57-01_00002.aac    1200.33s        1200.38s        video was shortest by 0.05s
box-e-23-05-11_17-49-56-99_00003.mp4    box-e-23-05-11_17-49-56-99_00003.aac    1201.75s        1201.96s        video was shortest by 0.21s
box-e-23-05-12_17-49-55-97_00004.mp4    box-e-23-05-12_17-49-55-97_00004.aac    1201.75s        1202.05s        video was shortest by 0.30s
box-e-23-05-13_17-49-55-94_00005.mp4    box-e-23-05-13_17-49-55-94_00005.aac    1201.75s        1202.01s        video was shortest by 0.26s
box-e-23-05-14_17-49-56-92_00006.mp4    box-e-23-05-14_17-49-56-92_00006.aac    1200.25s        1200.30s        video was shortest by 0.05s
box-f-23-05-10_17-49-56-57_00002.deinterlaced.mp4       box-f-23-05-10_17-49-56-57_00002.deinterlaced.aac       1200.33s        1200.43s        video was shortest by 0.09s
box-f-23-05-11_17-49-56-55_00003.mp4    box-f-23-05-11_17-49-56-55_00003.aac    1200.92s        1202.01s        video was shortest by 1.09s
box-f-23-05-12_17-49-56-61_00004.mp4    box-f-23-05-12_17-49-56-61_00004.aac    1201.75s        1202.01s        video was shortest by 0.26s
box-f-23-05-13_17-49-56-58_00005.mp4    box-f-23-05-13_17-49-56-58_00005.aac    1201.75s        1202.01s        video was shortest by 0.26s
box-f-23-05-14_17-49-56-56_00006.mp4    box-f-23-05-14_17-49-56-56_00006.aac    1200.25s        1200.30s        video was shortest by 0.05s
Total files processed: 34"""

"""20230507_061000_conc_A.deinterlaced.mp4 20230507_061000_conc_A.deinterlaced.aac 1199.25s        1200.09s        video was shortest by 0.84s
20230507_061001_conc_B.deinterlaced.mp4 20230507_061001_conc_B.deinterlaced.aac 1199.17s        1200.13s        video was shortest by 0.96s
20230507_061001_conc_C_.deinterlaced.mp4        20230507_061001_conc_C_.deinterlaced.aac        1199.08s        1200.09s        video was shortest by 1.00s
20230508_061000_conc_B_.deinterlaced.mp4        20230508_061000_conc_B_.deinterlaced.aac        1199.00s        1200.09s        video was shortest by 1.09s
20230508_061000_conc_C_.deinterlaced.mp4        20230508_061000_conc_C_.deinterlaced.aac        1199.83s        1200.13s        video was shortest by 0.29s
20230508_061001_conc_A_.deinterlaced.mp4        20230508_061001_conc_A_.deinterlaced.aac        1199.92s        1200.13s        video was shortest by 0.21s
20230509_061000_conc_B_.deinterlaced.mp4        20230509_061000_conc_B_.deinterlaced.aac        1199.75s        1200.13s        video was shortest by 0.38s
20230509_061000_conc_C_.deinterlaced.mp4        20230509_061000_conc_C_.deinterlaced.aac        1199.58s        1200.13s        video was shortest by 0.54s
box-a-23-05-09_05-49-56-49_00001.deinterlaced.mp4       box-a-23-05-09_05-49-56-49_00001.deinterlaced.aac       1199.92s        1200.13s        video was shortest by 0.21s
box-a-23-05-10_05-49-56-58_00002.mp4    box-a-23-05-10_05-49-56-58_00002.aac    1200.08s        1200.09s        video was shortest by 0.00s
box-a-23-05-11_05-49-56-56_00003.mp4    box-a-23-05-11_05-49-56-56_00003.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-a-23-05-12_05-49-56-53_00004.mp4    box-a-23-05-12_05-49-56-53_00004.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-b-23-05-10_05-49-56-23_00001.mp4    box-b-23-05-10_05-49-56-23_00001.aac    1200.08s        1200.09s        video was shortest by 0.00s
box-b-23-05-11_05-49-56-27_00002.mp4    box-b-23-05-11_05-49-56-27_00002.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-b-23-05-12_05-49-56-23_00003.mp4    box-b-23-05-12_05-49-56-23_00003.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-c-23-05-10_05-49-56-15_00001.mp4    box-c-23-05-10_05-49-56-15_00001.aac    1200.08s        1200.09s        video was shortest by 0.00s
box-c-23-05-11_05-49-55-99_00002.mp4    box-c-23-05-11_05-49-55-99_00002.aac    1202.17s        1202.18s        video was shortest by 0.01s
box-c-23-05-12_05-49-56-08_00003.mp4    box-c-23-05-12_05-49-56-08_00003.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-d-23-05-10_05-49-56-55_00001.mp4    box-d-23-05-10_05-49-56-55_00001.aac    1200.08s        1200.09s        video was shortest by 0.00s
box-d-23-05-11_05-49-56-53_00002.mp4    box-d-23-05-11_05-49-56-53_00002.aac    1202.17s        1202.18s        video was shortest by 0.01s
box-d-23-05-12_05-49-56-59_00003.mp4    box-d-23-05-12_05-49-56-59_00003.aac    1202.25s        1202.26s        video was shortest by 0.01s
box-d-23-05-13_05-49-56-58_00004.mp4    box-d-23-05-13_05-49-56-58_00004.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-d-23-05-14_05-49-56-56_00005.mp4    box-d-23-05-14_05-49-56-56_00005.aac    1202.17s        1202.22s        video was shortest by 0.05s
box-e-23-05-11_05-49-56-88_00002.mp4    box-e-23-05-11_05-49-56-88_00002.aac    1201.75s        1201.96s        video was shortest by 0.21s
box-e-23-05-12_05-49-56-06_00003.mp4    box-e-23-05-12_05-49-56-06_00003.aac    1201.67s        1201.71s        video was shortest by 0.04s
box-e-23-05-13_05-49-56-04_00004.mp4    box-e-23-05-13_05-49-56-04_00004.aac    1201.67s        1202.01s        video was shortest by 0.34s
box-e-23-05-14_05-49-55-93_00005.mp4    box-e-23-05-14_05-49-55-93_00005.aac    1201.67s        1201.75s        video was shortest by 0.08s
box-f-23-05-11_05-49-56-56_00002.mp4    box-f-23-05-11_05-49-56-56_00002.aac    1201.75s        1202.01s        video was shortest by 0.26s
box-f-23-05-12_05-49-56-62_00003.mp4    box-f-23-05-12_05-49-56-62_00003.aac    1201.67s        1201.75s        video was shortest by 0.08s
box-f-23-05-13_05-49-56-60_00004.mp4    box-f-23-05-13_05-49-56-60_00004.aac    1201.75s        1202.01s        video was shortest by 0.26s
box-f-23-05-14_05-49-56-57_00005.mp4    box-f-23-05-14_05-49-56-57_00005.aac    1201.67s        1201.75s        video was shortest by 0.08s
Total files processed: 31"""

# 12.1.7 - was - 6-LATER-insert audible AUDIO  to VIDEO - works - AudioSegment - CV2 --------------------.py
