# Read the CSV file containing the thresholds, precision, and recall
# Plot Precision and Recall against Discrimination Thresholds

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Define the directory where CSV files are located
# directory = r"D:\LEWIATAN\simb_circ_train_12bp\models\all-rows\validations"
directory = r"D:\LEWIATAN\simb_circ_train_12bp\models\all-rows-simon-polygons-plus-piotr-amber-109-feats\validations\summary precision curves"

csv_files = glob.glob(os.path.join(directory, '*_pr_curve.csv'))

# Prepare a list to store summary data
summary = []

# Process each file
for file_path in csv_files:
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Calculate F1 scores
    data['F1'] = 2 * (data['PRECISION'] * data['RECALL']) / (data['PRECISION'] + data['RECALL'])

    # Find the threshold corresponding to the maximum F1 score
    max_f1_threshold = data.loc[data['F1'].idxmax(), 'DISCRIMINATION THRESHOLDS']
    max_f1_value = data['F1'].max()

    # Append the results to the summary list
    summary.append([os.path.basename(file_path), max_f1_value, max_f1_threshold])

    # Plot Precision, Recall, and F1 against Discrimination Thresholds and save the plot as PNG
    plt.figure(figsize=(10,6))
    plt.plot(data['DISCRIMINATION THRESHOLDS'], data['PRECISION'], label='Precision', marker='o')
    plt.plot(data['DISCRIMINATION THRESHOLDS'], data['RECALL'], label='Recall', marker='x')
    plt.plot(data['DISCRIMINATION THRESHOLDS'], data['F1'], label='F1', marker='^')
    plt.axvline(x=0.5, color='gray', linestyle='--', linewidth=2, label='Threshold = 0.5')
    plt.axvline(x=max_f1_threshold, color='red', linestyle='--', linewidth=2, label=f'Max F1 ({max_f1_value:.2f}) at {max_f1_threshold}')
    plt.xlabel('Discrimination Thresholds')
    plt.ylabel('Metrics')
    plt.title('Precision, Recall, and F1 for Different Discrimination Thresholds')
    plt.legend()
    plt.grid(True)
    
    # Save the figure
    plt.savefig(os.path.join(directory, os.path.basename(file_path).replace('.csv', '.png')))
    plt.close()

# Save the summary data to a CSV file
summary_df = pd.DataFrame(summary, columns=['file_name', 'max F1', 'corresponding DISCRIMINATION THRESHOLD'])
summary_df.to_csv(os.path.join(directory, 'summary_precision_curves.csv'), index=False)

# analyze_precision_curves_all !.py
