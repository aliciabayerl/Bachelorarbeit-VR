import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import os

# Load the data
folder_path = 'POMS'
input_file = 'POMS_MS_participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Calculate mood state changes
data['Change_Tension'] = data['After Tension'] - data['Before Tension']
data['Change_Vigor'] = data['After Vigor'] - data['Before Vigor']
data['Change_Confusion'] = data['After Confusion'] - data['Before Confusion']
data['Change_Fatigue'] = data['After Fatigue'] - data['Before Fatigue']
data['Change_Anger'] = data['After Anger_x'] - data['Before Anger_x']
data['Change_Depression'] = data['After Depression'] - data['Before Depression']

# Split data by condition
condition_1 = data[data['Condition_x'] == 1]
condition_2 = data[data['Condition_x'] == 2]
condition_3 = data[data['Condition_x'] == 0]

# Calculate descriptive statistics
desc_stats_1 = condition_1.describe()
desc_stats_2 = condition_2.describe()
desc_stats_3 = condition_3.describe()


print("Condition 1 Descriptive Statistics:\n", desc_stats_1)
print("Condition 2 Descriptive Statistics:\n", desc_stats_2)
print("Condition 2 Descriptive Statistics:\n", desc_stats_3)


# List of mood states
mood_states = ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']

# Generate box plots in a single image
plt.figure(figsize=(15, 20))
for i, mood in enumerate(mood_states, start=1):
    plt.subplot(3, 2, i)
    sns.boxplot(x='Condition_x', y=mood, data=data)
    plt.title(f'Change in {mood} by Condition')

plt.tight_layout()
plt.savefig('MS_mood_changes_boxplots.png')
plt.close()

# Perform Mann-Whitney U Test for each mood state
results = {}
for mood in mood_states:
    stat, p = mannwhitneyu(condition_1[mood], condition_2[mood])
    results[mood] = (stat, p)

# Print and save Mann-Whitney U Test results
with open('MS_mann_whitney_u_test_results.txt', 'w') as f:
    for mood, (stat, p) in results.items():
        result = f"{mood}: Statistics={stat}, p={p}"
        print(result)
        f.write(result + '\n')

