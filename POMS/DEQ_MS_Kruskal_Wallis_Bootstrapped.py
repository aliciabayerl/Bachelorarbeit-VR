import pandas as pd
import os
from scipy.stats import kruskal
import scikit_posthocs as sp
import numpy as np
from numpy import mean, sqrt

# Load your data
folder_path = 'POMS'
input_file = 'DEQ_MS_participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Create change scores for each mood state
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

# Combine conditions 1 and 2 into a single group
data['Condition_Grouped'] = data['Condition_x'].replace({1: '1_and_2', 2: '1_and_2'})

# Split the data into the new groups
groups = {
    '0': data[data['Condition_Grouped'] == 0],
    '1_and_2': data[data['Condition_Grouped'] == '1_and_2']
}

def bootstrap(data, num_samples=1000):
    n = len(data)
    bootstrap_samples = np.random.choice(data, (num_samples, n), replace=True)
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    return np.percentile(bootstrap_means, [2.5, 97.5])

def cohen_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / dof)

alpha = 0.05

print("Kruskal-Wallis Test Results with Bootstrap and Effect Size:")
for score in change_scores:
    stat, p_value = kruskal(groups['0'][score], groups['1_and_2'][score])
    
    # Epsilon Squared calculation
    n = len(data)
    k = len(groups)
    epsilon_squared = (stat - k + 1) / (n - k)
    
    print(f'{score}: Statistics={stat}, p-value={p_value}, Epsilon Squared={epsilon_squared:.4f}')
    
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
        dunn_results = sp.posthoc_dunn(data, val_col=score, group_col='Condition_Grouped')
        print(dunn_results)
    else:
        print(f'There is no significant difference in {score} across the groups')
        
    # Bootstrap confidence intervals
    ci_0 = bootstrap(groups['0'][score].dropna())
    ci_1_and_2 = bootstrap(groups['1_and_2'][score].dropna())
    
    # Effect size calculation
    effect_size = cohen_d(groups['0'][score].dropna(), groups['1_and_2'][score].dropna())
    
    print(f'95% Confidence Interval for {score} in Condition 0: {ci_0}')
    print(f'95% Confidence Interval for {score} in Condition 1_and_2: {ci_1_and_2}')
    print(f'Effect Size (Cohen\'s d) for {score}: {effect_size:.4f}')
    print()
