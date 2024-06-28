import pandas as pd
from scipy.stats import wilcoxon
import os


folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)


alpha = 0.05
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Iterate over each condition and mood state
for condition in data['Condition'].unique():
    condition_data = data[data['Condition'] == condition]
    
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        stat, p_value = wilcoxon(condition_data[before_col], condition_data[after_col])
        
        print(f'Condition {condition}, Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}')
        
        if p_value < alpha:
            print(f'Reject the null hypothesis: There is a significant change in {mood}.')
        else:
            print(f'Fail to reject the null hypothesis: There is no significant change in {mood}.')
        


