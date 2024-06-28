import pandas as pd
from scipy.stats import wilcoxon
import os
import numpy as np

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

def bootstrap(data, num_samples=1000):
    n = len(data)
    bootstrap_samples = np.random.choice(data, (num_samples, n), replace=True)
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    return np.percentile(bootstrap_means, [2.5, 97.5])

alpha = 0.05

# List of mood states to analyze
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Analyzing Condition 0 separately
print("\nAnalyzing Condition 0:")
condition_0_data = data[data['Condition'] == 0]

for mood in mood_states:
    before_col = f'Before {mood}'
    after_col = f'After {mood}'
    
    before_scores = condition_0_data[before_col]
    after_scores = condition_0_data[after_col]
    
    if len(before_scores) > 1 and len(after_scores) > 1:
        differences = after_scores - before_scores
        ci = bootstrap(differences)
        print(f"95% Confidence Interval for {mood}: {ci}")
    else:
        print(f"Not enough data to perform bootstrap for {mood}.")
    
    differences = after_scores - before_scores
    
    if np.all(differences == 0):
        print(f"No changes detected in {mood}, skipping Wilcoxon test.")
    else:
        stat, p_value = wilcoxon(before_scores, after_scores, zero_method='wilcox', correction=False, mode='approx')
    
        print(f'Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}')
        
        if p_value < alpha:
            print(f'Reject the null hypothesis: There is a significant change in {mood}.')
        else:
            print(f'Fail to reject the null hypothesis: There is no significant change in {mood}.')

# Analyzing Conditions 1 and 2 combined
print("\nAnalyzing Conditions 1 and 2 combined:")
condition_1_2_data = data[data['Condition'].isin([1, 2])]

for mood in mood_states:
    before_col = f'Before {mood}'
    after_col = f'After {mood}'
    
    before_scores = condition_1_2_data[before_col]
    after_scores = condition_1_2_data[after_col]
    
    if len(before_scores) > 1 and len(after_scores) > 1:
        differences = after_scores - before_scores
        ci = bootstrap(differences)
        print(f"95% Confidence Interval for {mood}: {ci}")
    else:
        print(f"Not enough data to perform bootstrap for {mood}.")
    
    differences = after_scores - before_scores
    
    if np.all(differences == 0):
        print(f"No changes detected in {mood}, skipping Wilcoxon test.")
    else:
        stat, p_value = wilcoxon(before_scores, after_scores, zero_method='wilcox', correction=False, mode='approx')
    
        print(f'Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}')
        
        if p_value < alpha:
            print(f'Reject the null hypothesis: There is a significant change in {mood}.')
        else:
            print(f'Fail to reject the null hypothesis: There is no significant change in {mood}.')
