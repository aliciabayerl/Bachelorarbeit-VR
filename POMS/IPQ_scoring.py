import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from scipy.stats import shapiro, levene

def map_5_to_7_scale(value):
    scale_mapping = {
        -2: 0,
        -1: 2,
        0: 3.5,
        1: 5,
        2: 6,
    }
    mapped_value = scale_mapping.get(value, np.nan)
    print(f"Value: {value} -> Mapped Value: {mapped_value}")
    return mapped_value

def preprocess_value(value):
    if isinstance(value, str):
        value = value.split()[0]
    try:
        processed_value = int(float(value))  
    except ValueError:
        processed_value = np.nan
    print(f"Original Value: {value} -> Processed Value: {processed_value}")
    return processed_value

folder_path = 'POMS'
input_file = 'questionnaire2.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

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

# Reverse score items
reverse_items = {
    'SP': ['Matrix >> I felt like I was just perceiving pictures.'],
    'INV': ['Matrix >> I still paid attention to the real environment.'],
    'REAL': ['Matrix >> How real did the virtual world seem to you?']
}

def compute_ipq_means(data, ipq_items):
    for category, items in ipq_items.items():
        for item in items:
            if item in data.columns:
                data[item] = data[item].apply(preprocess_value)
                data[item] = data[item].apply(map_5_to_7_scale)
                if item in reverse_items.get(category, []):
                    data[item] = -1 * data[item] + 6
            else:
                print(f"Column not found: {item}")
                data[item] = None  
        
        # Compute mean
        valid_items = [item for item in items if item in data.columns]
        if valid_items:
            data[f'{category}_mean'] = data[valid_items].mean(axis=1)
            data[f'{category}_median'] = data[valid_items].median(axis=1)
        else:
            data[f'{category}_mean'] = None
            data[f'{category}_median'] = None

    # Compute overall presence mean and median
    data['Overall_Presence_mean'] = data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)
    data['Overall_Presence_median'] = data[['SP_mean', 'INV_mean', 'REAL_mean']].median(axis=1)

    data['Participant'] = data.index + 1

compute_ipq_means(data, ipq_items)
selected_columns = ['Condition', 'Participant'] + [f'{category}_mean' for category in ipq_items.keys()] + ['Overall_Presence_mean']
selected_columns2 = ['Condition', 'Participant'] + [f'{category}_median' for category in ipq_items.keys()] + ['Overall_Presence_median']

ipq_scores_data = data[selected_columns]
ipq_scores_data2 = data[selected_columns2]

output_file = 'IPQ_scores.csv'
output_file2 = 'IPQ_scores_median.csv'

output_file_path = os.path.join(folder_path, output_file)
output_file_path2 = os.path.join(folder_path, output_file2)

ipq_scores_data.to_csv(output_file_path, index=False)
ipq_scores_data2.to_csv(output_file_path2, index=False)

# Descriptive statistics for all participants
desc_stats_all = ipq_scores_data.describe().T
desc_stats_all['IQR'] = desc_stats_all['75%'] - desc_stats_all['25%']
desc_stats_all = desc_stats_all[['mean', 'std', '50%', 'IQR', '25%', '75%', 'min', 'max']]
print("Descriptive Statistics for All Participants:\n", desc_stats_all)

# Descriptive statistics for each condition
conditions = data['Condition'].unique()
desc_stats_by_condition = {}

for condition in conditions:
    condition_data = ipq_scores_data[data['Condition'] == condition]
    desc_stats = condition_data.describe().T
    desc_stats['IQR'] = desc_stats['75%'] - desc_stats['25%']
    desc_stats = desc_stats[['mean', 'std', '50%', 'IQR', '25%', '75%', 'min', 'max']]
    desc_stats_by_condition[condition] = desc_stats
    print(f"Descriptive Statistics for Condition {condition}:\n", desc_stats)


# Normality and variance tests
categories = ['SP', 'INV', 'REAL', 'Overall_Presence']

print("Normality Tests:")
for category in categories:
    stat, p_value = shapiro(ipq_scores_data[f'{category}_mean'].dropna())
    print(f'{category}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'{category} mean is normally distributed\n')
    else:
        print(f'{category} mean is not normally distributed\n')

print("Homogeneity of Variance Tests:")
for category in categories:
    stat, p_value = levene(ipq_scores_data[ipq_scores_data['Condition'] == 0][f'{category}_mean'],
                           ipq_scores_data[ipq_scores_data['Condition'] == 1][f'{category}_mean'],
                           ipq_scores_data[ipq_scores_data['Condition'] == 2][f'{category}_mean'])
    print(f'{category}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'Variances for {category} are equal across groups\n')
    else:
        print(f'Variances for {category} are not equal across groups\n')


categories = ['SP', 'INV', 'REAL']
colors = ['r', 'g', 'b']

N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Create radar chart
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.set_ylim(0, 6)

for condition in range(3):
    mean_values = ipq_scores_data[[f'{category}_mean' for category in categories]].iloc[condition].tolist()
    mean_values += mean_values[:1]

    ax.plot(angles, mean_values, color=colors[condition], linewidth=2, linestyle='solid', label=f'Condition {condition}')

plt.xticks(angles[:-1], categories)
plt.title('Radar Chart for IPQ Scores')
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()
