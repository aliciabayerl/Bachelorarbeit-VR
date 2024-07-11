import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up your data directory and file paths
folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'IPQ_scores.csv')
participant_scores_file = os.path.join(folder_path, 'participant_scores_deq.csv')

# Load the data
ipq_data = pd.read_csv(ipq_scores_file)
participant_data = pd.read_csv(participant_scores_file)

# Calculate Overall Presence from IPQ data
ipq_data['Overall_Presence'] = ipq_data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

# Define the DEQ mood states to calculate changes
deq_mood_states = [
    'Tension', 'Vigor', 'Confusion', 'Fatigue', 
    'Anger', 'Depression', 'Disgust', 'Fear', 
    'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness'
]

# Calculate change scores for each mood state
for mood in deq_mood_states:
    before_col = f'Before_{mood}'
    after_col = f'After_{mood}'
    if before_col in participant_data.columns and after_col in participant_data.columns:
        participant_data[f'Change_{mood}'] = participant_data[after_col] - participant_data[before_col]

# Merge the IPQ data with participant data
combined_data = pd.merge(participant_data, ipq_data[['Participant', 'Overall_Presence']], on='Participant')

# Calculate Spearman correlations for change scores
correlation_results = {}
for mood in deq_mood_states:
    change_col = f'Change_{mood}'
    if change_col in combined_data.columns:
        correlation_results[mood] = combined_data['Overall_Presence'].corr(combined_data[change_col], method='spearman')

# Convert the correlation results to a DataFrame for visualization
correlation_df = pd.DataFrame(list(correlation_results.items()), columns=['Mood State', 'Correlation'])

