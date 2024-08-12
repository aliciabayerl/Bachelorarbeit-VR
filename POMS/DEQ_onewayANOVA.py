import pandas as pd
from scipy.stats import f_oneway
import os

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate change scores
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']
for mood_state in mood_states:
    data[f'Change_{mood_state}'] = data[f'After {mood_state}'] - data[f'Before {mood_state}']

# Group conditions
groups = [data[data['Condition'] == i] for i in range(3)]

def calculate_eta_squared(f_stat, num_groups, num_samples):
    # Eta squared calculation
    eta_squared = f_stat * (num_groups - 1) / (f_stat * (num_groups - 1) + (num_samples - num_groups))
    return eta_squared

print("One-Way ANOVA Results:")
for score in mood_states:
    change_scores = [group[f'Change_{score}'] for group in groups]
    f_stat, p_value = f_oneway(*change_scores)
    
    # Calculate effect size (eta squared)
    num_groups = len(groups)
    num_samples = sum(len(group) for group in groups)
    eta_squared = calculate_eta_squared(f_stat, num_groups, num_samples)
    
    print(f'{score}: F-statistic={f_stat:.3f}, p-value={p_value:.3f}, eta squared={eta_squared:.3f}')
    
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
    else:
        print(f'There is no significant difference in {score} across the groups')
    print()
