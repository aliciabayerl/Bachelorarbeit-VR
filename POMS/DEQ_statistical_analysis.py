import pandas as pd
from scipy.stats import ttest_rel
import os

# Define file paths
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)

# Load the data
data = pd.read_csv(file_path)

# Calculate the difference between before and after mood states for each participant
for mood in ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']:
    data[f'Difference_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Define the mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

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
        
        print(f"Condition {condition}: p-value = {p_val:.4f}, Cohen's d = {cohen_d:.4f}")
    print()
