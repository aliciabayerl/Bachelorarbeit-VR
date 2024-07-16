import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Define file paths
folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)

# Define mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Calculate the change in mood states
for mood_state in mood_states:
    participant_scores[f'Change {mood_state}'] = participant_scores[f'After {mood_state}'] - participant_scores[f'Before {mood_state}']

# Define conditions and color palette
conditions = sorted(participant_scores['Condition'].unique(), reverse=True)
palette = ["#abd9e9", "#74add1", "#4575b4"]

# Create the plot
fig, ax = plt.subplots(figsize=(6, 4))  # Adjust figure size to be more compact
plt.rc('axes', labelsize=9)  # Fontsize of the x and y labels
plt.rc('xtick', labelsize=9)  # Fontsize of the x tick labels
plt.rc('ytick', labelsize=9)  # Fontsize of the y tick labels
plt.rc('legend', fontsize=9)  # Fontsize of the legend
plt.rc('font', family='sans-serif')  # Use a sans-serif font
plt.rc('font', **{'sans-serif': 'Arial'})  # Specifically use Arial

# Plot the data
for condition in conditions:
    condition_data = participant_scores[participant_scores['Condition'] == condition]
    x_values = mood_states
    y_values = [condition_data[f'Change {mood}'].mean() for mood in mood_states]
    ax.plot(x_values, y_values, marker='o', label=f'Condition {condition}', color=palette[condition % len(palette)])

# Label the axes
ax.set_xlabel('Mood State')
ax.set_ylabel('Average Change')

# Add legend
ax.legend(title='Condition', loc='lower left')

# Save and show the plot
output_image = os.path.join(image_path, 'DEQ_average_change_plot.png')
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.show()
