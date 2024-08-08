# done 20240525

# Calculates AGGREGATE Excel with only 4 rows:

# Day Category	Time Phase

# Days_1_3	Dark (not Light)
# Days_1_3	Light Dark (not Dark)
# Days_4_6	Dark (not Light)
# Days_4_6	Light Dark (not Dark)

# This Excel is necessary for Co-occurence heatmap plots (32.208 [not 207])

import pandas as pd
import os

# File paths
# data_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\'
data_path = 'D:\\LEWIATAN\\simb_circ_1_test_morning_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\'
filename = 'epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx'
summary_filename = filename.replace('.xlsx', '_summary_modified.xlsx')


# Load data
df = pd.read_excel(os.path.join(data_path, filename), sheet_name='Sheet1')
df['Start Date'] = df['Start Date'].astype(str)

# Calculate the observation 'Day' for each record based on the earliest date observed for each box
df['Day'] = df.groupby('BOX')['Start Date'].transform(lambda x: (pd.to_datetime(x) - pd.to_datetime(x).min()).dt.days + 1)

# Debugging output to check 'Day' column
print(df.columns)  # Check column names
print(df['Day'].head())  # Check first few entries in 'Day' column

# Define day categories
df['Day Category'] = pd.cut(df['Day'], bins=[0, 3, 6], labels=['Days_1_3', 'Days_4_6'], right=True)

# Define time phases
# df['Time Phase'] = pd.cut(df['End Time (min)'], bins=[0, 10, 20], labels=['Light', 'Dark'], right=True)
df['Time Phase'] = pd.cut(df['End Time (min)'], bins=[0, 10, 20], labels=['Dark', 'Light'], right=True) # morning 20240525

# Define a function to calculate SEM (Standard Error of the Mean)
def calculate_sem(series):
    return series.sem()

# Group data by new categories
grouped = df.groupby(['Day Category', 'Time Phase'])

# Define all columns to be included
column_names = [
    "N_nosing", 
    "N_following", "N_grooming", "N_anogenital sniffing", "N_mounting",
    "N_sniffing", "N_crawling", "N_fighting", "N_adjacent lying", "N_rearing",
    "N_self-grooming", "N_ALARM", "N_FLAT", "N_FRQ MODUL.", "N_SHORT",
    "Co_occurrence_nosing_following", "Co_occurrence_nosing_grooming", "Co_occurrence_nosing_anogenital sniffing", 
    "Co_occurrence_nosing_mounting", "Co_occurrence_nosing_sniffing", "Co_occurrence_nosing_crawling", 
    "Co_occurrence_nosing_fighting", "Co_occurrence_nosing_adjacent lying", "Co_occurrence_nosing_rearing", 
    "Co_occurrence_nosing_self-grooming", "Co_occurrence_nosing_ALARM", "Co_occurrence_nosing_FLAT", 
    "Co_occurrence_nosing_FRQ MODUL.", "Co_occurrence_nosing_SHORT", "Co_occurrence_following_grooming", 
    "Co_occurrence_following_anogenital sniffing", "Co_occurrence_following_mounting", "Co_occurrence_following_sniffing", 
    "Co_occurrence_following_crawling", "Co_occurrence_following_fighting", "Co_occurrence_following_adjacent lying", 
    "Co_occurrence_following_rearing", "Co_occurrence_following_self-grooming", "Co_occurrence_following_ALARM", 
    "Co_occurrence_following_FLAT", "Co_occurrence_following_FRQ MODUL.", "Co_occurrence_following_SHORT", 
    "Co_occurrence_grooming_anogenital sniffing", "Co_occurrence_grooming_mounting", "Co_occurrence_grooming_sniffing", 
    "Co_occurrence_grooming_crawling", "Co_occurrence_grooming_fighting", "Co_occurrence_grooming_adjacent lying", 
    "Co_occurrence_grooming_rearing", "Co_occurrence_grooming_self-grooming", "Co_occurrence_grooming_ALARM", 
    "Co_occurrence_grooming_FLAT", "Co_occurrence_grooming_FRQ MODUL.", "Co_occurrence_grooming_SHORT", 
    "Co_occurrence_anogenital sniffing_mounting", "Co_occurrence_anogenital sniffing_sniffing", "Co_occurrence_anogenital sniffing_crawling", 
    "Co_occurrence_anogenital sniffing_fighting", "Co_occurrence_anogenital sniffing_adjacent lying", "Co_occurrence_anogenital sniffing_rearing", 
    "Co_occurrence_anogenital sniffing_self-grooming", "Co_occurrence_anogenital sniffing_ALARM", "Co_occurrence_anogenital sniffing_FLAT", 
    "Co_occurrence_anogenital sniffing_FRQ MODUL.", "Co_occurrence_anogenital sniffing_SHORT", "Co_occurrence_mounting_sniffing", 
    "Co_occurrence_mounting_crawling", "Co_occurrence_mounting_fighting", "Co_occurrence_mounting_adjacent lying", 
    "Co_occurrence_mounting_rearing", "Co_occurrence_mounting_self-grooming", "Co_occurrence_mounting_ALARM", 
    "Co_occurrence_mounting_FLAT", "Co_occurrence_mounting_FRQ MODUL.", "Co_occurrence_mounting_SHORT", 
    "Co_occurrence_sniffing_crawling", "Co_occurrence_sniffing_fighting", "Co_occurrence_sniffing_adjacent lying", 
    "Co_occurrence_sniffing_rearing", "Co_occurrence_sniffing_self-grooming", "Co_occurrence_sniffing_ALARM", 
    "Co_occurrence_sniffing_FLAT", "Co_occurrence_sniffing_FRQ MODUL.", "Co_occurrence_sniffing_SHORT", 
    "Co_occurrence_crawling_fighting", "Co_occurrence_crawling_adjacent lying", "Co_occurrence_crawling_rearing", 
    "Co_occurrence_crawling_self-grooming", "Co_occurrence_crawling_ALARM", "Co_occurrence_crawling_FLAT", 
    "Co_occurrence_crawling_FRQ MODUL.", "Co_occurrence_crawling_SHORT", "Co_occurrence_fighting_adjacent lying", 
    "Co_occurrence_fighting_rearing", "Co_occurrence_fighting_self-grooming", "Co_occurrence_fighting_ALARM", 
    "Co_occurrence_fighting_FLAT", "Co_occurrence_fighting_FRQ MODUL.", "Co_occurrence_fighting_SHORT", 
    "Co_occurrence_adjacent lying_rearing", "Co_occurrence_adjacent lying_self-grooming", "Co_occurrence_adjacent lying_ALARM", 
    "Co_occurrence_adjacent lying_FLAT", "Co_occurrence_adjacent lying_FRQ MODUL.", "Co_occurrence_adjacent lying_SHORT", 
    "Co_occurrence_rearing_self-grooming", "Co_occurrence_rearing_ALARM", "Co_occurrence_rearing_FLAT", 
    "Co_occurrence_rearing_FRQ MODUL.", "Co_occurrence_rearing_SHORT", "Co_occurrence_self-grooming_ALARM", 
    "Co_occurrence_self-grooming_FLAT", "Co_occurrence_self-grooming_FRQ MODUL.", "Co_occurrence_self-grooming_SHORT", 
    "Co_occurrence_ALARM_FLAT", "Co_occurrence_ALARM_FRQ MODUL.", "Co_occurrence_ALARM_SHORT", "Co_occurrence_FLAT_FRQ MODUL.", 
    "Co_occurrence_FLAT_SHORT", "Co_occurrence_FRQ MODUL._SHORT"
]

# Prepare the summary DataFrame with required statistics for all specified columns
agg_dict = {column_name: ['mean', calculate_sem, 'count', 'sum'] for column_name in column_names}
summary_stats = grouped.agg(agg_dict).reset_index()

# Flatten the MultiIndex in columns
summary_stats.columns = [' '.join(col).strip() if col[1] else col[0] for col in summary_stats.columns.values]

# Get unique boxes and dates for each day category
boxes_per_day = df.groupby('Day Category')['BOX'].apply(lambda x: ' '.join(sorted(set(x)))).reset_index(name='Boxes')
dates_per_day = df.groupby('Day Category')['Start Date'].apply(lambda x: ' '.join(sorted(set(x)))).reset_index(name='Dates')

# Merge the unique boxes and dates with the summary stats
summary_data = pd.merge(summary_stats, boxes_per_day, on='Day Category', how='left')
summary_data = pd.merge(summary_data, dates_per_day, on='Day Category', how='left')

# Specify the column order, including new columns
order = ['Day Category', 'Time Phase', 'Boxes', 'Dates'] + \
        [f'{column_name} {stat}' for column_name in column_names for stat in ['mean', 'calculate_sem', 'count', 'sum']]

# Reorder columns as specified
summary_data = summary_data[order]

# Save the summary DataFrame to an Excel file
summary_data.to_excel(os.path.join(data_path, summary_filename), index=False)

print(f"Summary Excel file created: {summary_filename}")

# 32.203-EXCEL-co-occurrence-cols-SAVES-summary-morning-occurrence-python-GT-36 Excel !-AGGREGATE.py
