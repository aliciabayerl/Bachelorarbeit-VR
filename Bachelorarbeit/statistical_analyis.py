import pandas as pd
from scipy.stats import ttest_rel

# Load the data
data = pd.read_csv('participant_scores.csv')

# Calculate the difference between "Before" and "After" mood states for each participant
for mood in ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']:
    data[f'Difference_{mood}'] = data[f'After {mood}'] - data[f'Before {mood}']

# Perform statistical tests for each mood state
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']
for mood in mood_states:
    print(f"Statistical Analysis for {mood}:")
    for condition in data['Condition'].unique():
        condition_data = data[data['Condition'] == condition]
        condition_diff = condition_data[f'Difference_{mood}']
        
        # Perform paired t-test
        t_stat, p_val = ttest_rel(condition_diff, [0] * len(condition_diff))
        print(f"Condition {condition}: p-value = {p_val:.4f}")
    print()
