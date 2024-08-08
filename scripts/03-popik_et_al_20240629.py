# based on and thanks to: Lapp et al., 2023
# https://github.com/lapphe/AMBER-pipeline/blob/main/AMBER_pose_estimation.py 

import os
from itertools import product
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
import math
import circle_fit
from simba.misc_tools import get_fn_ext, SimbaTimer
from simba.utils.printing import stdout_success
from simba.read_config_unit_tests import check_str
from simba.feature_extractors.unit_tests import read_video_info
from simba.feature_extractors.perimeter_jit import jitted_hull
from simba.mixins.config_reader import ConfigReader
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.rw_dfs import read_df, save_df

from simba.plotting.geometry_plotter import GeometryPlotter

# Explicit config_path

# WORKED for evening !
# config_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v2.ini"
config_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\simb_circ_1_test_12bp_v1_sh37_without_frames_removed-(all frames)--all-rows-simon-polygons-plus-piotr-amber-109-feats-v2.ini"

# Additional function definitions

def calculate_weighted_avg(x, p=None, threshold=0.2):
    if p is not None and len(x) != len(p):
        raise ValueError('Got x and p with different lengths')

    selected_x, selected_p = [], []
    if p is not None:
        p = [0 if val is None else val for val in p]
        for i in range(len(x)):
            if p[i] > threshold:
                selected_x.append(x[i])
                selected_p.append(p[i])

    if len(selected_x) > 0:
        return np.ma.average(selected_x, weights=selected_p)
    else:
        return np.ma.average(x)

def angle3pt(ax, ay, bx, by, cx, cy):
        ang = math.degrees(
            math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx))
        return ang + 360 if ang < 0 else ang

def count_high_p(p, threshold=0.2):
    return len([1 for val in p if val > threshold])

def get_circle_fit_angle(x, y, p, threshold=0.5):
    if np.average(p) < threshold:
        return(0)
    
    xc, yc, r, sigma = circle_fit.least_squares_circle(list(zip(x, y)))
    
    angle = math.degrees(math.atan2(y[-1] - yc, x[-1] - xc) 
                        - math.atan2(y[0] - yc, x[0] - xc))
    return angle + 360 if angle < 0 else angle

def polygon_fill(x, y, p, threshold=0.2):

    """
    Fills-in points with p lower than threshold. Uses points with p above the threshold to fill-in.
    :param x: List of x-coordinates
    :param y: List of y-coordinates
    :param p: List of probabilities
    :param threshold: Threshold for the probabilities
    :return: Filled-in x, y
    """

    if len(x) != len(y):
        raise ValueError('Got x and y with different lengths')
    if len(x) != len(p):
        raise ValueError('Got x and p with different lengths')

    selected_points = []
    for i in range(len(x)):
        if p[i] > threshold:
            selected_points.append([x[i], y[i]])

    if len(selected_points) < 3:
        return np.zeros((len(x), 2)).astype(np.float32)

    missing_points = len(x) - len(selected_points)
    if missing_points > 0:
        selected_points.extend([selected_points[0]] * missing_points)

    return np.array(selected_points).astype(np.float32)

# --------------------------------------------------------------------------------------------------------------------------

class UserDefinedFeatureExtractor(ConfigReader, FeatureExtractionMixin):

    """
    Class for featurizing data within SimBA project using user-defined body-parts in the pose-estimation data.
    Results are stored in the `project_folder/csv/features_extracted` directory of the SimBA project.
    """

    def __init__(self, config_path: str):
        ConfigReader.__init__(self, config_path=config_path)
        FeatureExtractionMixin.__init__(self)

        # Initialize the files_found attribute based on config 
        self.files_found = self.read_files_from_config()

        self.timer = SimbaTimer()
        self.timer.start_timer()
        print('Extracting features from {} file(s)...'.format(str(len(self.files_found))))
        self.extract_features()

    def extract_features(self):
        print('started extract_features ...')

        black_threshold = 0.4
        white_threshold = 0.4
        roll_windows_values = [1, 2, 5, 8, 0.5]  # values used to calculate rolling average across frames

        # for file_cnt, file_path in enumerate(self.files_found):
        # from piotr_120324_3-20240313-1940 !.py
        for file_cnt, file_path in enumerate(self.outlier_corrected_paths):
            # video_timer = SimbaTimer()
            # video_timer.start_timer()
            video_timer = SimbaTimer(start=True)
            _, video_name, _ = get_fn_ext(filepath=file_path)
            print(f'Processing {video_name} ... ')

            print('Extracting features for video ...............  {}/{}...'.format(str(file_cnt+1), str(len(self.files_found))))
            _, file_name, _ = get_fn_ext(file_path)
            check_str("file name", file_name)
            video_settings, self.px_per_mm, fps = self.read_video_info(video_name=file_name)
            pixels_per_mm = self.px_per_mm

            csv_df = read_df(file_path, self.file_type)

# works
            print(f'Processing {video_name} -- Video settings {video_settings} -- ')
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
            # Define all body parts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            # Body parts will be in two categories: white and black animals
            body_part_names = [x.replace('_x', '') for x in list(csv_df.columns) if '_x' in x]
            white_body_part_names, black_body_part_names = [], []
            for bp in body_part_names:
                if 'black' in bp:
                    black_body_part_names.append(bp)
                else:
                    white_body_part_names.append(bp)

            print("White body part names:\n", white_body_part_names)
            print("Black body part names:\n", black_body_part_names)
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
            # Do Simon's magic with NaNs and up/down interpolation - stolen from Simon's rectangles and polygons +++++++++++

            # csv_df = csv_df.fillna(0)
            csv_df = csv_df.drop(csv_df.index[[0]])                   # AMBER
            # PP 20230318 csv_df = csv_df.apply(pd.to_numeric)        # AMBER

            csv_df = csv_df.apply(pd.to_numeric, errors='coerce').fillna(0).replace(0, np.nan)    # SIMON <- PIOTR SEES NO DIFFERENCE ...
            csv_df = csv_df.interpolate(method='nearest').bfill().ffill()                         # SIMON <-- THIS FILLS MISSING DATA IN features_extracted !!! 
            csv_df = csv_df.reset_index(drop=True)                    # AMBER
# --------------------------------------------------------------------------------------------------------------------------


# 1 BEG CENTROIDS -> whole body -> head -> anus ----------------------------------------------------------------------------

            print("Starting to calculate white & black WHOLE BODY = CENTERS centroids...")

# 1.1. BEG whole body centroid ---------------------------------------------------------------------------------------------
# WHITE feature 1 2
#           white_center_parts = ['white_nose_1', 'white_left_eye_1', 'white_right_eye_1', 'white_head_1', 'white_back_1', 'white_pelvis_1', 'white_anogenital_1', 'white_left_shoulder_1', 'white_right_shoulder_1', 'white_middle_1']
            white_center_parts = ['white_head_1', 'white_back_1', 'white_pelvis_1', 'white_anogenital_1', 'white_left_shoulder_1', 'white_right_shoulder_1', 'white_middle_1'] # not nose, eyes

            # Calculate white centroids
            csv_df['white_wholebody_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in white_center_parts],[row[str(column) + '_p'] for column in white_center_parts],
            threshold=white_threshold), axis=1)
            
            csv_df['white_wholebody_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in white_center_parts],[row[str(column) + '_p'] for column in white_center_parts],
            threshold=white_threshold), axis=1)
            
            # After calculating white whole body centroids
            # print("Calculated white whole body centroid x-coordinates:\n", csv_df['white_wholebody_centroid_x'].head())
            # print("Calculated white whole body centroid y-coordinates:\n", csv_df['white_wholebody_centroid_y'].head())
            # input("Press Enter to continue...")

# BLACK feature 3 4
#           black_center_parts = ['black_nose_2', 'black_left_eye_2', 'black_right_eye_2', 'black_head_2', 'black_back_2', 'black_pelvis_2', 'black_anogenital_2', 'black_left_shoulder_2', 'black_right_shoulder_2', 'black_middle_2']
            black_center_parts = ['black_head_2', 'black_back_2', 'black_pelvis_2', 'black_anogenital_2', 'black_left_shoulder_2', 'black_right_shoulder_2', 'black_middle_2'] # not nose, eyes
            
            # Calculate black centroids
            csv_df['black_wholebody_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in black_center_parts],[row[str(column) + '_p'] for column in black_center_parts],
            threshold=black_threshold), axis=1)
            
            csv_df['black_wholebody_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in black_center_parts],[row[str(column) + '_p'] for column in black_center_parts],
            threshold=black_threshold), axis=1)
            
            # After calculating black whole body centroids
            # print("Calculated black whole body centroid x-coordinates:\n", csv_df['black_wholebody_centroid_x'].head())
            # print("Calculated black whole body centroid y-coordinates:\n", csv_df['black_wholebody_centroid_y'].head())
            # input("Press Enter to continue...")
# END whole body centroid --------------------------------------------------------------------------------------------------


# 1.2. BEG head centroid ---------------------------------------------------------------------------------------------------

            print("Starting to calculate white & black HEADS centroids...")

# WHITE feature 5 6
            white_head_parts = ['white_nose_1', 'white_left_eye_1', 'white_right_eye_1', 'white_head_1']

            csv_df['white_head_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in white_head_parts],[row[str(column) + '_p'] for column in white_head_parts],
            threshold=white_threshold), axis=1)

            csv_df['white_head_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in white_head_parts],[row[str(column) + '_p'] for column in white_head_parts],
            threshold=white_threshold), axis=1)

            # After calculating white head centroids
            # print("Calculated white head centroid x-coordinates:\n", csv_df['white_head_centroid_x'].head())
            # print("Calculated white head centroid y-coordinates:\n", csv_df['white_head_centroid_y'].head())
            # input("Press Enter to continue...")
# BLACK feature 7 8
            black_head_parts = ['black_nose_2', 'black_left_eye_2', 'black_right_eye_2', 'black_head_2']

            csv_df['black_head_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in black_head_parts],[row[str(column) + '_p'] for column in black_head_parts],
            threshold=black_threshold), axis=1)

            csv_df['black_head_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in black_head_parts],[row[str(column) + '_p'] for column in black_head_parts],
            threshold=black_threshold), axis=1)

            # After calculating black head centroids
            # print("Calculated black head centroid x-coordinates:\n", csv_df['black_head_centroid_x'].head())
            # print("Calculated black head centroid y-coordinates:\n", csv_df['black_head_centroid_y'].head())
            # input("Press Enter to continue...")
# END head centroid --------------------------------------------------------------------------------------------------------


# 1.3. BEG anus centroid ---------------------------------------------------------------------------------------------------
            print("Starting to calculate white & black ANUSES centroids...")
# WHITE feature 9 10
#           white_anus_parts = ['white_pelvis_1', 'white_anogenital_1', 'white_tail_1', 'white_middle_1', 'white_tail2_1']
            white_anus_parts = ['white_pelvis_1', 'white_anogenital_1', 'white_tail_1']

            csv_df['white_anus_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in white_anus_parts],[row[str(column) + '_p'] for column in white_anus_parts],
            threshold=white_threshold), axis=1)

            csv_df['white_anus_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in white_anus_parts],[row[str(column) + '_p'] for column in white_anus_parts],
            threshold=white_threshold), axis=1)

            # After calculating white anus centroids
            # print("Calculated white anus centroid x-coordinates:\n", csv_df['white_anus_centroid_x'].head())
            # print("Calculated white anus centroid y-coordinates:\n", csv_df['white_anus_centroid_y'].head())
            # input("Press Enter to continue...")

# BLACK feature 11 12
#           black_anus_parts = ['black_pelvis_2', 'black_anogenital_2', 'black_tail_2', 'black_middle_2', 'black_tail2_2']
            black_anus_parts = ['black_pelvis_2', 'black_anogenital_2', 'black_tail_2']

            csv_df['black_anus_centroid_x'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_x'] for column in black_anus_parts],[row[str(column) + '_p'] for column in black_anus_parts],
            threshold=black_threshold), axis=1)

            csv_df['black_anus_centroid_y'] = csv_df.apply(lambda row: calculate_weighted_avg([row[str(column) + '_y'] for column in black_anus_parts],[row[str(column) + '_p'] for column in black_anus_parts],
                threshold=black_threshold), axis=1)

            # After calculating black anus centroids
            # print("Calculated black anus centroid x-coordinates:\n", csv_df['black_anus_centroid_x'].head())
            # print("Calculated black anus centroid y-coordinates:\n", csv_df['black_anus_centroid_y'].head())
            # input("Press Enter to continue...")
# END anus centroid --------------------------------------------------------------------------------------------------------
# END OF CENTROIDS            


# POLYGONS = CONVEX HULLs -> whole body -> head ----------------------------------------------------------------------------
# WHITE
# feature 13            
            print("Starting to calculate white & black POLYGONS = CONVEX HULLS for CENTERS...")
            
            # BEG white whole body polygon (convex hull) -------------------------------------------------------------------------------
            white_wholebody_polygon = csv_df.apply(lambda row: polygon_fill([row[p + '_x'] for p in white_body_part_names],[row[p + '_y'] for p in white_body_part_names],[row[p + '_p'] for p in white_body_part_names], 0.2), axis=1)
            white_wholebody_polygon = np.array(white_wholebody_polygon.tolist()).reshape((len(white_wholebody_polygon), -1, 2)).astype(np.float32)

            # After calculating white whole body polygon
            # print("White whole body polygons shape:", white_wholebody_polygon.shape)

            csv_df['white_wholebody_convex_hull'] = jitted_hull(points=white_wholebody_polygon.astype(np.float32), target='area') / (pixels_per_mm ** 2)
            
            # After calculating white whole body convex hull
            # print("White whole body convex hull areas:\n", csv_df['white_wholebody_convex_hull'].head())
# BLACK
# feature 14
            black_wholebody_polygon = csv_df.apply(lambda row: polygon_fill([row[p + '_x'] for p in black_body_part_names],[row[p + '_y'] for p in black_body_part_names],[row[p + '_p'] for p in black_body_part_names], 0.2), axis=1)
            black_wholebody_polygon = np.array(black_wholebody_polygon.tolist()).reshape((len(black_wholebody_polygon), -1, 2)).astype(np.float32)

            # After calculating black whole body polygon
            # print("black whole body polygons shape:", black_wholebody_polygon.shape)

            csv_df['black_wholebody_convex_hull'] = jitted_hull(points=black_wholebody_polygon.astype(np.float32), target='area') / (pixels_per_mm ** 2)
            
            # After calculating black whole body convex hull
            # print("black whole body convex hull areas:\n", csv_df['black_wholebody_convex_hull'].head())
# END white whole body polygon (convex hull) ---------------------------------------------------------------------------------------------------------------


# BEG head polygon (convex hull) ---------------------------------------------------------------------------------------------------------------
            print("Starting to calculate white & black POLYGONS = CONVEX HULLS for HEADS...")

            # White head convex hull
            # white_head_parts defined for the centroid
# WHITE
# feature 15
            white_head_polygon = csv_df.apply(lambda row: polygon_fill([row[p + '_x'] for p in white_head_parts],[row[p + '_y'] for p in white_head_parts],[row[p + '_p'] for p in white_head_parts], 0.2), axis=1)
            white_head_polygon = np.array(white_head_polygon.tolist()).reshape((len(white_head_polygon), -1, 2)).astype(np.float32)
            csv_df['white_head_convex_hull'] = jitted_hull(points=white_head_polygon.astype(np.float32), target='area') / (pixels_per_mm ** 2)

            # After calculating white head convex hull
            # print("White head convex hull areas:\n", csv_df['white_head_convex_hull'].head())
# WHITE
# feature 16
            # Black head convex hull
            # black_head_parts defined for the centroid
            black_head_polygon = csv_df.apply(lambda row: polygon_fill([row[p + '_x'] for p in black_head_parts],[row[p + '_y'] for p in black_head_parts],[row[p + '_p'] for p in black_head_parts], 0.2), axis=1)
            black_head_polygon = np.array(black_head_polygon.tolist()).reshape((len(black_head_polygon), -1, 2)).astype(np.float32)
            csv_df['black_head_convex_hull'] = jitted_hull(points=black_head_polygon.astype(np.float32), target='area') / (pixels_per_mm ** 2)
            # @@ NEEDED FOR REARING

            # After calculating black head convex hull
            # print("black head convex hull areas:\n", csv_df['black_head_convex_hull'].head())
# EOF head polygon (convex hull) ---------------------------------------------------------------------------------------------------------------

# BEG distances within animal ------------------------------------------------------------------------------------------------------------------
# feature 17, 18, 19, 20, 21, 22
            # WITHIN ANIMAL

            # to see rearing (animal should stay motionless) ++++++++++++++++++++++++++++
            csv_df['dist_white_head_anus'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['white_anus_centroid_x']) ** 2 +(csv_df['white_head_centroid_y'] - csv_df['white_anus_centroid_y']) ** 2) / pixels_per_mm  # white y black y (between parts)
            csv_df['dist_black_head_anus'] = np.sqrt((csv_df['black_head_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 +(csv_df['black_head_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm  # (between parts)
            # @@ NOT NEEDED FOR REARING

            csv_df['dist_white_center_anus'] = np.sqrt((csv_df['white_wholebody_centroid_x'] - csv_df['white_anus_centroid_x']) ** 2 +(csv_df['white_wholebody_centroid_y'] - csv_df['white_anus_centroid_y']) ** 2) / pixels_per_mm  # white y black y (between parts)
            csv_df['dist_black_center_anus'] = np.sqrt((csv_df['black_wholebody_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 +(csv_df['black_wholebody_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm  # (between parts)
            # @@ NEEDED FOR REARING

            csv_df['dist_white_center_head'] = np.sqrt((csv_df['white_wholebody_centroid_x'] - csv_df['white_head_centroid_x']) ** 2 +(csv_df['white_wholebody_centroid_y'] - csv_df['white_head_centroid_y']) ** 2) / pixels_per_mm  # white y black y (between parts)
            csv_df['dist_black_center_head'] = np.sqrt((csv_df['black_wholebody_centroid_x'] - csv_df['black_head_centroid_x']) ** 2 +(csv_df['black_wholebody_centroid_y'] - csv_df['black_head_centroid_y']) ** 2) / pixels_per_mm  # (between parts)
# EOF distances within animal ------------------------------------------------------------------------------------------------------------------


# BEG distances between animals  ---------------------------------------------------------------------------------------------------------------
        # BETWEEN ANIMALS
# feature 23, 24, 25
            print("Starting to calculate white & black DISTANCES BETWEEN CENTROIDS...")

            # to see contacts +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            csv_df['dist_between_centroids_centers'] = np.sqrt((csv_df['white_wholebody_centroid_x'] - csv_df['black_wholebody_centroid_x']) ** 2 + (csv_df['white_wholebody_centroid_y'] - csv_df['black_wholebody_centroid_y']) ** 2) / pixels_per_mm
            csv_df['dist_between_centroids_heads'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['black_head_centroid_x']) ** 2 +(csv_df['white_head_centroid_y'] - csv_df['black_head_centroid_y']) ** 2) / pixels_per_mm
            csv_df['dist_between_centroids_anuses'] = np.sqrt((csv_df['white_anus_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 +(csv_df['white_anus_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm

# feature 26, 27, 28, 29
            # to see anogenital sniff (animal should stay motionless) +++++++++++++++++++
            csv_df['dist_white_head_black_anus'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 + (csv_df['white_head_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm
            csv_df['dist_black_head_white_anus'] = np.sqrt((csv_df['black_head_centroid_x'] - csv_df['white_anus_centroid_x']) ** 2 + (csv_df['black_head_centroid_y'] - csv_df['white_anus_centroid_y']) ** 2) / pixels_per_mm
            
            # to see head-center contacts (head-head already defined) +++++++++++++++++++
            csv_df['dist_white_head_black_center'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['black_wholebody_centroid_x']) ** 2 + (csv_df['white_head_centroid_y'] - csv_df['black_wholebody_centroid_y']) ** 2) / pixels_per_mm
            csv_df['dist_black_head_white_center'] = np.sqrt((csv_df['black_head_centroid_x'] - csv_df['white_wholebody_centroid_x']) ** 2 + (csv_df['black_head_centroid_y'] - csv_df['white_wholebody_centroid_y']) ** 2) / pixels_per_mm
# EOF distances between animals  ---------------------------------------------------------------------------------------------------------------


# BEG distances between specific parts of animals  ---------------------------------------------------------------------------------------------
# based on - __pr_curve-smae-with-permutation-imp-all-rows-rect-poly-addit-sets-without-hi-corr-features.xlsx

# 1. for adjacent lying:

# 1.1. Distance (mm) black_head_2-white_middle_1
#            csv_df['black_head_2-white_middle_1'] = np.sqrt((csv_df['black_head_centroid_x'] - csv_df['white_wholebody_centroid_x']) ** 2 + (csv_df['black_head_centroid_y'] - csv_df['white_wholebody_centroid_y']) ** 2) / pixels_per_mm
# already defined as dist_black_head_white_center

# 1.2. Distance (mm) white_head_1-black_middle_2
#            csv_df['white_head_1-black_middle_2'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['black_wholebody_centroid_x']) ** 2 + (csv_df['white_head_centroid_y'] - csv_df['black_wholebody_centroid_y']) ** 2) / pixels_per_mm
# already defined as dist_white_head_black_center            

# features 30, 31
# 1.3. Distance (mm) white_middle_1-black_anogenital_2
            csv_df['dist_white_center_black_anogenital'] = np.sqrt((csv_df['white_wholebody_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 + (csv_df['white_wholebody_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm

# 1.4. Distance (mm) black_middle_2-white_anogenital_1
            csv_df['dist_black_center_white_anogenital'] = np.sqrt((csv_df['black_wholebody_centroid_x'] - csv_df['white_anus_centroid_x']) ** 2 + (csv_df['black_wholebody_centroid_y'] - csv_df['white_anus_centroid_y']) ** 2) / pixels_per_mm

# ALREADY AS 06
# 1.5. Distance (mm) white_head_1-black_anogenital_2
#            csv_df['white_head_1-black_anogenital_2'] = np.sqrt((csv_df['white_head_centroid_x'] - csv_df['black_anus_centroid_x']) ** 2 + (csv_df['white_head_centroid_y'] - csv_df['black_anus_centroid_y']) ** 2) / pixels_per_mm

# ALREADY AS 07
# 1.6. Distance (mm) black_head_2-white_anogenital_1
#            csv_df['black_head_2-white_anogenital_1'] = np.sqrt((csv_df['black_head_centroid_x'] - csv_df['white_anus_centroid_x']) ** 2 + (csv_df['black_head_centroid_y'] - csv_df['white_anus_centroid_y']) ** 2) / pixels_per_mm

# EOF distances between specific parts of animals  -------------------------------------------------------------------------



# BEG movements 245-284 ----------------------------------------------------------------------------------------------------
# EVERY BODY PART
# feature 32-59

# to do: white movement white_head_1 (mm) @@
            # Calculate movements
            print('Calculating movements')

# WHITE
            white_movement_columns = white_body_part_names

 # ['white_nose_1', 'white_left_eye_1', 'white_right_eye_1', 'white_head_1', 'white_back_1', 'white_pelvis_1', 'white_anogenital_1', 'white_left_shoulder_1', 'white_right_shoulder_1', 'white_tail_1', 'white_middle_1', 'white_tail2_1']
 
            # Create a shifted dataframe and combine to use for movement calculations
            csv_df_shifted = csv_df.shift(periods=1)
            # This line creates a new DataFrame (csv_df_shifted) by shifting the original DataFrame (csv_df) down by one row. 
            # This means that each row in csv_df_shifted will contain the data from the row above it in csv_df. The first row in csv_df_shifted will be filled with NaN values because there's no row above the first row.
            csv_df_shifted.columns = [i + '_shifted' for i in csv_df.columns.values.tolist()]
            # This line renames the columns of csv_df_shifted by adding _shifted to the end of each original column name. 
            # This is done to differentiate between the current and previous frame's values when the two DataFrames are combined.
            csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')
            # This line concatenates the original DataFrame (csv_df) and the shifted DataFrame (csv_df_shifted) side by side (since axis=1). 
            # The join='inner' argument ensures that only rows with indices present in both DataFrames are kept in the combined DataFrame (csv_df_combined).
            csv_df_combined = csv_df_combined.fillna(0)
            # This line replaces all NaN values in csv_df_combined with 0. This is particularly important for the first row of the shifted DataFrame, which was filled with NaN values during the shift operation.
            csv_df_combined = csv_df_combined.reset_index(drop=True)
            # This resets the index of csv_df_combined, dropping the old index and replacing it with a new integer index starting from 0. 
            # This is often a good practice when manipulating DataFrames to ensure the index is clean and sequential.

            for bp in white_movement_columns:
                column_name = bp + '_movement'
                x1, y1 = (bp + '_x', bp + '_y')
                x2, y2 = (bp + '_x_shifted', bp + '_y_shifted')
                csv_df[column_name] = (np.sqrt((csv_df_combined[x1] - csv_df_combined[x2]) ** 2 + (csv_df_combined[y1] - csv_df_combined[y2]) ** 2)) / pixels_per_mm
                csv_df.at[0, column_name] = np.average(csv_df[column_name].iloc[1:10])

                print('Calculating Movements for ...', column_name)

                # Calculate movements:
# The for loop iterates over each body part in white_movement_columns, calculating the movement for each body part between consecutive frames:


            # Calculate average movements
            white_movements = ['white_nose_1_movement', 'white_left_eye_1_movement', 'white_right_eye_1_movement', 'white_head_1_movement',
                                'white_back_1_movement', 'white_pelvis_1_movement', 'white_anogenital_1_movement', 'white_left_shoulder_1_movement',
                                'white_right_shoulder_1_movement', 'white_tail_1_movement',	'white_middle_1_movement', 'white_tail2_1_movement']


            white_movements_p = ['white_nose_1_p', 'white_left_eye_1_p', 'white_right_eye_1_p', 'white_head_1_p', 
                                 'white_back_1_p', 'white_pelvis_1_p', 'white_anogenital_1_p', 'white_left_shoulder_1_p', 
                                 'white_right_shoulder_1_p', 'white_middle_1_p', 'white_tail_1_p', 'white_tail2_1_p']
            
                
            csv_df['white_avg_movement'] = csv_df.apply(lambda row: calculate_weighted_avg(
                [row[d] for d in white_movements],
                [row[d] for d in white_movements_p],
                threshold=white_threshold), axis=1)

            csv_df['white_max_movement'] = np.ma.max([csv_df['white_nose_1_movement'], csv_df['white_left_eye_1_movement'],
                                                    csv_df['white_right_eye_1_movement'], csv_df['white_head_1_movement'],
                                                    csv_df['white_back_1_movement'], csv_df['white_pelvis_1_movement'],
                                                    csv_df['white_anogenital_1_movement'], csv_df['white_left_shoulder_1_movement'],
                                                    csv_df['white_right_shoulder_1_movement'], csv_df['white_middle_1_movement'],
                                                    csv_df['white_tail_1_movement'],csv_df['white_tail2_1_movement']], axis=0)      

# BLACK

            black_movement_columns = black_body_part_names

            csv_df_shifted = csv_df.shift(periods=1)
            csv_df_shifted.columns = [i + '_shifted' for i in csv_df.columns.values.tolist()]
            csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')
            csv_df_combined = csv_df_combined.fillna(0)
            csv_df_combined = csv_df_combined.reset_index(drop=True)

            for bp in black_movement_columns:
                column_name = bp + '_movement'
                x1, y1 = (bp + '_x', bp + '_y')
                x2, y2 = (bp + '_x_shifted', bp + '_y_shifted')
                csv_df[column_name] = (np.sqrt((csv_df_combined[x1] - csv_df_combined[x2]) ** 2 + (csv_df_combined[y1] - csv_df_combined[y2]) ** 2)) / pixels_per_mm
                csv_df.at[0, column_name] = np.average(csv_df[column_name].iloc[1:10])


            # Calculate average movements
            black_movements = ['black_nose_2_movement', 'black_left_eye_2_movement', 'black_right_eye_2_movement', 'black_head_2_movement',
                                'black_back_2_movement', 'black_pelvis_2_movement', 'black_anogenital_2_movement', 'black_left_shoulder_2_movement',
                                'black_right_shoulder_2_movement', 'black_tail_2_movement',	'black_middle_2_movement', 'black_tail2_2_movement']


            black_movements_p = ['black_nose_2_p', 'black_left_eye_2_p', 'black_right_eye_2_p', 'black_head_2_p', 
                                 'black_back_2_p', 'black_pelvis_2_p', 'black_anogenital_2_p', 'black_left_shoulder_2_p', 
                                 'black_right_shoulder_2_p', 'black_middle_2_p', 'black_tail_2_p', 'black_tail2_2_p']
            
                
            csv_df['black_avg_movement'] = csv_df.apply(lambda row: calculate_weighted_avg(
                [row[d] for d in black_movements],
                [row[d] for d in black_movements_p],
                threshold=black_threshold), axis=1)

            csv_df['black_max_movement'] = np.ma.max([csv_df['black_nose_2_movement'], csv_df['black_left_eye_2_movement'],
                                                    csv_df['black_right_eye_2_movement'], csv_df['black_head_2_movement'],
                                                    csv_df['black_back_2_movement'], csv_df['black_pelvis_2_movement'],
                                                    csv_df['black_anogenital_2_movement'], csv_df['black_left_shoulder_2_movement'],
                                                    csv_df['black_right_shoulder_2_movement'], csv_df['black_middle_2_movement'],
                                                    csv_df['black_tail_2_movement'],csv_df['black_tail2_2_movement']], axis=0)      

# CENTROID MOVEMENTS
# feature 60-69

            # Define lists of centroid pairs for white and black animals
            centroid_pairs_white = [
                ('white_wholebody_centroid_x', 'white_wholebody_centroid_y'),
                ('white_head_centroid_x', 'white_head_centroid_y'),
                ('white_anus_centroid_x', 'white_anus_centroid_y')
                # Add more pairs as needed
            ]

            centroid_pairs_black = [
                ('black_wholebody_centroid_x', 'black_wholebody_centroid_y'),
                ('black_head_centroid_x', 'black_head_centroid_y'),
                ('black_anus_centroid_x', 'black_anus_centroid_y')
                # Add more pairs as needed
            ]

            # Function to calculate movements for given centroid pairs
            def calculate_individual_centroid_movements(centroid_pairs, color_prefix):
                movement_columns = []  # To store movement columns for overall average and max calculations
                for x_col, y_col in centroid_pairs:
                    movement_col = f'{x_col[:-2]}_movement'  # Remove '_x' and append '_movement'
                    movement_columns.append(movement_col)  # Add movement column to the list for later aggregation
                    
                    x1, y1 = x_col, y_col
                    x2, y2 = f'{x_col}_shifted', f'{y_col}_shifted'
                    
                    # Calculate the movement for the current centroid
                    csv_df[movement_col] = np.sqrt((csv_df_combined[x1] - csv_df_combined[x2]) ** 2 + (csv_df_combined[y1] - csv_df_combined[y2]) ** 2) / pixels_per_mm
                    # Manage the first row by setting its value to the average of the next few values
                    csv_df.at[0, movement_col] = np.average(csv_df[movement_col].iloc[1:10])

                    # white_centroids_avg_movement etc
                
                # Insert new columns for the average and max movements of the group
                avg_movement_col = f'{color_prefix}_centroids_avg_movement'
                max_movement_col = f'{color_prefix}_centroids_max_movement'
                csv_df[avg_movement_col] = csv_df[movement_columns].mean(axis=1)
                csv_df[max_movement_col] = csv_df[movement_columns].max(axis=1)

            # Prepare the DataFrame for movement calculations
            csv_df_shifted = csv_df.shift(periods=1)
            csv_df_shifted.columns = [i + '_shifted' for i in csv_df.columns.values.tolist()]
            csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')
            csv_df_combined = csv_df_combined.fillna(0)
            csv_df_combined = csv_df_combined.reset_index(drop=True)

            # Calculate movements for white and black centroid pairs
            calculate_individual_centroid_movements(centroid_pairs_white, 'white')
            calculate_individual_centroid_movements(centroid_pairs_black, 'black')
# EOF movements 245-295 ----------------------------------------------------------------------------------------------------------------------
            

# BEG 383-393 AVERAGE AND SUM PROBABILITIES ----------------------------------------------------------------------------------------------------
# feature 70-73
            print('Calculating white sum of probababilities ...')   #, column_name)

            white_bp_columns = [
                'white_nose_1_p', 'white_left_eye_1_p', 'white_right_eye_1_p', 'white_head_1_p',
                'white_back_1_p', 'white_pelvis_1_p', 'white_anogenital_1_p', 'white_left_shoulder_1_p',
                'white_right_shoulder_1_p', 'white_middle_1_p', 'white_tail_1_p', 'white_tail2_1_p'
            ]

            # Calculate the average using np.ma.average
            csv_df['average_white_bp_probabilities'] = np.ma.average(csv_df[white_bp_columns], axis=1)

            # Calculate the sum using DataFrame.sum()
            csv_df['sum_white_bp_probabilities'] = csv_df[white_bp_columns].sum(axis=1)



            black_bp_columns = [
                'black_nose_2_p', 'black_left_eye_2_p', 'black_right_eye_2_p', 'black_head_2_p',
                'black_back_2_p', 'black_pelvis_2_p', 'black_anogenital_2_p', 'black_left_shoulder_2_p',
                'black_right_shoulder_2_p', 'black_middle_2_p', 'black_tail_2_p', 'black_tail2_2_p'
            ]

            # Calculate the average using np.ma.average
            csv_df['average_black_bp_probabilities'] = np.ma.average(csv_df[black_bp_columns], axis=1)

            # Calculate the sum using DataFrame.sum()
            csv_df['sum_black_bp_probabilities'] = csv_df[black_bp_columns].sum(axis=1)
# EOF 383-393 AVERAGE AND SUM PROBABILITIES ----------------------------------------------------------------------------------------------------

# BEG 395-419 CIRCLE = CURVE AND ANGLES --------------------------------------------------------------------------------------------------------
# feature 74-75

            print('Calculating fields = angles')

            white_angle_1_ps = [
                'white_nose_1_p', 'white_head_1_p',
                'white_back_1_p', 'white_middle_1_p', 
                'white_pelvis_1_p', 'white_anogenital_1_p',
                'white_tail_1_p', 'white_tail2_1_p'
            ]

            white_angle_1_xs = [
                'white_nose_1_x', 'white_head_1_x',
                'white_back_1_x', 'white_middle_1_x', 
                'white_pelvis_1_x', 'white_anogenital_1_x',
                'white_tail_1_x', 'white_tail2_1_x'
            ]

            white_angle_1_ys = [
                'white_nose_1_y', 'white_head_1_y',
                'white_back_1_y', 'white_middle_1_y', 
                'white_pelvis_1_y', 'white_anogenital_1_y', 
                'white_tail_1_y', 'white_tail2_1_y'
            ]

            csv_df['white_circle_fit_angle_curve'] = csv_df.apply(lambda row: get_circle_fit_angle(
                [row[p] for p in white_angle_1_xs],
                [row[p] for p in white_angle_1_ys],
                [row[p] for p in white_angle_1_ps]), axis=1)



            black_angle_2_ps = [
                'black_nose_2_p', 'black_head_2_p',
                'black_back_2_p', 'black_middle_2_p', 
                'black_pelvis_2_p', 'black_anogenital_2_p',
                'black_tail_2_p', 'black_tail2_2_p'
            ]

            black_angle_2_xs = [
                'black_nose_2_x', 'black_head_2_x',
                'black_back_2_x', 'black_middle_2_x', 
                'black_pelvis_2_x', 'black_anogenital_2_x',
                'black_tail_2_x', 'black_tail2_2_x'
            ]

            black_angle_2_ys = [
                'black_nose_2_y', 'black_head_2_y',
                'black_back_2_y', 'black_middle_2_y', 
                'black_pelvis_2_y', 'black_anogenital_2_y', 
                'black_tail_2_y', 'black_tail2_2_y'
            ]

            csv_df['black_circle_fit_angle_curve'] = csv_df.apply(lambda row: get_circle_fit_angle(
                [row[p] for p in black_angle_2_xs],
                [row[p] for p in black_angle_2_ys],
                [row[p] for p in black_angle_2_ps]), axis=1)
            

# feature 76-81
               
            # Angle (degrees) anogenital tail tail2     # ADJACENT, CRAWL, FIGHT, GROOM, MOUNT, REAR
            csv_df['white_ano_tail1_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['white_anogenital_1_x'], 
                x['white_anogenital_1_y'], 
                x['white_tail_1_x'], 
                x['white_tail_1_y'], 
                x['white_tail2_1_x'], 
                x['white_tail2_1_y']
                ), axis=1)

            # Angle (degrees) back anogenital tail2     # ADJACENT, ANOGENITAL SNIFF, SNIFF
            csv_df['white_back_ano_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['white_back_1_x'], 
                x['white_back_1_y'], 
                x['white_anogenital_1_x'], 
                x['white_anogenital_1_y'], 
                x['white_tail2_1_x'], 
                x['white_tail2_1_y']
                ), axis=1)
            
            # Angle (degrees) tail middle tail2         # ADJACENT, CRAWL, GROOM
            csv_df['white_tail1_middle_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['white_tail_1_x'], 
                x['white_tail_1_y'], 
                x['white_middle_1_x'], 
                x['white_middle_1_y'], 
                x['white_tail2_1_x'], 
                x['white_tail2_1_y']
                ), axis=1)



            csv_df['black_ano_tail1_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['black_anogenital_2_x'], 
                x['black_anogenital_2_y'], 
                x['black_tail_2_x'], 
                x['black_tail_2_y'], 
                x['black_tail2_2_x'], 
                x['black_tail2_2_y']
                ), axis=1)

            csv_df['black_back_ano_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['black_back_2_x'], 
                x['black_back_2_y'], 
                x['black_anogenital_2_x'], 
                x['black_anogenital_2_y'], 
                x['black_tail2_2_x'], 
                x['black_tail2_2_y']
                ), axis=1)
            
            csv_df['black_tail1_middle_tail2_angle'] = csv_df.apply(lambda x: angle3pt(
                x['black_tail_2_x'], 
                x['black_tail_2_y'], 
                x['black_middle_2_x'], 
                x['black_middle_2_y'], 
                x['black_tail2_2_x'], 
                x['black_tail2_2_y']
                ), axis=1)

# EOF 395-419 CIRCLE = CURVE AND ANGLES --------------------------------------------------------------------------------------------------------

            # Moving averages

            # Rolling sums

# BEG 219-237 HIGH PROBABILITY BODY PARTS AND CENTROID ROLLS -----------------------------------------------------------------------------------
# feature 82-109

# white_movement_columns = white_body_part_names
# ['white_nose_1', 'white_left_eye_1', 'white_right_eye_1', 'white_head_1', 'white_back_1', 'white_pelvis_1', 
# 'white_anogenital_1', 'white_left_shoulder_1', 'white_right_shoulder_1', 'white_tail_1', 'white_middle_1', 'white_tail2_1']

# WHITE
            white_columns_x, white_columns_y, white_columns_p = [], [], []
            for bp in white_body_part_names:
                white_columns_x.append(str(bp) + '_x')
                white_columns_y.append(str(bp) + '_y')
                white_columns_p.append(str(bp) + '_p')


            print('Calculating high probably body part counts .... and centroid rolls for white')

            csv_df['white_high_probability_bp'] = csv_df.apply(lambda row: count_high_p([row[p] for p in white_columns_p]), axis=1)            
            csv_df['white_high_probability_bp_no_zero'] = csv_df['white_high_probability_bp']
            csv_df['white_high_probability_bp_no_zero'].replace(to_replace = 0, value = 1, inplace=True)


            csv_df['white_wholebody_centroid_mult_x'] = csv_df['white_wholebody_centroid_x'] * csv_df['white_high_probability_bp_no_zero']
            csv_df['white_wholebody_centroid_mult_y'] = csv_df['white_wholebody_centroid_y'] * csv_df['white_high_probability_bp_no_zero']

            csv_df['white_head_centroid_mult_x'] = csv_df['white_head_centroid_x'] * csv_df['white_high_probability_bp_no_zero']
            csv_df['white_head_centroid_mult_y'] = csv_df['white_head_centroid_y'] * csv_df['white_high_probability_bp_no_zero']

            csv_df['white_anus_centroid_mult_x'] = csv_df['white_anus_centroid_x'] * csv_df['white_high_probability_bp_no_zero']
            csv_df['white_anus_centroid_mult_y'] = csv_df['white_anus_centroid_y'] * csv_df['white_high_probability_bp_no_zero']

#           roll_rows_30 = int(30*60*fps)               # 30x60 = 1,800 (30 minutes) x 30 fps = 54,000
            rolling_rows_1_second = int(fps)           # 12 = 1 second
#           rolling_rows_12_frames = int(12)            # 12 frames (1 second)

            csv_df['white_wholebody_centroid_x_roll_mean_1_second'] = csv_df['white_wholebody_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['white_wholebody_centroid_y_roll_mean_1_second'] = csv_df['white_wholebody_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()

            csv_df['white_head_centroid_x_roll_mean_1_second'] = csv_df['white_head_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['white_head_centroid_y_roll_mean_1_second'] = csv_df['white_head_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()

            csv_df['white_anus_centroid_x_roll_mean_1_second'] = csv_df['white_anus_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['white_anus_centroid_y_roll_mean_1_second'] = csv_df['white_anus_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['white_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()

            # Calculate rolling standard deviations ?

# BLACK
            black_columns_x, black_columns_y, black_columns_p = [], [], []
            for bp in black_body_part_names:
                black_columns_x.append(str(bp) + '_x')
                black_columns_y.append(str(bp) + '_y')
                black_columns_p.append(str(bp) + '_p')

            print('Calculating high probably body part counts .... and centroid rolls for black')

            csv_df['black_high_probability_bp'] = csv_df.apply(lambda row: count_high_p([row[p] for p in black_columns_p]), axis=1)            
            csv_df['black_high_probability_bp_no_zero'] = csv_df['black_high_probability_bp']
            csv_df['black_high_probability_bp_no_zero'].replace(to_replace = 0, value = 1, inplace=True)


            csv_df['black_wholebody_centroid_mult_x'] = csv_df['black_wholebody_centroid_x'] * csv_df['black_high_probability_bp_no_zero']
            csv_df['black_wholebody_centroid_mult_y'] = csv_df['black_wholebody_centroid_y'] * csv_df['black_high_probability_bp_no_zero']

            csv_df['black_head_centroid_mult_x'] = csv_df['black_head_centroid_x'] * csv_df['black_high_probability_bp_no_zero']
            csv_df['black_head_centroid_mult_y'] = csv_df['black_head_centroid_y'] * csv_df['black_high_probability_bp_no_zero']

            csv_df['black_anus_centroid_mult_x'] = csv_df['black_anus_centroid_x'] * csv_df['black_high_probability_bp_no_zero']
            csv_df['black_anus_centroid_mult_y'] = csv_df['black_anus_centroid_y'] * csv_df['black_high_probability_bp_no_zero']

#           roll_rows_30 = int(30*60*fps)   # 30x60 = 1,800 x 30 fps = 54,000
#           roll_rows_30 = int(fps)          # 12
# SEE ABOVE

            csv_df['black_wholebody_centroid_x_roll_mean_1_second'] = csv_df['black_wholebody_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['black_wholebody_centroid_y_roll_mean_1_second'] = csv_df['black_wholebody_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()


            csv_df['black_head_centroid_x_roll_mean_1_second'] = csv_df['black_head_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['black_head_centroid_y_roll_mean_1_second'] = csv_df['black_head_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()

            csv_df['black_anus_centroid_x_roll_mean_1_second'] = csv_df['black_anus_centroid_mult_x'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()
            csv_df['black_anus_centroid_y_roll_mean_1_second'] = csv_df['black_anus_centroid_mult_y'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum() / csv_df['black_high_probability_bp_no_zero'].rolling(rolling_rows_1_second, min_periods=0, center=True).sum()

# EOF 219-237 HIGH PROBABILITY BODY PARTS AND CENTROID ROLLS -----------------------------------------------------------------------------------


            # Replace infinity with 0
            csv_df.replace([np.inf, -np.inf], 0, inplace=True)

            # Save DF
            print('Saving features for video {}...'.format(file_name))  # <-- ?
            self.data_df = csv_df
            self.data_df.columns = csv_df.columns
            self.data_df = self.data_df.fillna(0).apply(pd.to_numeric)
            
            # was: save_path = os.path.join(self.save_dir, file_name + '.' + self.file_type)
            # from piotr_120324_3-20240313-1940 !.py
            save_path = os.path.join(self.features_dir, f'{video_name}.{self.file_type}')
            self.data_df = self.data_df.reset_index(drop=True).fillna(0)
            save_df(self.data_df, self.file_type, save_path)
                
            video_timer.stop_timer()
            print('Feature extraction complete for video {} (elapsed time: {}s)'.format(file_name, video_timer.
                                                                                        elapsed_time_str))

        self.timer.stop_timer()
        stdout_success(f'Feature extraction complete for {str(len(self.files_found))} video(s). Results are saved inside the project_folder/csv/features_extracted directory'
                       , elapsed_time=self.timer.elapsed_time_str)


    # Placeholder for the method to read files
    def read_files_from_config(self):
        # Read the file paths from the config or a directory and return them as a list
        return []

# The main execution block
if __name__ == "__main__":
    extractor = UserDefinedFeatureExtractor(config_path=config_path)
    # No need to call run(), it's already called inside __init__


# 003-A_amber_feature_extraction_20230815-pp-10.0-movements !.py
