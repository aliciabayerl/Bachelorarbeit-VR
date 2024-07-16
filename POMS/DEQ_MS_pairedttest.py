import pandas as pd
from scipy.stats import ttest_rel
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths
folder_path = 'POMS'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)

# Load the data
data = pd.read_csv(file_path)

# Define the column name for motion sickness
motion_sickness_col = 'Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'

# Separate data into motion sickness and no motion sickness groups
motion_sickness = data[data[motion_sickness_col] == 'Yes'].copy()
no_motion_sickness = data[data[motion_sickness_col] == 'No'].copy()

# Calculate the change scores for each mood state in both groups
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood in mood_states:
    motion_sickness[f'Change_{mood}'] = motion_sickness[f'After {mood}'] - motion_sickness[f'Before {mood}']
    no_motion_sickness[f'Change_{mood}'] = no_motion_sickness[f'After {mood}'] - no_motion_sickness[f'Before {mood}']

def cohen_d(x, y):
    """Compute Cohen's d for paired samples."""
    n = len(x)
    diff = x - y
    return np.mean(diff) / np.std(diff, ddof=1)

def analyze_and_plot(group_data, group_name):
    results = []
    for mood in mood_states:
        mood_change = group_data[f'Change_{mood}']
        t_stat, p_val = ttest_rel(mood_change, [0] * len(mood_change))
        mean_diff = mood_change.mean()
        std_diff = mood_change.std()
        effect_size = cohen_d(mood_change, np.zeros(len(mood_change)))  # Calculate Cohen's d
        df = len(mood_change) - 1  # Calculate degrees of freedom

        results.append({
            'Mood': mood,
            'Mean Difference': mean_diff,
            'Standard Deviation': std_diff,
            'p-value': p_val,
            'Cohen\'s d': effect_size,
            'Degrees of Freedom': df,
            't-statistic': t_stat,
            'Group': group_name
        })
        
        print(f"{group_name} - {mood}: Mean Difference = {mean_diff:.2f}, Std Dev = {std_diff:.2f}, p-value = {p_val:.4f}, Cohen's d = {effect_size:.2f}, df = {df}, t-statistic = {t_stat:.2f}")

    results_df = pd.DataFrame(results)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Mood', y='Mean Difference', hue='Group', data=results_df)
    plt.title(f'Mean Change in Mood States for {group_name}')
    plt.ylabel('Mean Difference')
    plt.xlabel('Mood State')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Analyze and plot for no motion sickness group
analyze_and_plot(no_motion_sickness, "No Motion Sickness")

# Analyze and plot for motion sickness group
analyze_and_plot(motion_sickness, "Motion Sickness")

# Perform statistical analysis for each condition and all conditions combined
def analyze_conditions(data, group_name):
    conditions = data['Condition_x'].unique()
    combined_conditions = [1, 2]  # Combining conditions 1 and 2

    for condition in conditions:
        condition_data = data[data['Condition_x'] == condition]
        analyze_and_plot(condition_data, f"{group_name} - Condition {condition}")

    combined_data = data[data['Condition_x'].isin(combined_conditions)]
    analyze_and_plot(combined_data, f"{group_name} - Combined Condition 1 & 2")

# Analyze for no motion sickness group
analyze_conditions(no_motion_sickness, "No Motion Sickness")

# Analyze for motion sickness group
analyze_conditions(motion_sickness, "Motion Sickness")
