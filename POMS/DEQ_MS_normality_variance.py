import pandas as pd
import os
from scipy.stats import shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal


folder_path = 'POMS'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'Yes']
no_motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'No']

mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']


for mood_state in mood_states:
    no_motion_sickness[f'Change_{mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

change_scores = [f'Change_{mood_state}' for mood_state in mood_states]

#Check normality
print("Normality Tests:")
for score in change_scores:
    stat, p_value = shapiro(no_motion_sickness[score])
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'{score} is normally distributed')
    else:
        print(f'{score} is not normally distributed')
    print()

#Check homogeneity of variance
print("Homogeneity of Variance Tests:")
for score in change_scores:
    stat, p_value = levene(no_motion_sickness[no_motion_sickness['Condition_x'] == 0][score],
                           no_motion_sickness[no_motion_sickness['Condition_x'] == 1][score],
                           no_motion_sickness[no_motion_sickness['Condition_x'] == 2][score])
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'Variances for {score} are equal across groups')
    else:
        print(f'Variances for {score} are not equal across groups')
    print()

# Plot histogram
plt.figure(figsize=(14, 10))
for i, score in enumerate(change_scores, 1):
    plt.subplot(2, 4, i)
    sns.histplot(no_motion_sickness[score], kde=True)
    plt.title(f'Distribution of {score}')
    plt.xlabel('Change Score')
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


