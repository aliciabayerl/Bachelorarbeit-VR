import os
import pandas as pd
from scipy.stats import pearsonr

folder_path = 'POMS'

ipq_scores_file = os.path.join(folder_path, 'IPQ_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)
ipq_scores['Participant'] = participant_scores['Participant']

conditions = {}
for i in range(3):  # assuming there are 3 conditions: condition_0.csv, condition_1.csv, condition_2.csv
    condition_file = f'condition_{i}.csv'
    conditions[i] = pd.read_csv(condition_file)

# Function to calculate correlations
def calculate_correlations(ipq_data, condition_data):
    correlations = {}
    for variable in ['Change_Tension', 'Change_Vigor', 'Change_Confusion', 'Change_Fatigue', 'Change_Anger', 'Change_Depression']:
        corr, _ = pearsonr(ipq_data['SP_mean'], condition_data[variable])
        correlations[variable] = corr
    return correlations

# Iterate over conditions
for condition_id, condition_data in conditions.items():
    # Merge IPQ_scores.csv with condition_data based on 'Condition' column
    merged_data = pd.merge(ipq_scores[ipq_scores['Condition'] == condition_id], condition_data, on='Participant')
    
    # Calculate correlations
    correlations = calculate_correlations(merged_data, condition_data)
    
    # Output correlations for each condition
    print(f"\nCorrelations for Condition {condition_id}:")
    for variable, corr in correlations.items():
        print(f"Pearson correlation between SP_mean and {variable}: {corr:.3f}")
