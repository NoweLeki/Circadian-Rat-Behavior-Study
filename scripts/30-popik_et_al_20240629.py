# done 20240524

# Saves the most important, to-be RO
# epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx
# file. Note that IN THIS FILE the Ns are true Ns and co-occurences are true co-occurrences, as explained later
# However, a) for the 3-D plots, some Ns should be converted to time in seconds (divided by FPS 12) so that the max Ns = 720 will be 60 s
# Why 720 is max? Because in SimBA INI file, we count every episode of nosing, sniffing etc. 
# One row = 60 s. With FPS = 12 there could be 720 (max) episodes of nosing. 

    # Produces desired plots and Excel !!! Bingo

# Reads CSVs defined in 
# circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv
# and located in
# 6_machine_results--behaviors-plus-usv-adjusted-final

# Saves 
# a) plots in
# plots_31.96 (these are matrices, 4 columns x 5 rows = 20 heatmaps)

# b) Excel as
# output_filename = f"epoch_analysis_detailed_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_31.96')}.xlsx"

# <-- this Excel file is needed for 
# 1) summary:
# 32.202-summary--sequence analysis co-occurrence-python-GT-36 Excel !.py

# and 2) 3D plots:
# 32.206-just-plot-3d-sequence analysis co-occurrence-python-GT-36.py
# 32.207-colors-just-plot-3d-sequence analysis co-occurrence-python-GT-36.py
# needed is --- filename = 'epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx'

# How it works: CSVs in
# 6_machine_results--behaviors-plus-usv-adjusted-final
# have rows (each row = 1/12 s because FPS = 12). For every EPOCH, script saves "how many times (N) the given behavior or USV was present within the EPOCH (max is 720)".
# Then it also looks for instances of co-occurrences: IF and only IF within a given time EPOCH there was behavior-A AND behavior-B ot calculates the their sum and displays as N co-occurrences
# Otherwise it fills cells as blanks = NaN

import pandas as pd
import os
from datetime import datetime, timedelta
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
EPOCH_LENGTH = 60  # seconds per epoch

# Paths
# index_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-evening-36-rows-with-audio-and-video_09.992.1.csv'
# data_files_dir = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\6_machine_results--behaviors-plus-usv-adjusted-final'
# output_dir = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\7_sequential_analysis'
index_file_path = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\usv\\usv_csvs\\circadian_1_usv_results-morning-36-rows-with-audio-and-video_09.992.1.csv'
data_files_dir = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\6_machine_results--behaviors-plus-usv-adjusted-final'
output_dir = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\7_sequential_analysis'

plot_dir = os.path.join(output_dir, 'plots_31.96')
os.makedirs(plot_dir, exist_ok=True)

# Load index DataFrame
df_index = pd.read_csv(index_file_path)
df_index['Simba_file'] = df_index['Simba_file'].astype(str)  # Ensure all entries are strings
df_index = df_index[['Simba_file', 'Updated Video Start Date', 'Updated Video Start Time', 'BOX', 'FPS']].drop_duplicates()

# Format the date and time columns to remove delimiters
df_index['Updated Video Start Date'] = df_index['Updated Video Start Date'].apply(lambda x: x.replace('-', '') if isinstance(x, str) else 'unknown_date')
df_index['Updated Video Start Time'] = df_index['Updated Video Start Time'].apply(lambda x: x.replace(':', '') if isinstance(x, str) else 'unknown_time')

behaviors = ["nosing", "following", "grooming", "anogenital sniffing", "mounting", 
             "sniffing", "crawling", "fighting", "adjacent lying", "rearing", 
             "self-grooming", "ALARM", "FLAT", "FRQ MODUL.", "SHORT",] 

behavior_pairs = list(combinations(behaviors, 2))

# flexible filename :
# output_filename = f"epoch_analysis_detailed_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_31.96')}.xlsx"  # -Ns_and_co-occ
# fixed filename :
# output_filename = f"epoch_analysis_detailed_2024-04-17_14_31_03_31.96_test.xlsx"    # -Ns_and_co-occ
output_filename = f"epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx"         # for morning, I used this filename
output_path = os.path.join(output_dir, output_filename)

epoch_details = []
individual_colorbar = True

for _, row in df_index.iterrows():
    simba_filename = row['Simba_file']
    if simba_filename == 'nan':  # Skip rows where 'Simba_file' is NaN
        continue
    fps = row['FPS']  # Use FPS from the index file
    date_str = row['Updated Video Start Date']
    time_str = row['Updated Video Start Time']
    box = row['BOX']
    filename = f"{date_str}-{time_str}-{box}"  # Create a formatted filename
    file_path = os.path.join(data_files_dir, simba_filename)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    data = pd.read_csv(file_path)
    if data.empty or not all(col in data.columns for col in behaviors):
        print(f"Required columns are missing in file: {file_path}")
        continue

    num_rows = len(data)
    duration_in_seconds = num_rows / fps
    num_epochs = int(duration_in_seconds // EPOCH_LENGTH)

    fig, axes = plt.subplots(5, 4, figsize=(20, 15))
    fig.suptitle(f'Co-occurrence Matrices for {filename}', fontsize=16)

    for epoch in range(num_epochs):
        ax = axes[epoch // 4, epoch % 4]
        start_time = epoch * EPOCH_LENGTH
        end_time = (epoch + 1) * EPOCH_LENGTH
        start_row = int(start_time * fps)
        end_row = int(min(end_time * fps, num_rows))

        behavior_counts = {behavior: data[behavior].iloc[start_row:end_row].sum() for behavior in behaviors}

        matrix = np.zeros((len(behaviors), len(behaviors)))
        for i, b1 in enumerate(behaviors):
            for j, b2 in enumerate(behaviors):
                if i != j and behavior_counts[b1] > 0 and behavior_counts[b2] > 0:
                    matrix[i, j] = behavior_counts[b1] + behavior_counts[b2]
                else:
                    matrix[i, j] = np.nan  # Use NaN for non-co-occurrences

        if not np.isnan(matrix).all():
            sns.heatmap(matrix, mask=np.triu(np.ones_like(matrix, dtype=bool)), annot=False, cmap='coolwarm', ax=ax, cbar=individual_colorbar, square=False, fmt=".0f")            
            ax.grid(True, linestyle='--', linewidth=0.5, color='grey')
            tick_positions = np.arange(0.5, len(behaviors))
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(behaviors, rotation=45, horizontalalignment='right', fontsize=8)
            ax.set_yticks(tick_positions)
            ax.set_yticklabels(behaviors, rotation=0, horizontalalignment='right', fontsize=8)
            ax.set_title(f'Epoch {start_time // 60}-{end_time // 60} min', fontsize=10)
        else:
            ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, color='red', fontsize=16)
            ax.set_xticks([])
            ax.set_yticks([])

        # Excel data preparation and appending
        excel_row = {
            "Filename": filename,
            "Epoch Number": epoch + 1,
            "Start Date": row['Updated Video Start Date'],  # Added Start Date
            "End Date": row['Updated Video Start Date'],  # Added End Date, assuming the same as Start Date
            "Start Time (HH:MM:SS)": (datetime.strptime(date_str + " " + time_str, "%Y%m%d %H%M%S") + timedelta(seconds=start_time)).strftime("%H:%M:%S"),
            "End Time (HH:MM:SS)": (datetime.strptime(date_str + " " + time_str, "%Y%m%d %H%M%S") + timedelta(seconds=end_time)).strftime("%H:%M:%S"),
            "BOX": row['BOX'],  # Added BOX
            "Start Time (s)": start_time,
            "End Time (s)": end_time,
            "Start Time (min)": start_time/60,
            "End Time (min)": end_time/60
        }

        for b in behaviors:
            excel_row[f"N_{b}"] = behavior_counts.get(b, 0)
        for (b1, b2) in behavior_pairs:
            co_occ_key = f"Co_occurrence_{b1}_{b2}"
            b1_count = behavior_counts.get(b1, 0)
            b2_count = behavior_counts.get(b2, 0)
            if b1_count > 0 and b2_count > 0:
                co_occ_value = b1_count + b2_count
                excel_row[co_occ_key] = co_occ_value
            else:
                excel_row[co_occ_key] = ""  # Leave cell blank if either count is zero

        epoch_details.append(excel_row)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(plot_dir, f"{filename}_co-occurrence.png"))
    plt.close()

# Save details to Excel
epoch_details_df = pd.DataFrame(epoch_details)
epoch_details_df.to_excel(output_path, index=False)
print(f"Excel file and plots are created in: {output_dir}")

# 31.96-sequence analysis co-occurrence-python-saves PLOTS and (to be read only) EXCEL-GT-36 !.py
