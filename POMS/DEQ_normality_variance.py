import pandas as pd
import os
from scipy.stats import shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
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

change_scores = ['Change_Anger', 'Change_Disgust', 'Change_Fear', 'Change_Anxiety', 'Change_Sadness', 'Change_Desire', 'Change_Relaxation', 'Change_Happiness']

# Normality tests
print("Normality Tests:")
for score in change_scores:
    stat, p_value = shapiro(data[score])
    print(f'{score}: Statistics={stat}, p-value={p_value}')
    if p_value > 0.05:
        print(f'{score} is normally distributed')
    else:
        print(f'{score} is not normally distributed')
    print()

# Homogeneity of variance tests
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

# Plot settings for better readability on A4
plt.rcParams.update({'font.size': 14, 'axes.titlesize': 16, 'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 14})

# Distribution plots
plt.figure(figsize=(10.5, 7))  
for i, score in enumerate(change_scores, 1):
    plt.subplot(2, 4, i)
    mood = score.split('_')[1]  
    sns.histplot(data[score], kde=True)
    plt.title(f'Change in {mood}')  
    plt.xlabel('Change Score')
    plt.ylabel('Frequency')

plt.tight_layout()
image_path = 'POMS/Plot_images'
output_image = os.path.join(image_path, 'DEQ_distribution.png')
plt.savefig(output_image, dpi=300)  # High resolution for A4 print
plt.show()

# Boxplots
plt.figure(figsize=(21, 14))  # A4 size in inches
for i, score in enumerate(change_scores, 1):
    plt.subplot(2, 4, i)
    sns.boxplot(x='Condition', y=score, data=data)
    mood = score.split('_')[1]
    plt.title(f'Change in {mood}')
    plt.xlabel('Condition')
    plt.ylabel('Change Score')

plt.tight_layout()
output_image_boxplot = os.path.join(image_path, 'DEQ_Boxplot.png')
plt.savefig(output_image_boxplot, dpi=300)  # High resolution for A4 print
plt.show()
