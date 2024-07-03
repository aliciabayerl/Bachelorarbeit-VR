import pandas as pd
from scipy.stats import wilcoxon
import os

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

alpha = 0.05

# List of mood states to analyze
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']

# Function to calculate rank-biserial correlation as effect size
def rank_biserial_effect_size(w_stat, n):
    return (2 * w_stat / (n * (n + 1))) - 1

# Iterate over each condition and mood state
for condition in data['Condition'].unique():
    condition_data = data[data['Condition'] == condition]
    
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        stat, p_value = wilcoxon(condition_data[before_col], condition_data[after_col])
        
        # Calculate effect size
        n = len(condition_data)
        effect_size = rank_biserial_effect_size(stat, n)
        
        print(f'Condition {condition}, Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}')
        
        if p_value < alpha:
            print(f'Reject the null hypothesis: There is a significant change in {mood}.')
        else:
            print(f'Fail to reject the null hypothesis: There is no significant change in {mood}.')
