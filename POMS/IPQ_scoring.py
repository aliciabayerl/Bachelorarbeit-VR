import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt
from math import pi



def map_5_to_7_scale(value):
    scale_mapping = {
        -2: 0,
        -1: 2,
        0: 3.5,
        1: 5,
        2: 6
    }
    return scale_mapping.get(value, np.nan)

def preprocess_value(value):
    if isinstance(value, str):
        value = value.split()[0]
    try:
        return int(value)
    except ValueError:
        return np.nan

folder_path = 'POMS'
input_file = 'questionnaire.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)
print(data.columns)


ipq_items = {
    'SP': [
        'Matrix >> I did not feel present in the virtual space.',
        'Matrix >> In the computer generated world I had a sense of "being there"',
        'Matrix >> Somehow I felt that the virtual world surrounded me.',
        'Matrix >> I felt like I was just perceiving pictures.',
        'Matrix >> I had a sense of acting in the virtual space, rather than operating something from outside',
        'Matrix >> I felt present in the virtual space.'
    ],
    'INV': [
        'Matrix >> How aware were you of the real world surrounding while navigating in the virtual world? (i.e. sounds, room temperature, other people, etc.)?',
        'Matrix >> I was not aware of my real environment',
        'Matrix >> I still paid attention to the real environment.',
        'Matrix >> I was completely captivated by the virtual world.'
    ],
    'REAL': [
        'Matrix >> How real did the virtual world seem to you?',
        'Matrix >> How much did your experience in the virtual environment seem consistent with your real world experience ?',
        'Matrix >> The virtual world seemed more realistic than the real world.'
    ]
}

def compute_ipq_means(data, ipq_items, condition):
    for category, items in ipq_items.items():
        for item in items:
            if item in data.columns:
                data[item] = data[item].apply(preprocess_value)
                data[item] = data[item].apply(map_5_to_7_scale)
            else:
                print(f"Column not found: {item}")
        
        data[f'{category}_mean_condition_{condition}'] = data[items].mean(axis=1)

categories = ['SP', 'INV', 'REAL']
colors = ['r', 'g', 'b']

N = len(categories)

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Create radar chart
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.set_ylim(0, 6)

for condition in range(3):
    compute_ipq_means(data, ipq_items, condition)
    
    mean_values = data[[f'{category}_mean_condition_{condition}' for category in categories]].mean().tolist()
    mean_values += mean_values[:1]

    ax.plot(angles, mean_values, color=colors[condition], linewidth=2, linestyle='solid', label=f'Condition {condition}')

plt.xticks(angles[:-1], categories)

plt.title('Radar Chart for IPQ Scores')

plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()