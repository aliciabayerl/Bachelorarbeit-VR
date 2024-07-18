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
motion_sickness_col = 'Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'

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

# Function to calculate Cohen's d
def cohen_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / dof)

# Perform independent t-tests and calculate effect sizes
results = []
for mood in mood_states:
    no_sound_data = no_motion_sickness[no_motion_sickness['Combined_Condition'] == 'No Sound'][f'Change_{mood}'].dropna()
    auditory_stimuli_data = no_motion_sickness[no_motion_sickness['Combined_Condition'] == 'Auditory Stimuli'][f'Change_{mood}'].dropna()

    if len(no_sound_data) > 0 and len(auditory_stimuli_data) > 0:
        t_stat, p_val = ttest_ind(no_sound_data, auditory_stimuli_data)
        effect_size = cohen_d(no_sound_data, auditory_stimuli_data)
        results.append({'Mood State': mood, 't-statistic': t_stat, 'p-value': p_val, 'Effect Size (Cohen\'s d)': effect_size})
    else:
        results.append({'Mood State': mood, 't-statistic': np.nan, 'p-value': np.nan, 'Effect Size (Cohen\'s d)': np.nan})

# Create DataFrame to display results
results_df = pd.DataFrame(results)

# Plotting results
plt.figure(figsize=(6, 4))
plt.rc('axes', labelsize=10)  # Fontsize of the x and y labels
plt.rc('xtick', labelsize=9)  # Fontsize of the x tick labels
plt.rc('ytick', labelsize=9)  # Fontsize of the y tick labels
plt.rc('legend', fontsize=9)  # Fontsize of the legend
plt.rc('font', family='sans-serif')  # Use a sans-serif font
plt.rc('font', **{'sans-serif': 'Arial'})  # Specifically use Arial

group_means = no_motion_sickness.groupby('Combined_Condition')[[f'Change_{mood}' for mood in mood_states]].mean()
colors = ["#abd9e9", "#4575b4"]
bar_width = 0.35
index = np.arange(len(mood_states))

for i, condition in enumerate(group_means.index):
    mean_changes = group_means.loc[condition].apply(lambda x: x if x != 0 else 0.01)
    for j, value in enumerate(mean_changes):
        color = 'darkblue' if value == 0.01 else colors[i % len(colors)]
        plt.bar(index[j] + i * bar_width, value, bar_width, label=condition if j == 0 else "", color=color)

plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.ylim(-7, 6)  # Adjust the y-axis limits for better visibility
plt.xticks(index + bar_width / 2, mood_states)
plt.legend(title='')
plt.tight_layout()

# Display t-test results
print(results_df)

# Save the plot
output_image = os.path.join(folder_path, 'DEQ_change_comparison_plot.png')
plt.savefig(output_image)
plt.show()
