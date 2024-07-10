import pandas as pd
from scipy.stats import ttest_ind
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

# Define the column for motion sickness
motion_sickness_col =  'Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'


# Filter out participants without motion sickness
no_motion_sickness = data[data[motion_sickness_col] == 'No'].copy()

# Define condition mapping
no_motion_sickness['Combined_Condition'] = no_motion_sickness['Condition_x'].replace({
    0: 'No Sound',
    1: 'Auditory Stimuli',
    2: 'Auditory Stimuli'
})

# Calculate change scores for each mood state
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood_state in mood_states:
    no_motion_sickness[f'Change_{mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

# Perform independent t-tests
results = []
for mood in mood_states:
    no_sound_data = no_motion_sickness[no_motion_sickness['Combined_Condition'] == 'No Sound'][f'Change_{mood}'].dropna()
    auditory_stimuli_data = no_motion_sickness[no_motion_sickness['Combined_Condition'] == 'Auditory Stimuli'][f'Change_{mood}'].dropna()

    t_stat, p_val = ttest_ind(no_sound_data, auditory_stimuli_data, equal_var=False)  # Welch's t-test for unequal variances
    results.append({'Mood State': mood, 't-statistic': t_stat, 'p-value': p_val})

# Create DataFrame to display results
results_df = pd.DataFrame(results)

# Plotting results
plt.figure(figsize=(14, 8))
group_means = no_motion_sickness.groupby('Combined_Condition')[[f'Change_{mood}' for mood in mood_states]].mean()
colors = sns.color_palette("Blues", n_colors=2)
bar_width = 0.35
index = np.arange(len(mood_states))

for i, condition in enumerate(group_means.index):
    plt.bar(index + i * bar_width, group_means.loc[condition], bar_width, label=condition, color=colors[i % len(colors)])

plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.title('Average Change in Mood States by Audio Condition')
plt.xticks(index + bar_width / 2, mood_states, rotation=45)
plt.legend(title='Condition')
plt.tight_layout()

# Display t-test results
print(results_df)

# Save the plot
output_image = os.path.join(folder_path, 'DEQ_change_comparison_plot.png')
plt.savefig(output_image)
plt.show()
