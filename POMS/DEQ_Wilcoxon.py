import pandas as pd
from scipy.stats import wilcoxon
import os
import numpy as np

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

alpha = 0.05
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

def calculate_effect_size(stat, n):
    z = (stat - n * (n + 1) / 4) / np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    r = z / np.sqrt(n)
    return abs(r)

# Iterate over each condition and mood state
for condition in data['Condition'].unique():
    condition_data = data[data['Condition'] == condition]
    
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        # Perform Wilcoxon signed-rank test
        stat, p_value = wilcoxon(condition_data[before_col], condition_data[after_col])

        # Calculate effect size
        n = len(condition_data[before_col])
        effect_size = calculate_effect_size(stat, n)
        
        # Print the Wilcoxon test result and effect size
        print(f'Condition {condition}, Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}')
        
for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        # Perform Wilcoxon signed-rank test
        stat, p_value = wilcoxon(condition_data[before_col], condition_data[after_col])

        # Calculate effect size
        n = len(condition_data[before_col])
        effect_size = calculate_effect_size(stat, n)
        
        # Print the Wilcoxon test result and effect size
        print(f'ALL Participants: Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}')
        