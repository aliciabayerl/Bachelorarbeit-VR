import os
import pandas as pd
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'

participant_scores_file = os.path.join(folder_path, 'participant_scores.csv')
participant_scores = pd.read_csv(participant_scores_file)
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)

participant_scores['Change_Tension'] = participant_scores['After Tension'] - participant_scores['Before Tension']
participant_scores['Change_Vigor'] = participant_scores['After Vigor'] - participant_scores['Before Vigor']
participant_scores['Change_Confusion'] = participant_scores['After Confusion'] - participant_scores['Before Confusion']
participant_scores['Change_Fatigue'] = participant_scores['After Fatigue'] - participant_scores['Before Fatigue']
participant_scores['Change_Anger'] = participant_scores['After Anger_x'] - participant_scores['Before Anger_x']
participant_scores['Change_Depression'] = participant_scores['After Depression'] - participant_scores['Before Depression']

negative_mood_change = participant_scores[['Change_Tension', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']].sum(axis=1)
overall_mood_disturbance = negative_mood_change - participant_scores['Change_Vigor']
participant_scores['Overall_Mood_Disturbance'] = overall_mood_disturbance

merged_data = pd.merge(ipq_scores, participant_scores, on='Participant')

merged_data['Overall_Presence'] = merged_data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

def calculate_correlations(ipq_data, condition_data, ipq_variable):
    correlations = {}
    for variable in ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression', 'Overall_Mood_Disturbance']:
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
