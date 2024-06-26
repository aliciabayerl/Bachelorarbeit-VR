import pandas as pd
import os
from scipy.stats import shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal



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

# Check for normality
change_scores = ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']

print("Normality Tests:")
for score in change_scores:
    stat, p_value = shapiro(data[score])
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'{score} is normally distributed')
    else:
        print(f'{score} is not normally distributed')
    print()

# Check for homogeneity of variance
print("Homogeneity of Variance Tests:")
for score in change_scores:
    stat, p_value = levene(data[data['Condition'] == 0][score],
                           data[data['Condition'] == 1][score],
                           data[data['Condition'] == 2][score])
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'Variances for {score} are equal across groups')
    else:
        print(f'Variances for {score} are not equal across groups')
    print()

# Plot 
plt.figure(figsize=(14, 10))
for i, score in enumerate(change_scores, 1):
    plt.subplot(2, 3, i)
    sns.histplot(data[score], kde=True)
    plt.title(f'Distribution of {score}')
    plt.xlabel('Change Score')
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


