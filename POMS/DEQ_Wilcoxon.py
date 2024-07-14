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
results = []
for condition in data['Condition'].unique():
    condition_data = data[data['Condition'] == condition]
    
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        
        # Perform Wilcoxon signed-rank test
        stat, p_value = wilcoxon(condition_data[before_col], condition_data[after_col])
        n = len(condition_data[before_col])

        # Calculate effect size
        effect_size = calculate_effect_size(stat, n)
        
        # Store the Wilcoxon test result and effect size, including n
        results.append({
            'Condition': condition,
            'Mood': mood,
            'Statistics': stat,
            'p_value': p_value,
            'Effect Size': effect_size,
            'n': n
        })

# Perform Wilcoxon signed-rank test on all participants' data
for mood in mood_states:
    before_col = f'Before {mood}'
    after_col = f'After {mood}'
    
    # Perform Wilcoxon signed-rank test
    stat, p_value = wilcoxon(data[before_col], data[after_col])
    n = len(data[before_col])

    # Calculate effect size
    effect_size = calculate_effect_size(stat, n)
    
    # Store the Wilcoxon test result and effect size for all participants
    results.append({
        'Condition': 'ALL Participants',
        'Mood': mood,
        'Statistics': stat,
        'p_value': p_value,
        'Effect Size': effect_size,
        'n': n
    })

# Convert results to DataFrame for better visualization
results_df = pd.DataFrame(results)

# Print the results
print(results_df)

# Save the results to a CSV file for further analysis or reference
output_file = os.path.join(folder_path, 'wilcoxon_test_results.csv')
results_df.to_csv(output_file, index=False)
