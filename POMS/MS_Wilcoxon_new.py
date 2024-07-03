import pandas as pd
from scipy.stats import wilcoxon
import os
import numpy as np

# Load your data
folder_path = 'POMS'
input_file = 'POMS_MS_participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Define a function for bootstrapping
def bootstrap(data, num_samples=1000):
    n = len(data)
    bootstrap_samples = np.random.choice(data, (num_samples, n), replace=True)
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    return np.percentile(bootstrap_means, [2.5, 97.5])

alpha = 0.05

# List of mood states to analyze
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']

# Iterate over each condition
for condition_id in range(3):  # Assuming there are 3 conditions
    print(f"\nAnalyzing Condition {condition_id}:")
    
    # Filter data for the current condition
    condition_data = data[data['Condition_x'] == condition_id]
    
    # Iterate over each mood state
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'

        
        # Extract actual columns from DataFrame
        before_scores = condition_data[before_col]
        after_scores = condition_data[after_col]
        
        # Apply bootstrapping only if there are enough samples
        if len(before_scores) > 1 and len(after_scores) > 1:
            ci = bootstrap(after_scores - before_scores)
            print(f"95% Confidence Interval for {mood}: {ci}")
        else:
            print(f"Not enough data to perform bootstrap for {mood}.")
            
        # Perform Wilcoxon signed-rank test
        stat, p_value = wilcoxon(before_scores, after_scores, zero_method='wilcox', correction=False, mode='exact')
        
        # Calculate the effect size using Method 2
        n = len(before_scores)
        effect_size = (2 * stat / (n * (n + 1))) - 1
    
        # Print the Wilcoxon test result and effect size
        print(f'{mood}: Statistics={stat}, p-value={p_value:.3f}, Effect Size={effect_size:.3f}')
            


