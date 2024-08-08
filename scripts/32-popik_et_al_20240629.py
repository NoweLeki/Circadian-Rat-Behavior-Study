# done 20240524

import pandas as pd
import numpy as np
import os

# Define paths and filenames
# input_file = r"D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\epoch_analysis_detailed_2024-04-17_14_31_03_31.96_by_days.xlsx"
# output_folder = r"D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\8_sequential_analysis_for_statistics"
input_file = r"D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\epoch_analysis_detailed_2024-04-17_14_31_03_31.96_by_days.xlsx"
output_folder = r"D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\8_sequential_analysis_for_statistics"

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the data from the Excel file
df = pd.read_excel(input_file, sheet_name='Sheet1')

# Define behavior columns
behaviors = [
    "N_nosing", "N_following", "N_grooming", "N_anogenital sniffing",
    "N_mounting", "N_sniffing", "N_crawling", "N_fighting", 
    "N_adjacent lying", "N_rearing", "N_self-grooming", "N_ALARM", 
    "N_FLAT", "N_FRQ MODUL.", "N_SHORT"
]

# Define co-occurrence columns
co_occurrences = [col for col in df.columns if 'Co_occurrence_' in col]

# Combine all columns to iterate over
all_columns = behaviors + co_occurrences

# Process each column
for column in all_columns:
    # Pivot the table with 'Day' and 'Filename' as indices
    pivot_df = df.pivot(index=['Day', 'Filename'], columns='Epoch Number', values=column)
    pivot_df.columns = [f"Epoch_{i}" for i in range(1, len(pivot_df.columns) + 1)]

    # Decide on fill value based on column type
    if column in behaviors:
        fill_value = 0
    else:  # Co-occurrence columns
        fill_value = np.nan  # Use numpy to define NaN

    # Replace missing values with the chosen fill value
    pivot_df.fillna(fill_value, inplace=True)

    # Define the output filename based on the column
    if column in behaviors:
        behavior_name = column.replace("N_", "N_")
        output_filename = f"{behavior_name}.csv"
    else:
        output_filename = f"{column}.csv"

    # Output file path
    output_file = os.path.join(output_folder, output_filename)
    # Save to CSV
    pivot_df.to_csv(output_file)

# 35.104-transpose columns for ANOVA WITH DAYS (!).py
