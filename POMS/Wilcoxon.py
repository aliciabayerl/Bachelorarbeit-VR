import pandas as pd
from scipy.stats import wilcoxon
import os
import numpy as np

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

alpha = 0.05
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']

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
        n = len(condition_data[before_col])

        # Calculate effect size
        effect_size = calculate_effect_size(stat, n)
        
        # Print the Wilcoxon test result and effect size, including n
        print(f'Condition {condition}, Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}, n={n}')

# Assuming 'ALL Participants' was meant to aggregate data from all conditions, not just one
all_data_before = data.filter(like='Before')
all_data_after = data.filter(like='After')

for mood in mood_states:
    before_col = f'Before {mood}'
    after_col = f'After {mood}'
    
    # Perform Wilcoxon signed-rank test on all participants' data
    stat, p_value = wilcoxon(data[before_col], data[after_col])
    n = len(data[before_col])

    # Calculate effect size
    effect_size = calculate_effect_size(stat, n)
    
    # Print the Wilcoxon test result and effect size for all participants
    print(f'ALL Participants: Change_{mood}: Statistics={stat:.3f}, p={p_value:.3f}, Effect Size={effect_size:.3f}, n={n}')
