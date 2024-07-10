import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define file paths
folder_path = 'POMS'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)

# Load the data
data = pd.read_csv(file_path)

# Define the column name for motion sickness
motion_sickness_col = 'Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'

# Separate data into no motion sickness group
no_motion_sickness = data[data[motion_sickness_col] == 'No'].copy()

# Define the Condition mapping
no_motion_sickness['Combined_Condition'] = no_motion_sickness['Condition_x'].replace({
    0: 'No Sound',
    1: 'Auditory Stimuli',
    2: 'Auditory Stimuli'
})

# Calculate the change scores for each mood state
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood_state in mood_states:
    no_motion_sickness[f'Change_{mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

# Prepare the data for plotting
group_means = no_motion_sickness.groupby('Combined_Condition')[[f'Change_{mood}' for mood in mood_states]].mean()

# Create a bar plot using a standard blue palette
colors = sns.color_palette("Blues", n_colors=2)  
plt.figure(figsize=(14, 8))
bar_width = 0.35  # width of bars
index = np.arange(len(mood_states)) 

# Plot each condition
for i, condition in enumerate(group_means.index):
    plt.bar(index + i * bar_width, group_means.loc[condition], bar_width, label=condition, color=colors[i % len(colors)])

plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.title('Average Change in Mood States for Participants with No Motion Sickness by Audio Condition')
plt.xticks(index + bar_width / 2, mood_states, rotation=45)
plt.legend(title='Condition')
plt.tight_layout()

# Save the plot
output_image = os.path.join(folder_path, 'DEQ_change_comparison_plot.png')
plt.savefig(output_image)
plt.show()
