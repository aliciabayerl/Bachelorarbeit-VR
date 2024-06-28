import os
import pandas as pd
from scipy.stats import pearsonr

folder_path = 'POMS'

# Load participant scores
participant_scores_file = os.path.join(folder_path, 'participant_scores.csv')
participant_scores = pd.read_csv(participant_scores_file)
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)

# Calculate change scores
participant_scores['Change_Tension'] = participant_scores['After Tension'] - participant_scores['Before Tension']
participant_scores['Change_Vigor'] = participant_scores['After Vigor'] - participant_scores['Before Vigor']
participant_scores['Change_Confusion'] = participant_scores['After Confusion'] - participant_scores['Before Confusion']
participant_scores['Change_Fatigue'] = participant_scores['After Fatigue'] - participant_scores['Before Fatigue']
participant_scores['Change_Anger'] = participant_scores['After Anger_x'] - participant_scores['Before Anger_x']
participant_scores['Change_Depression'] = participant_scores['After Depression'] - participant_scores['Before Depression']

# Merge on 'Participant' column if correlating with SP_mean
merged_data = pd.merge(ipq_scores, participant_scores, on='Participant')
print(merged_data)

# Function to calculate correlations
def calculate_correlations(ipq_data, condition_data):
    correlations = {}
    for variable in ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']:
        corr, _ = pearsonr(ipq_data['SP_mean'], condition_data[variable])
        correlations[variable] = corr
    return correlations

# Example correlation calculation for each condition (assuming 'Condition' column exists)
conditions = merged_data['Condition_x'].unique()

for condition_id in conditions:
    condition_data = merged_data[merged_data['Condition_x'] == condition_id]
    
    correlations = calculate_correlations(condition_data, condition_data)
    
    print(f"\nCorrelations for Condition {condition_id}:")
    for variable, corr in correlations.items():
        print(f"Pearson correlation between SP_mean and {variable}: {corr:.3f}")
