import os
import pandas as pd

# Define the folders
# targets_inserted_folder = r"D:\LEWIATAN\-\targets_inserted\7 - just 01 (copy sh9_plus3_outliers just 01) 20231110"
# features_extracted_folder = r"D:\LEWIATAN\-\features_extracted"
# destination_folder = r"D:\LEWIATAN\-\targets_inserted"

targets_inserted_folder = r"D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\targets_inserted\7 - just 01 (copy sh9_plus3_outliers just 01) 20231110"
features_extracted_folder = r"D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\fe-8-fe-0-simon-polygons-ver-2-plus-piotr-amber-109-feats"
destination_folder = r"D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\targets_inserted\ti-8-fe-0-simon-polygons-ver-2-plus-piotr-amber-109-feats"

# Loop over the files in the source folder that end with "-just-01.csv"
for targets_inserted_file in os.listdir(targets_inserted_folder):
    if targets_inserted_file.endswith("-just-01.csv"):
        # Construct the full path to the source file
        targets_inserted_file_path = os.path.join(targets_inserted_folder, targets_inserted_file)
        
        # Remove "-just-01" from the filename to match with the corresponding file in the features folder
        feature_file_name = targets_inserted_file.replace("-just-01", "")
        feature_file_path = os.path.join(features_extracted_folder, feature_file_name)

        # Check if the corresponding file exists in the features folder
        if os.path.exists(feature_file_path):
            # Read the CSV files into DataFrames
            target_df = pd.read_csv(targets_inserted_file_path)
            feature_df = pd.read_csv(feature_file_path)

            # Check if the number of rows matches
            min_length = min(len(target_df), len(feature_df))
            if len(target_df) != len(feature_df):
                print(f"Row mismatch detected. Trimming to {min_length} rows for: {targets_inserted_file}")

            # Trim DataFrames to the minimum length
            target_df = target_df.head(min_length)
            feature_df = feature_df.head(min_length)

            # Add columns 2-12 from the target DataFrame to the features DataFrame
            combined_df = pd.concat([feature_df, target_df.iloc[:, 1:12]], axis=1)

            # Save the modified file in the destination folder
            destination_file_path = os.path.join(destination_folder, feature_file_name)
            combined_df.to_csv(destination_file_path, index=False)
            print(f"Combined file saved as: {destination_file_path}")
        else:
            print(f"Corresponding feature file not found for: {targets_inserted_file}")

print("Processing completed.")

# 007-1 simba_read_features_extracted__add_01_from_targets_inserted !.py
