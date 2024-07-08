import pandas as pd
from scipy.stats import ttest_rel
import os
import numpy as np

# Define file paths
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)

# Load the data
data = pd.read_csv(file_path)

# Calculate the difference between before and after mood states for each participant
for mood in ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']:
    data[f'Difference_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Define the mood states
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']

# Perform statistical analysis and calculate Cohen's d
for mood in mood_states:
    print(f"Statistical Analysis for {mood}:")
    for condition in data['Condition'].unique():
        condition_data = data[data['Condition'] == condition]
        condition_diff = condition_data[f'Difference_{mood}']
        
        # Paired t-test
        t_stat, p_val = ttest_rel(condition_diff, [0] * len(condition_diff))
        
        # Calculate Cohen's d
        mean_diff = condition_diff.mean()
        std_diff = condition_diff.std()
        cohen_d = mean_diff / std_diff
        
        # Calculate degrees of freedom
        df = len(condition_diff) - 1
        
        print(f"Condition {condition}: t-statistic = {t_stat:.4f}, p-value = {p_val:.4f}, Cohen's d = {cohen_d:.4f}, df = {df}")
    print()

# Perform statistical analysis and calculate Cohen's d for all participants combined
print("Statistical Analysis for All Participants Across All Conditions:")
for mood in ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']:
    differences = data[f'Difference_{mood}']
    if np.all(differences == 0):
        print(f"{mood}: No changes detected, skipping t-test.")
    else:
        t_stat, p_val = ttest_rel(differences, [0] * len(differences))
        mean_diff = differences.mean()
        std_diff = differences.std(ddof=1)  # Use sample standard deviation
        cohen_d = mean_diff / std_diff if std_diff != 0 else 0  # Avoid division by zero
        df = len(differences) - 1  # Calculate degrees of freedom
        print(f"{mood}: t-statistic = {t_stat:.4f}, p-value = {p_val:.4f}, Cohen's d = {cohen_d:.4f}, df = {df}")
