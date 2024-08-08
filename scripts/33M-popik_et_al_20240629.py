# done 20240525

# Creates co-occurence and N_ 3D plots 
# as _32.215-2.png
# in
# D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\8_sequential_analysis_for_statistics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, proj3d
import os
import re
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, viridis
from matplotlib.colors import LinearSegmentedColormap

# Custom gradient color maps
# 20240524 replace sequence of lines
dark_cmap = LinearSegmentedColormap.from_list("dark", ["#ffffd9", "#ff7f0e"])    # Yellow to orange
light_cmap = LinearSegmentedColormap.from_list("light", ["#1f77b4", "#08306b"])  # Blue to dark blue

# data_path = r"D:\LEWIATAN\simb_circ_1_test_evening_12bp_all_33\project_folder\csv\8_sequential_analysis_for_statistics"
data_path = r"D:\LEWIATAN\simb_circ_1_test_morning_12bp_all_33\project_folder\csv\8_sequential_analysis_for_statistics"

def create_label(filename):
    base = filename.replace('.csv', '').replace('_', ' ')
    if filename.startswith("N_"):
        activity = " ".join(base[2:].split()).lower()  # Normalize the case
        return f"Mean {activity.capitalize()}"
    else:
        if "Co occurrence" in base:
            parts = base.lower().split(' ')[2:]  # Normalize and split
            combined_activities = []
            skip_next = False
            for i in range(len(parts)):
                if skip_next:
                    skip_next = False
                    continue
                if i + 1 < len(parts) and ' '.join([parts[i], parts[i+1]]) in ['anogenital sniffing', 'self grooming', 'frq modul.', 'short call']:
                    combined_activities.append(' '.join([parts[i], parts[i+1]]))
                    skip_next = True
                else:
                    combined_activities.append(parts[i])
            activities = ' and '.join(combined_activities)
            return f"Mean Co-occurrence of {activities}"
        return f"Mean {base.lower().capitalize()}"

for filename in os.listdir(data_path):
    if filename.endswith(".csv"):
        full_path = os.path.join(data_path, filename)
        df = pd.read_csv(full_path)
        df = df.drop(columns=['Filename'], errors='ignore')

        # Aggregate duplicate days by taking the mean of the observations
        df = df.groupby('Day').mean().reset_index()

        # Reindex DataFrame to include all days in the range with missing days filled with 0
        min_day = df['Day'].min()
        max_day = df['Day'].max()
        all_days = np.arange(min_day, max_day + 1)
        df = df.set_index('Day').reindex(all_days).fillna(0).reset_index()

        # Extract and reshape the data for 3D plotting
        epoch_data = df.filter(regex='^Epoch_\\d+$').stack().reset_index()
        epoch_data.columns = ['index', 'Epoch', 'Value']
        epoch_data['Day'] = df['Day'].iloc[epoch_data['index']].values
        epoch_data['Epoch'] = epoch_data['Epoch'].str.extract(r'(\d+)', expand=False).astype(int)
        epoch_data = epoch_data.dropna(subset=['Value'])
        X, Y = np.meshgrid(sorted(epoch_data['Day'].unique()), sorted(epoch_data['Epoch'].unique()))
        Z = epoch_data.pivot_table(index='Epoch', columns='Day', values='Value', fill_value=0).values

        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Apply normalization and colormap based on epoch values
        # 2024024 change norm_light->norm_dark to norm_dark->norm_light
        norm_dark = Normalize(vmin=np.min(Z[Y<=9]), vmax=np.max(Z[Y<=9])) if np.any(Y<=9) else None
        norm_light = Normalize(vmin=np.min(Z[Y>9]), vmax=np.max(Z[Y>9])) if np.any(Y>9) else None
        colors = np.zeros((Y.shape[0], Y.shape[1], 4))  # Initialize with transparent colors

        for i in range(Y.shape[0]):
            for j in range(Y.shape[1]):
                if Y[i, j] <= 9 and norm_light:
                    colors[i, j] = light_cmap(norm_light(Z[i, j]))
                elif Y[i, j] > 9 and norm_dark:
                    colors[i, j] = dark_cmap(norm_dark(Z[i, j]))

        # Plot the surface with color mapping
        ax.plot_surface(X, Y, Z, facecolors=colors, edgecolor='black', linewidth=0.5, linestyle='dotted')

        # Set the Z-axis to start at 0 and ensure there is always a positive upper limit
        ax.set_zlim(0, max(np.max(Z), 0.1))  # Use at least 0.1 as the upper limit if data max is not greater



        ax.set_yticks(range(2, 21, 2))
        ax.set_xlabel('Day')
        ax.set_ylabel('Epoch Number')
        ax.set_zlabel(create_label(filename))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.1f'))


        # -------
        # Inside plotting loop after setting labels
        # Manipulate tick parameters and viewing angle

        # Adjust tick parameters
        # ax.tick_params(axis='x', pad=10)  # Pad the ticks on the X-axis for better visibility
        # ax.tick_params(axis='y', pad=10)  # Pad the ticks on the Y-axis

        # Set the viewing angle (elev: up/down, azim: left/right)
        # ax.view_init(elev=90, azim=-45)

        # Rotate the labels for better visibility and to avoid overlap
        # for label in ax.xaxis.get_ticklabels():
        #    label.set_rotation(60)  # Rotate X axis labels for better visibility
        # ax.yaxis.labelpad = 20  # Add some padding to the y-axis label for clarity
        ax.zaxis.labelpad = 10  # Add some padding to the z-axis label if needed
        # -------


        # Generate and save the plot
        plot_filename = filename.replace('.csv', '_32.215-2.png')
        # 
        plt.savefig(os.path.join(data_path, plot_filename), format='png', dpi=300)
        plt.close()

# 32.215-DARKER-morning-co-occ-several-based on CSV - just-plot-3d-sequence analysis co-occurrence-python-GT-36.py
        