import os
import pandas as pd
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'

participant_scores_file = os.path.join(folder_path, 'DEQ_MS_participant_scores.csv')
data = pd.read_csv(participant_scores_file)
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)

print(data.columns)
print(ipq_scores.columns)

data['Change_Anger'] = data['After Anger'] - data['Before Anger']
data['Change_Disgust'] = data['After Disgust'] - data['Before Disgust']
data['Change_Fear'] = data['After Fear'] - data['Before Fear']
data['Change_Anxiety'] = data['After Anxiety'] - data['Before Anxiety']
data['Change_Sadness'] = data['After Sadness'] - data['Before Sadness']
data['Change_Desire'] = data['After Desire'] - data['Before Desire']
data['Change_Relaxation'] = data['After Relaxation'] - data['Before Relaxation']
data['Change_Happiness'] = data['After Happiness'] - data['Before Happiness']


change_scores = ['Change_Anger', 'Change_Disgust', 'Change_Fear', 'Change_Anxiety', 'Change_Sadness', 'Change_Desire', 'Change_Relaxation', 'Change_Happiness']



negative_mood_change = data[['Change_Anger', 'Change_Disgust', 'Change_Fear', 'Change_Anxiety', 'Change_Sadness', 'Change_Desire']].sum(axis=1)

merged_data = pd.merge(ipq_scores, data, on='Participant')
print(merged_data.columns)
merged_data['Overall_Presence'] = merged_data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

def calculate_correlations(ipq_data, condition_data, ipq_variable):
    correlations = {}
    for variable in ['Change_Anger', 'Change_Disgust', 'Change_Fear', 'Change_Anxiety', 'Change_Sadness', 'Change_Desire', 'Change_Relaxation', 'Change_Happiness']:
        corr, _ = spearmanr(ipq_data[ipq_variable], condition_data[variable])
        correlations[variable] = corr
    return correlations

def plot_presence_by_condition(data):
    plt.figure(figsize=(10, 6))
    
    condition_means = data.groupby('Condition_x')['Overall_Presence'].mean().reset_index()
    
    # Plotting the bar plot
    sns.barplot(x='Condition_x', y='Overall_Presence', data=condition_means, palette='viridis')
    plt.title('Average Overall Sense of Presence by Condition')
    plt.xlabel('Condition')
    plt.ylabel('Average Overall Sense of Presence')
    plt.grid(True)
    plt.show()

plot_presence_by_condition(merged_data)

ipq_variables = ['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']
correlations_dict = {}

for ipq_variable in ipq_variables:
    correlations = calculate_correlations(merged_data, merged_data, ipq_variable)
    title = f"Correlations with {ipq_variable}"
    correlations_dict[ipq_variable] = correlations
    
    print(f"\n{title}:")
    for variable, corr in correlations.items():
        print(f"Spearman correlation between {ipq_variable} and {variable}: {corr:.3f}")

