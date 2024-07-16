import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Define folder paths and file names
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
output_image_path = os.path.join(folder_path, 'Plot_Images')

# Load the data
data = pd.read_csv(file_path)

# Define mood states and calculate changes
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Summary statistics for significance
summary_stats = {
    'Anger': {'p-value': 0.033, 'r-value': 0.789},
    'Disgust': {'p-value': 0.001, 'r-value': 0.689},
    'Fear': {'p-value': 0.628, 'r-value': 0.727},
    'Anxiety': {'p-value': 0.021, 'r-value': 0.599},
    'Sadness': {'p-value': 0.043, 'r-value': 0.699},
    'Desire': {'p-value': 0.188, 'r-value': 0.545},
    'Relaxation': {'p-value': 0.413, 'r-value': 0.329},
    'Happiness': {'p-value': 0.041, 'r-value': 0.372}
}

# Plotting
plt.figure(figsize=(6, 4))  # Adjust figure size to be smaller
plt.rc('axes', labelsize=10)  # Fontsize of the x and y labels
plt.rc('xtick', labelsize=9)  # Fontsize of the x tick labels
plt.rc('ytick', labelsize=9)  # Fontsize of the y tick labels
plt.rc('legend', fontsize=9)  # Fontsize of the legend
plt.rc('font', family='sans-serif')  # Use a sans-serif font
plt.rc('font', **{'sans-serif': 'Arial'})  # Specifically use Arial

colors = ['#abd9e9' if stats['p-value'] > 0.05 else '#4575b4' for stats in summary_stats.values()]
bars = sns.barplot(x=list(summary_stats.keys()), y=[data[f'Change_{mood}'].mean() for mood in mood_states], palette=colors)

plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.axhline(0, color='black', linewidth=0.8)

plt.yticks(np.arange(-3.0, 3.0, 0.5))


# Adding legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#4575b4', label='Significant Change'),
                   Patch(facecolor='#abd9e9', label='Non-significant Change')]
plt.legend(handles=legend_elements)

# Save and show plot
output_image = os.path.join(output_image_path, 'Mood_Changes_Significance.png')
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.show()
