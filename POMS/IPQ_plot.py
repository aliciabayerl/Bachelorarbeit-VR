import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'IPQ_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)

# Compute overall presence
ipq_scores['Overall_Presence'] = ipq_scores[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

# Group by condition and calculate means
condition_means = ipq_scores.groupby('Condition')[['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']].mean().reset_index()

# Rename the columns for clarity in the plot
condition_means = condition_means.rename(columns={
    'SP_mean': 'Spatial Presence',
    'INV_mean': 'Involvement',
    'REAL_mean': 'Realism',
    'Overall_Presence': 'Overall Presence'
})

# Plot settings
plt.figure(figsize=(6, 4))  # Adjust figure size to be smaller
plt.rc('axes', labelsize=10)  # Fontsize of the x and y labels
plt.rc('xtick', labelsize=9)  # Fontsize of the x tick labels
plt.rc('ytick', labelsize=9)  # Fontsize of the y tick labels
plt.rc('legend', fontsize=9)  # Fontsize of the legend
plt.rc('font', family='sans-serif')  # Use a sans-serif font
plt.rc('font', **{'sans-serif': 'Arial'})  # Specifically use Arial

# Define colors
palette_colors = ["#abd9e9", "#74add1", "#4575b4", "#800080"]

# Define bar positions and heights
bar_width = 0.2
positions = [condition_means['Condition'] + i * bar_width for i in range(len(condition_means.columns) - 1)]
heights = [condition_means[col] for col in condition_means.columns[1:]]

# Plot bars
for i, (pos, height, color) in enumerate(zip(positions, heights, palette_colors)):
    plt.bar(pos, height, bar_width, label=condition_means.columns[i + 1], color=color)

# Customize plot
plt.xlabel('Condition')
plt.ylabel('Mean Score')
plt.axhline(0, color='black', linewidth=0.8)
plt.xticks(condition_means['Condition'] + bar_width * 1.5, condition_means['Condition'])
plt.legend(title='', loc = 'lower right')

# Save and display the plot
image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'IPQ_PresencePlot.png')
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.show()
