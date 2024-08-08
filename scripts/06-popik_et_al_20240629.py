import os
import pandas as pd

# Directories
# source_dir = r'D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\fe-0-simon-polygons-ver-2'
# append_dir = r'D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\fe-7-piotr-amber-109-feats'
# output_dir = r'D:\LEWIATAN\simb_circ_train_12bp\project_folder\csv\fe-8-fe-0-simon-polygons-ver-2-plus-piotr-amber-109-feats'

# source_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\fe-polygons'
# append_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\fe-piotr-amber-109-feats'
# output_dir = r'D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\fe-8-fe-0-simon-polygons-plus-piotr-amber-109-feats'

source_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\fe-polygons'
append_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\fe-piotr-amber-109-feats'
output_dir = r'D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\fe-8-fe-0-simon-polygons-plus-piotr-amber-109-feats'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the CSV files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.csv'):
        source_path = os.path.join(source_dir, filename)
        append_path = os.path.join(append_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if the corresponding file exists in the append directory
        if os.path.exists(append_path):
            # Load CSVs
            source_df = pd.read_csv(source_path)
            append_df = pd.read_csv(append_path)

            # Check row counts and adjust if necessary
            if len(source_df) != len(append_df):
                min_len = min(len(source_df), len(append_df))
                source_df = source_df.head(min_len)
                append_df = append_df.head(min_len)
                print(f"Row count mismatch in {filename}. Adjusted to {min_len} rows.")
            else:
                print(f"Row count matches in {filename}.")

            # Append columns from append_df to source_df
            merged_df = pd.concat([source_df, append_df], axis=1)

            # Save the merged DataFrame
            merged_df.to_csv(output_path, index=False, float_format='%.32f')  # Save as 32-bit CSV
            print(f"Merged file saved: {output_path}")
        else:
            print(f"No corresponding file found for {filename} in {append_dir}")

# 006-merge-simon-polygons-with-piotr-amber-109-feats.py
