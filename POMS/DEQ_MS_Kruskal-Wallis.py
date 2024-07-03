import pandas as pd
import os
from scipy.stats import shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
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

# Split the data into the conditions
groups = [data[data['Condition_x'] == 0], data[data['Condition_x'] == 1], data[data['Condition_x'] == 2]]

def cohen_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / dof)

print("Kruskal-Wallis Test Results with Effect Size:")
for score in change_scores:
    stat, p_value = kruskal(groups[0][score], groups[1][score], groups[2][score])
    
    # Epsilon Squared calculation
    n = len(data)
    k = len(groups)
    epsilon_squared = (stat - k + 1) / (n - k)
    
    print(f'{score}: Statistics={stat}, p-value={p_value}, Epsilon Squared={epsilon_squared:.4f}')
    
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
        dunn_results = posthoc_dunn(data, val_col=score, group_col='Condition_x')
        print(dunn_results)
        
        # Effect size calculation for significant pairs
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                effect_size = cohen_d(groups[i][score].dropna(), groups[j][score].dropna())
                print(f'Effect Size (Cohen\'s d) between Group {i} and Group {j} for {score}: {effect_size:.4f}')
    else:
        print(f'There is no significant difference in {score} across the groups')
    print()
