import pandas as pd
import os
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
import numpy as np
from numpy import mean, sqrt

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Create change scores for each mood state
data['Change_Tension'] = data['After Tension'] - data['Before Tension']
data['Change_Vigor'] = data['After Vigor'] - data['Before Vigor']
data['Change_Confusion'] = data['After Confusion'] - data['Before Confusion']
data['Change_Fatigue'] = data['After Fatigue'] - data['Before Fatigue']
data['Change_Anger'] = data['After Anger_x'] - data['Before Anger_x']
data['Change_Depression'] = data['After Depression'] - data['Before Depression']

change_scores = [
    'Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 
    'Change_Anger', 'Change_Depression'
]

# Split the data into the conditions
groups = [data[data['Condition'] == 0], data[data['Condition'] == 1], data[data['Condition'] == 2]]

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
    
    # Effect size calculation for all pairs
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            effect_size = cohen_d(groups[i][score].dropna(), groups[j][score].dropna())
            #print(f'Effect Size (Cohen\'s d) between Group {i} and Group {j} for {score}: {effect_size:.4f}')
    
    if p_value < 0.05:
        print(f'There is a significant difference in {score} across the groups')
        dunn_results = posthoc_dunn(data, val_col=score, group_col='Condition')
        print(dunn_results)
    #else:
        #print(f'There is no significant difference in {score} across the groups')
    #print()
