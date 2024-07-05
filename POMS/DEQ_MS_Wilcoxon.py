import pandas as pd
from scipy.stats import wilcoxon
import os
import numpy as np

# Load your data
folder_path = 'POMS'
input_file = 'DEQ_MS_participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

def bootstrap(data, num_samples=1000):
    n = len(data)
    bootstrap_samples = np.random.choice(data, (num_samples, n), replace=True)
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    return np.percentile(bootstrap_means, [2.5, 97.5])

def calculate_effect_size(stat, n):
    z = (stat - n * (n + 1) / 4) / np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    r = z / np.sqrt(n)
    return abs(r)

alpha = 0.05

# List of mood states to analyze
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

for condition_id in range(3):  
    print(f"\nAnalyzing Condition {condition_id}:")
    
    condition_data = data[data['Condition_x'] == condition_id]
    
    # Iterate over each mood state
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        # Extract actual columns from DataFrame
        before_scores = condition_data[before_col]
        after_scores = condition_data[after_col]
        
        # Compute differences between after and before scores
        differences = after_scores - before_scores
        
        # Apply bootstrapping only if there are enough samples
        if len(before_scores) > 1 and len(after_scores) > 1:
            ci = bootstrap(differences)
            print(f"95% Confidence Interval for {mood}: {ci}")
        else:
            print(f"Not enough data to perform bootstrap for {mood}.")
        
        if np.all(differences == 0):
            print(f"No changes detected in {mood}, skipping Wilcoxon test.")
        else:
            # Perform Wilcoxon signed-rank test
            stat, p_value = wilcoxon(before_scores, after_scores, zero_method='wilcox', correction=False, mode='approx')
            
            # Calculate the effect size
            n = len(before_scores)
            effect_size = calculate_effect_size(stat, n)
        
            # Print the Wilcoxon test result, effect size, and confidence interval
            print(f'Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}')
            
        

