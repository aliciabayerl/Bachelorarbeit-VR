import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
output_image_path = os.path.join(folder_path, 'Plot_Images')

data = pd.read_csv(file_path)

mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood in mood_states:
    data[f'Change_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

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
plt.figure(figsize=(10, 6))  
colors = ['#abd9e9' if stats['p-value'] > 0.05 else '#4575b4' for stats in summary_stats.values()]
bars = sns.barplot(x=list(summary_stats.keys()), y=[data[f'Change_{mood}'].mean() for mood in mood_states], palette=colors)
plt.title('Average Change in Mood States by Condition with Significance Highlighting')
plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.axhline(0, color='black', linewidth=0.8) 
plt.grid(True, linestyle='--', alpha=0.6)

# Adding legend 
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#4575b4', label='Significant Change'),
                   Patch(facecolor='#abd9e9', label='Non-significant Change')]
plt.legend(handles=legend_elements, title="Significance")

output_image = os.path.join(output_image_path, 'Mood_Changes_Significance.png')
plt.savefig(output_image)
plt.show()
