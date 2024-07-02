import pandas as pd
from scipy.stats import ttest_rel
import os
import numpy as np

# Define file paths
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate the difference between before and after mood states for each participant
for mood in ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']:
    data[f'Difference_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Function to calculate Cohen's d for paired samples
def cohen_d_paired(x):
    return np.mean(x) / np.std(x, ddof=1)

# Statistical paired t-test to find out p value to test statistical value: p value < 0.05 means stat. difference is significant enough not to be random
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']
for mood in mood_states:
    print(f"Statistical Analysis for {mood}:")
    for condition in data['Condition'].unique():
        condition_data = data[data['Condition'] == condition]
        condition_diff = condition_data[f'Difference_{mood}']
        
        # Paired t-test
        t_stat, p_val = ttest_rel(condition_diff, [0] * len(condition_diff))
        
        # Calculate Cohen's d
        cohen_d = cohen_d_paired(condition_diff)
        
        print(f"Condition {condition}: p-value = {p_val:.4f}, Cohen's d = {cohen_d:.4f}")
    print()
