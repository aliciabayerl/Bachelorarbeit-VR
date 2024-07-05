import pandas as pd
import os


folder_path = 'POMS'


# Load the data from the CSV files
file_path_no_ms = 'DEQ_MS_participant_scores.csv'
file_path_yes_ms = 'DEQ_MSyes_participant_scores.csv'

data_no_ms = pd.read_csv(os.path.join(folder_path, file_path_no_ms))
data_yes_ms = pd.read_csv(os.path.join(folder_path, file_path_yes_ms))

# List of mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Initialize dictionaries to store descriptive statistics for each condition
descriptive_stats_no_motion_sickness = {}
descriptive_stats_motion_sickness = {}

# Define the conditions
no_motion_sickness_conditions = [0]
motion_sickness_conditions = [1, 2]

# Function to calculate descriptive statistics for a given dataset
def calculate_descriptive_stats(data):
    stats = {}
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'

        stats[mood] = {
            'Before Mean': data[before_col].mean(),
            'Before Median': data[before_col].median(),
            'Before Std Dev': data[before_col].std(),
            'Before Min': data[before_col].min(),
            'Before Max': data[before_col].max(),
            'Before Q1': data[before_col].quantile(0.25),
            'Before Q3': data[before_col].quantile(0.75),
            'Before IQR': data[before_col].quantile(0.75) - data[before_col].quantile(0.25),

            'After Mean': data[after_col].mean(),
            'After Median': data[after_col].median(),
            'After Std Dev': data[after_col].std(),
            'After Min': data[after_col].min(),
            'After Max': data[after_col].max(),
            'After Q1': data[after_col].quantile(0.25),
            'After Q3': data[after_col].quantile(0.75),
            'After IQR': data[after_col].quantile(0.75) - data[after_col].quantile(0.25)
        }
    return stats

# Calculate descriptive statistics for No Motion Sickness
descriptive_stats_no_motion_sickness = calculate_descriptive_stats(data_no_ms)

# Calculate descriptive statistics for Motion Sickness
descriptive_stats_motion_sickness = calculate_descriptive_stats(data_yes_ms)

# Convert the descriptive statistics dictionaries to DataFrames
stats_no_motion_sickness_df = pd.DataFrame(descriptive_stats_no_motion_sickness).T
stats_motion_sickness_df = pd.DataFrame(descriptive_stats_motion_sickness).T

# Print the descriptive statistics for both conditions
print("Descriptive Statistics for No Motion Sickness:")
print(stats_no_motion_sickness_df)

print("\nDescriptive Statistics for Motion Sickness:")
print(stats_motion_sickness_df)

# Optionally, save the descriptive statistics to CSV files
stats_no_motion_sickness_df.to_csv('descriptive_statistics_no_motion_sickness.csv')
stats_motion_sickness_df.to_csv('descriptive_statistics_motion_sickness.csv')

# Display summary statistics for each condition (combined for motion sickness vs no motion sickness)
print("\nSummary Statistics by Condition (No Motion Sickness vs Motion Sickness):")
print(pd.concat([data_no_ms.groupby('Condition_x').describe().T, data_yes_ms.groupby('Condition_x').describe().T], axis=1, keys=['No Motion Sickness', 'Motion Sickness']))
