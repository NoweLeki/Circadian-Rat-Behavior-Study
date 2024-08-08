# done 20240524

import pandas as pd

# File paths
# data_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\'
data_path = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\'

filename = 'epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx'
output_filename = 'epoch_analysis_detailed_2024-04-17_14_31_03_31.96_by_days.xlsx'

# Load the data
df = pd.read_excel(data_path + filename)

# Function to calculate 'Day' based on 'Start Date' and 'BOX'
def calculate_days(group):
    # Find unique start dates and map them to day numbers
    unique_dates = sorted(group['Start Date'].unique())
    day_map = {date: idx + 1 for idx, date in enumerate(unique_dates)}
    # Apply map to 'Start Date'
    group['Day'] = group['Start Date'].map(day_map)
    return group

# Apply the function to each 'BOX' group
# Note: include_groups=False to handle the deprecation warning
grouped = df.groupby('BOX', group_keys=False).apply(calculate_days)

# Move 'Day' column to the first position
cols = grouped.columns.tolist()
cols = cols[-1:] + cols[:-1]  # This moves the last column (Day) to the first position
grouped = grouped[cols]

# Save the updated DataFrame to a new Excel file
grouped.to_excel(data_path + output_filename, index=False)

print(f"Updated file saved as {output_filename}")

# 32.300-add Day column to _epoch_analysis_detailed_ -python-GT-36 Excel !.py
