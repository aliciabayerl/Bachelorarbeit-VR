import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import os

folder_path = 'POMS'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

data['Change_Tension'] = data['After Tension'] - data['Before Tension']
data['Change_Vigor'] = data['After Vigor'] - data['Before Vigor']
data['Change_Confusion'] = data['After Confusion'] - data['Before Confusion']
data['Change_Fatigue'] = data['After Fatigue'] - data['Before Fatigue']
data['Change_Anger'] = data['After Anger_x'] - data['Before Anger_x']
data['Change_Depression'] = data['After Depression'] - data['Before Depression']

condition_1 = data[data['Condition'] == 1]
condition_2 = data[data['Condition'] == 2]
condition_0 = data[data['Condition'] == 0]

desc_stats_1 = condition_1.describe()
desc_stats_2 = condition_2.describe()
desc_stats_0 = condition_0.describe()


print("Condition 1 Descriptive Statistics:\n", desc_stats_1)
print("Condition 2 Descriptive Statistics:\n", desc_stats_2)
print("Condition 0 Descriptive Statistics:\n", desc_stats_0)


desc_stats_1.to_csv('condition_1.csv')
desc_stats_2.to_csv('condition_2.csv')
desc_stats_0.to_csv('condition_0.csv')

mood_states = ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']

plt.figure(figsize=(15, 20))
for i, mood in enumerate(mood_states, start=1):
    plt.subplot(3, 2, i)
    sns.boxplot(x='Condition', y=mood, data=data)
    plt.title(f'Change in {mood} by Condition')

plt.tight_layout()
plt.savefig('mood_changes_boxplots.png')
plt.close()

# Perform Mann-Whitney U Test for each mood state
results = {}
for mood in mood_states:
    stat, p = mannwhitneyu(condition_1[mood], condition_2[mood])
    results[mood] = (stat, p)

with open('mann_whitney_u_test_results.txt', 'w') as f:
    for mood, (stat, p) in results.items():
        result = f"{mood}: Statistics={stat}, p={p}"
        print(result)
        f.write(result + '\n')

