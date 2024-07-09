import pandas as pd
import os
from scipy.stats import mannwhitneyu

# Load your data
folder_path = 'POMS'
input_file_no_motion_sickness = 'DEQ_MS_participant_scores.csv'
input_file_motion_sickness = 'DEQ_MSyes_participant_scores.csv'

file_path_no_motion_sickness = os.path.join(folder_path, input_file_no_motion_sickness)
file_path_motion_sickness = os.path.join(folder_path, input_file_motion_sickness)

data_no_motion_sickness = pd.read_csv(file_path_no_motion_sickness)
data_motion_sickness = pd.read_csv(file_path_motion_sickness)

# Calculate change scores
for data in [data_no_motion_sickness, data_motion_sickness]:
    data['Change_Anger'] = data['After Anger'] - data['Before Anger']
    data['Change_Disgust'] = data['After Disgust'] - data['Before Disgust']
    data['Change_Fear'] = data['After Fear'] - data['Before Fear']
    data['Change_Anxiety'] = data['After Anxiety'] - data['Before Anxiety']
    data['Change_Sadness'] = data['After Sadness'] - data['Before Sadness']
    data['Change_Desire'] = data['After Desire'] - data['Before Desire']
    data['Change_Relaxation'] = data['After Relaxation'] - data['Before Relaxation']
    data['Change_Happiness'] = data['After Happiness'] - data['Before Happiness']

change_scores = [
    'Change_Anger', 'Change_Disgust', 'Change_Fear', 'Change_Anxiety', 
    'Change_Sadness', 'Change_Desire', 'Change_Relaxation', 'Change_Happiness'
]

# Function to calculate rank-biserial correlation
def rank_biserial_correlation(U, n1, n2):
    return 1 - (2 * U) / (n1 * n2)

print("Mann-Whitney U Test Results:")
for score in change_scores:
    group_no_motion_sickness = data_no_motion_sickness[score]
    group_motion_sickness = data_motion_sickness[score]
    
    # Mann-Whitney U test
    stat, p_value = mannwhitneyu(group_no_motion_sickness, group_motion_sickness, alternative='two-sided')
    n1 = len(group_no_motion_sickness)
    n2 = len(group_motion_sickness)
    effect_size = rank_biserial_correlation(stat, n1, n2)
    
    print(f'{score}: Statistics={stat}, p-value={p_value}, Effect Size={effect_size:.3f}')
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
    else:
        print(f'There is no significant difference in {score} across the groups')
    print()
