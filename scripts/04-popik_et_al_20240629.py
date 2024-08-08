import os
import cv2
import pandas as pd
import numpy as np

# Directories
# csv_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\features_extracted\only_6'
# video_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\videos'
# output_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\frames\output\geometry_visualization\amber'

csv_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\fe-piotr-amber-109-feats\only_3'
video_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\videos'
output_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\frames\output\geometry_visualization\amber'

# done 20240520
# Shape properties and colors are defined here...

# Shape sizes
circle_size = 36    # whole body
triangle_size = 10   # head
square_size = 10     # anus

red_color = (3, 3, 252)         # BGR not RGB
violet_color = (238, 130, 238)
white_color = (255, 255, 255)
grey_color = (128, 128, 128)
black_color = (0, 0, 0)

# Smaller font, not bold
font_scale = 0.5
thickness = 1


# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# BEG Define functions for drawing shapes... -----------------------------------------------------
# Shape properties
shape_thickness = 2  # Adjust for desired shape outline thickness

def draw_triangle(frame, center, size, color, thickness):
    """Draw an equilateral triangle centered at (x, y)"""
    x, y = center
    # Calculate the vertices of the triangle
    vertices = np.array([
        [x, y - size],
        [x + size * np.sqrt(3) / 2, y + size / 2],
        [x - size * np.sqrt(3) / 2, y + size / 2]], np.int32)
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness=thickness)

def draw_square(frame, center, size, color, thickness):
    """Draw a square centered at (x, y)"""
    x, y = center
    top_left = (int(x - size / 2), int(y - size / 2))
    bottom_right = (int(x + size / 2), int(y + size / 2))
    cv2.rectangle(frame, top_left, bottom_right, color, thickness)
# EOF Define functions for drawing shapes... -----------------------------------------------------

# BEG Function to add movement text to frame -----------------------------------------------------
def add_movement_text_to_frame(frame, frame_count, frame_width, frame_height, df):

    font_scale = 0.5
    thickness = 1
    starting_y_position = frame_height - 550  # Adjust as needed

    red_color = (3, 3, 252)         # BGR not RGB
    green_color = (3, 252, 3)         # BGR not RGB
    white_color = (255, 255, 255)
    
    # Define metrics with their labels, critical values, and colors
    metrics = [
# BEG CONTACTS -----------------------------------------------------------------
        {'name': 'dist_between_centroids_centers', 'label': '01 dist centr centers', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
        {'name': 'dist_between_centroids_heads', 'label': '02 dist centr heads', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
        {'name': 'dist_between_centroids_anuses', 'label': '03 dist centr anuses', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
# EOF CONTACTS -----------------------------------------------------------------

# BEG ANOGENITAL ---------------------------------------------------------------
        {'name': 'dist_white_head_black_anus', 'label': '04/06 dist W head B anus', 'critical_value': 100, 'color_above': white_color, 'color_below': red_color},
        {'name': 'dist_black_head_white_anus', 'label': '05/07 dist B head W anus', 'critical_value': 100, 'color_above': white_color, 'color_below': red_color},
# EOF ANOGENITAL ---------------------------------------------------------------

# BEG HEAD-CENTER --------------------------------------------------------------
        {'name': 'dist_white_head_black_center', 'label': '06/16/08 dist W head B centr', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
        {'name': 'dist_black_head_white_center', 'label': '07/15/09 dist B head W centr', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
# END HEAD-CENTER --------------------------------------------------------------

# BEG distances between specific parts of animals  ------------------------------------------------------------------------------------------------------------------
# based on - __pr_curve-smae-with-permutation-imp-all-rows-rect-poly-addit-sets-without-hi-corr-features.xlsx
# 1. for adjacent lying:

# 1.1. Distance (mm) black_head_2-white_middle_1
# 1.2. Distance (mm) white_head_1-black_middle_2

# 1.3. Distance (mm) white_middle_1-black_anogenital_2
        {'name': 'dist_white_center_black_anogenital', 'label': '08/17 dist W center B anus', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
# 1.4. Distance (mm) black_middle_2-white_anogenital_1
        {'name': 'dist_black_center_white_anogenital', 'label': '09/18 dist B center W anus', 'critical_value': 100, 'color_above': white_color, 'color_below': green_color},
# END distances between specific parts of animals  ------------------------------------------------------------------------------------------------------------------

# BEG WHOLE ANIMAL movements  ---------------------------------------------------------------------------------------------------------------------------------------
        {'name': 'white_avg_movement', 'label': '10/19 MOVE W BP AVG', 'critical_value': 0.74, 'color_above': red_color, 'color_below': white_color},
        {'name': 'white_max_movement', 'label': '11/20 MOVE W BP MAX', 'critical_value': 3.0, 'color_above': red_color, 'color_below': white_color},
        {'name': 'black_avg_movement', 'label': '12/21 MOVE B BP AVG', 'critical_value': 0.74, 'color_above': red_color, 'color_below': white_color},
        {'name': 'black_max_movement', 'label': '13/22 MOVE B BP MAX', 'critical_value': 3.0, 'color_above': red_color, 'color_below': white_color},
# END WHOLE ANIMAL movements  ---------------------------------------------------------------------------------------------------------------------------------------


        {'name': 'white_centroids_avg_movement', 'label': '23 MOVE WH AVG CENTROID', 'critical_value': 0.59, 'color_above':red_color, 'color_below': white_color},
        {'name': 'white_centroids_max_movement', 'label': '24 MOVE WH MAX CENTROID', 'critical_value': 1.12, 'color_above':red_color, 'color_below': white_color},
        {'name': 'black_centroids_avg_movement', 'label': '25 MOVE BL AVG CENTROID', 'critical_value': 0.67, 'color_above':red_color, 'color_below': white_color},
        {'name': 'black_centroids_max_movement', 'label': '26 MOVE BL MAX CENTROID', 'critical_value': 1.29, 'color_above':red_color, 'color_below': white_color},
    
# BEG REARINGS -----------------------------------------------------------------
# SEE HEAD-ANUS
# END REARINGS -----------------------------------------------------------------
    
# BEG CONVEX HULLS -------------------------------------------------
        {'name': 'white_head_convex_hull', 'label': '/10 W HEAD CONVEX', 'critical_value': 360, 'color_above': red_color, 'color_below': white_color},
        {'name': 'black_head_convex_hull', 'label': '/11 B HEAD CONVEX', 'critical_value': 360, 'color_above': red_color, 'color_below': white_color},
        {'name': 'white_wholebody_convex_hull', 'label': '/12 W WHOLE CONVEX', 'critical_value': 9000, 'color_above': red_color, 'color_below': white_color},
        {'name': 'black_wholebody_convex_hull', 'label': '/13 B WHOLE CONVEX', 'critical_value': 9000, 'color_above': red_color, 'color_below': white_color},
# END CONVEX HULLS -------------------------------------------------

# BEG CURVES AND ANGLES -------------------------------------------------
        {'name': 'white_circle_fit_angle_curve', 'label': '27 W CIRCLE FIT', 'critical_value': 180, 'color_above': red_color, 'color_below': white_color},
        {'name': 'black_circle_fit_angle_curve', 'label': '28 B CIRCLE FIT', 'critical_value': 180, 'color_above': red_color, 'color_below': white_color},
# EOF CURVES AND ANGLES -------------------------------------------------

# BEG ROLLING WINDOWS -------------------------------------------------

            
        ]


    for metric in metrics:
        metric_value = int(round(df.loc[frame_count, metric['name']]))
        color_txt = metric['color_above'] if metric_value >= metric['critical_value'] else metric['color_below']
        cv2.putText(frame, f"{metric['label']}: {metric_value}", (frame_width - 300, starting_y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color_txt, thickness)
        starting_y_position += 15  # Move down for the next text

# EOF Function to add movement text to frame -----------------------------------------------------



# Process each CSV and corresponding video

for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_dir, csv_file)
        video_file = csv_file.replace('.csv', '.mp4')
        video_path = os.path.join(video_dir, video_file)
        output_video_path = os.path.join(output_dir, video_file.replace('.mp4', '_amber.mp4'))

        df = pd.read_csv(csv_path)
        print(f"Processing video: {video_file}...")

        cap = cv2.VideoCapture(video_path)
        frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count < len(df):
                # Drawing shapes based on DataFrame coordinates...

                # Example: Using a triangle for white_head, a circle for black_head, and a square for white_wholebody
                # Adjust as needed for centroids

                x, y = df.loc[frame_count, ['white_wholebody_centroid_x', 'white_wholebody_centroid_y']]
                cv2.circle(frame, (int(x), int(y)), circle_size, white_color, shape_thickness)            # red

                x, y = df.loc[frame_count, ['black_wholebody_centroid_x', 'black_wholebody_centroid_y']]
                cv2.circle(frame, (int(x), int(y)), circle_size, black_color, shape_thickness)            # violet

                x, y = df.loc[frame_count, ['white_head_centroid_x', 'white_head_centroid_y']]
                draw_triangle(frame, (int(x), int(y)), triangle_size, white_color, shape_thickness)

                x, y = df.loc[frame_count, ['black_head_centroid_x', 'black_head_centroid_y']]
                draw_triangle(frame, (int(x), int(y)), triangle_size, black_color, shape_thickness)

                x, y = df.loc[frame_count, ['white_anus_centroid_x', 'white_anus_centroid_y']]
                draw_square(frame, (int(x), int(y)), square_size, white_color, shape_thickness)

                x, y = df.loc[frame_count, ['black_anus_centroid_x', 'black_anus_centroid_y']]
                draw_square(frame, (int(x), int(y)), square_size, black_color, shape_thickness)

                green_color = (3, 252, 3)         # BGR not RGB


                x, y = df.loc[frame_count, ['white_wholebody_centroid_x_roll_mean_1_second', 'white_wholebody_centroid_y_roll_mean_1_second']]        # novel 20240327
                cv2.circle(frame, (int(x), int(y)), circle_size - 12, white_color, shape_thickness - 1)                         # novel 20240327

                x, y = df.loc[frame_count, ['black_wholebody_centroid_x_roll_mean_1_second', 'black_wholebody_centroid_y_roll_mean_1_second']]        # novel 20240327
                cv2.circle(frame, (int(x), int(y)), circle_size - 12, black_color, shape_thickness -1 )                         # novel 20240327

                x, y = df.loc[frame_count, ['white_head_centroid_x_roll_mean_1_second', 'white_head_centroid_y_roll_mean_1_second']]
                draw_triangle(frame, (int(x), int(y)), triangle_size - 5, white_color, shape_thickness - 1)

                x, y = df.loc[frame_count, ['black_head_centroid_x_roll_mean_1_second', 'black_head_centroid_y_roll_mean_1_second']]
                draw_triangle(frame, (int(x), int(y)), triangle_size - 5, black_color, shape_thickness - 1)

                x, y = df.loc[frame_count, ['white_anus_centroid_x_roll_mean_1_second', 'white_anus_centroid_y_roll_mean_1_second']]
                draw_square(frame, (int(x), int(y)), square_size - 5 , white_color, shape_thickness - 1)

                x, y = df.loc[frame_count, ['black_anus_centroid_x_roll_mean_1_second', 'black_anus_centroid_y_roll_mean_1_second']]
                draw_square(frame, (int(x), int(y)), square_size - 5, black_color, shape_thickness - 1)


                # Adding text overlays for movements
                add_movement_text_to_frame(frame, frame_count, frame_width, frame_height, df)

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

print("Processing completed.")

# 004-B_amber_feature_extraction_20230815-pp-10.1-plots !.py
