import pandas as pd
import os

# Define the folder path and file names
folder_path = 'POMS'
file_path_no_ms = 'DEQ_MS_participant_scores.csv'
file_path_yes_ms = 'DEQ_MSyes_participant_scores.csv'

# Load the data from the CSV files
data_no_ms = pd.read_csv(os.path.join(folder_path, file_path_no_ms))
data_yes_ms = pd.read_csv(os.path.join(folder_path, file_path_yes_ms))

# List of mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Define the conditions
conditions = [0, 1, 2]
condition_labels = {0: 'Condition 0', 1: 'Condition 1', 2: 'Condition 2'}

# Initialize dictionaries to store descriptive statistics for each condition and motion sickness status
descriptive_stats_no_motion_sickness = {cond: {} for cond in conditions}
descriptive_stats_motion_sickness = {cond: {} for cond in conditions}

# Function to calculate descriptive statistics for a given dataset
def calculate_descriptive_stats(data, condition):
    stats = {}
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'

        stats[mood] = {
            'Before Mean': data[data['Condition_x'] == condition][before_col].mean(),
            'Before Median': data[data['Condition_x'] == condition][before_col].median(),
            'Before Std Dev': data[data['Condition_x'] == condition][before_col].std(),
            'Before Min': data[data['Condition_x'] == condition][before_col].min(),
            'Before Max': data[data['Condition_x'] == condition][before_col].max(),
            'Before Q1': data[data['Condition_x'] == condition][before_col].quantile(0.25),
            'Before Q3': data[data['Condition_x'] == condition][before_col].quantile(0.75),
            'Before IQR': data[data['Condition_x'] == condition][before_col].quantile(0.75) - data[data['Condition_x'] == condition][before_col].quantile(0.25),

            'After Mean': data[data['Condition_x'] == condition][after_col].mean(),
            'After Median': data[data['Condition_x'] == condition][after_col].median(),
            'After Std Dev': data[data['Condition_x'] == condition][after_col].std(),
            'After Min': data[data['Condition_x'] == condition][after_col].min(),
            'After Max': data[data['Condition_x'] == condition][after_col].max(),
            'After Q1': data[data['Condition_x'] == condition][after_col].quantile(0.25),
            'After Q3': data[data['Condition_x'] == condition][after_col].quantile(0.75),
            'After IQR': data[data['Condition_x'] == condition][after_col].quantile(0.75) - data[data['Condition_x'] == condition][after_col].quantile(0.25)
        }
    return stats

# Calculate descriptive statistics for No Motion Sickness across all conditions
for cond in conditions:
    descriptive_stats_no_motion_sickness[cond] = calculate_descriptive_stats(data_no_ms, cond)

# Calculate descriptive statistics for Motion Sickness across all conditions
for cond in conditions:
    descriptive_stats_motion_sickness[cond] = calculate_descriptive_stats(data_yes_ms, cond)

# Convert the descriptive statistics dictionaries to DataFrames
def stats_to_dataframe(stats, labels):
    dfs = {}
    for cond, label in labels.items():
        df = pd.DataFrame(stats[cond]).T
        df.columns = [f'{col} ({label})' for col in df.columns]
        dfs[cond] = df
    return dfs

# Convert the statistics to DataFrames
stats_no_motion_sickness_df = stats_to_dataframe(descriptive_stats_no_motion_sickness, condition_labels)
stats_motion_sickness_df = stats_to_dataframe(descriptive_stats_motion_sickness, condition_labels)

# Concatenate data for all conditions
combined_no_ms_df = pd.concat([stats_no_motion_sickness_df[0], stats_no_motion_sickness_df[1], stats_no_motion_sickness_df[2]], axis=1)
combined_yes_ms_df = pd.concat([stats_motion_sickness_df[0], stats_motion_sickness_df[1], stats_motion_sickness_df[2]], axis=1)

# Save the descriptive statistics to CSV files
combined_no_ms_df.to_csv('descriptive_statistics_no_motion_sickness.csv')
combined_yes_ms_df.to_csv('descriptive_statistics_motion_sickness.csv')

# Print the descriptive statistics for both conditions
print("Descriptive Statistics for No Motion Sickness:")
print(combined_no_ms_df)

print("\nDescriptive Statistics for Motion Sickness:")
print(combined_yes_ms_df)
