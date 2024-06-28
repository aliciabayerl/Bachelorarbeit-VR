import pandas as pd
import os
from scipy.stats import mannwhitneyu

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate change scores
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

# Group conditions
data['Condition_Grouped'] = data['Condition'].replace({1: '1_and_2', 2: '1_and_2'})

groups = {
    '0': data[data['Condition_Grouped'] == 0],
    '1_and_2': data[data['Condition_Grouped'] == '1_and_2']
}

print("Mann-Whitney U Test Results:")
for score in change_scores:
    group_0_scores = groups['0'][score]
    group_1_and_2_scores = groups['1_and_2'][score]
    
    # Mann-Whitney U test
    stat, p_value = mannwhitneyu(group_0_scores, group_1_and_2_scores, alternative='two-sided')
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
    else:
        print(f'There is no significant difference in {score} across the groups')
    print()
