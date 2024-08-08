# remember to UN-COMMENT a given set of two behaviors, a behavior and USV type or two types of USVs.  
# only one pair can be plotted at the time ! 

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# File paths
data_path = 'D:\\LEWIATAN\\simb_circ_1_test_evening_12bp_all_33\\project_folder\\csv\\7_sequential_analysis\\'
filename = 'epoch_analysis_detailed_2024-04-17_14_31_03_31.96.xlsx'
summary_filename = filename.replace('.xlsx', '_summary_modified.xlsx')
plots_path = os.path.join(data_path, 'plots')
os.makedirs(plots_path, exist_ok=True)

# Load the summary data
df = pd.read_excel(os.path.join(data_path, summary_filename))

# Print all columns in the dataframe for debugging
print("All columns in the dataframe:")
print(df.columns.tolist())

# Define the categories and phases
# day_categories = ['Days_1_3', 'Days_4_6'] # 20240603
day_categories = ['Days_4_6', 'Days_1_3']
time_phases = ['Light', 'Dark']

"""# Define the major keyword and the order of subcategories
major_keyword = 'FLAT'
subcategories_order = [
    "ALARM", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying", "anogenital sniffing",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'ALARM'
subcategories_order = [
    "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying", "anogenital sniffing",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'FRQ MODUL.'
subcategories_order = [
    "ALARM", "FLAT", "SHORT", "DUMMY", "adjacent lying", "anogenital sniffing",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'SHORT'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "DUMMY", "adjacent lying", "anogenital sniffing",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'adjacent lying'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "anogenital sniffing",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'anogenital sniffing'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "crawling", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'crawling'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "fighting", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'fighting'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "following", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'following'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "grooming", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'grooming'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "nosing", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'nosing'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "grooming", "mounting",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'mounting'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "grooming", "nosing",
    "rearing", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'rearing'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "grooming", "nosing",
    "mounting", "self-grooming", "sniffing"
]"""

# done

"""# Define the major keyword and the order of subcategories
major_keyword = 'self-grooming'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "grooming", "nosing",
    "mounting", "rearing", "sniffing"
]"""

# done

# Define the major keyword and the order of subcategories
major_keyword = 'sniffing'
subcategories_order = [
    "ALARM", "FLAT", "FRQ MODUL.", "SHORT", "DUMMY", "adjacent lying",
    "anogenital sniffing", "crawling", "fighting", "following", "grooming", "nosing",
    "mounting", "rearing", "self-grooming"
]

# done

# Construct the column names dynamically
columns_to_plot = []
for subcategory in subcategories_order:
    if subcategory == "DUMMY":
        columns_to_plot.append("DUMMY")
    else:
        column_name_1 = f"Co_occurrence_{subcategory}_{major_keyword} sum"
        column_name_2 = f"Co_occurrence_{major_keyword}_{subcategory} sum"
        if column_name_1 in df.columns:
            columns_to_plot.append(column_name_1)
        if column_name_2 in df.columns:
            columns_to_plot.append(column_name_2)

# Print the relevant columns
print("Relevant columns:")
for col in columns_to_plot:
    print(col)

"""
Determine the global minimum and maximum values
"""
global_min = float('inf')
global_max = float('-inf')

for column in columns_to_plot:
    if column != "DUMMY":
        col_min = df[column].min()
        col_max = df[column].max()
        print(f'{column}: min={col_min}, max={col_max}')
        global_min = min(global_min, col_min)
        global_max = max(global_max, col_max)

print(f'Global min value: {global_min}')
print(f'Global max value: {global_max}')

# Function to create heatmap for a specific column
def save_heatmap(data, column, filename):
    fig, axs = plt.subplots(2, 2, figsize=(5, 5))
    
    if column != "DUMMY":
        # Extract the subcategory and major keyword for the title
        if 'Co_occurrence_' in column:
            title_parts = column.replace('Co_occurrence_', '').replace(' sum', '').split('_')
            if len(title_parts) == 2:
                title = f"{title_parts[1]} {title_parts[0]}"
            else:
                title = column  # Fallback if the expected format is not found
        else:
            title = column

        fig.suptitle(title, fontsize=16, y=0.9)  # Adjust y to move the title down
        """
        Use global min and max for normalization
        """
        norm = plt.Normalize(global_min, global_max)  # Use global min and max for normalization
        
        # Function to create heatmap for a specific subset of data
        def plot_heatmap(subset_data, ax):
            pivot_table = subset_data.pivot_table(index="Day", columns="Phase", values=column, aggfunc='sum')
            sns.heatmap(pivot_table, ax=ax, annot=True, cmap='coolwarm', cbar=False, norm=norm, fmt='.0f', annot_kws={'size': 16})
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel('')
            ax.set_ylabel('')

        # Create a new DataFrame to extract 'Day' and 'Phase' for the heatmaps
        heatmap_data = data[['Day Category', 'Time Phase', column]]
        heatmap_data.columns = ['Day', 'Phase', column]

        # Plot each heatmap
        for i, day_category in enumerate(day_categories):
            for j, time_phase in enumerate(time_phases):
                subset_data = heatmap_data[(heatmap_data['Day'] == day_category) & (heatmap_data['Phase'] == time_phase)]
                plot_heatmap(subset_data, axs[i, j])

        # Set global Y axis label
        fig.text(0.5, 0.01, 'Phase', ha='center', fontsize=16)
        fig.text(0.25, 0.03, 'Light', ha='center', fontsize=16)
        fig.text(0.75, 0.03, 'Dark', ha='center', fontsize=16)

        # Set global X axis label
        fig.text(0.01, 0.5, 'Days', va='center', rotation='vertical', fontsize=16)
        fig.text(0.03, 0.3, '1-3', va='center', rotation='vertical', fontsize=16)
        fig.text(0.03, 0.7, '4-6', va='center', rotation='vertical', fontsize=16)
    else:
        # Plot the dummy plot
        for i in range(2):
            for j in range(2):
                axs[i, j].axis('off')
                axs[i, j].set_facecolor("white")

    # Adjust layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)  # Adjust top to make space for title
    plt.tight_layout(rect=[0.1, 0.1, 0.9, 0.9])

    # Save the plot
    plt.savefig(filename)
    plt.close()

# Save each heatmap
for idx, column in enumerate(columns_to_plot):
    plot_filename = os.path.join(plots_path, f'plot_{idx + 1}.png')
    save_heatmap(df, column, plot_filename)

# Print the order of columns used for plots
print("Order of columns used for plots:")
for column in columns_to_plot:
    print(column)

# Load the images
plot_files = [os.path.join(plots_path, f'plot_{i}.png') for i in range(1, len(columns_to_plot) + 1)]
images = [Image.open(plot_file) for plot_file in plot_files]

# Define the size of the contact sheet
contact_sheet_width = 5 * images[0].width
contact_sheet_height = 3 * images[0].height

# Create a blank contact sheet
contact_sheet = Image.new("RGB", (contact_sheet_width, contact_sheet_height), "white")

# Paste each image into the contact sheet
for idx, img in enumerate(images):
    x = (idx % 5) * img.width
    y = (idx // 5) * img.height
    contact_sheet.paste(img, (x, y))

# Save the contact sheet
contact_sheet_filename = os.path.join(data_path, f'heatmap_co_occurrence_{major_keyword}_contact_sheet_32.208.png')
contact_sheet.save(contact_sheet_filename)
print(f'Contact sheet saved as: {contact_sheet_filename}')

# 32.208-PLOTS-co-occurrences-heatmaps-evening-python-GT-36 Excel !-AGGREGATE-contact sheet-NORMALIZED.py
