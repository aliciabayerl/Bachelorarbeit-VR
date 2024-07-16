import pandas as pd
import os

# Define the folder path and file names
folder_path = 'POMS'
output_folder_path = os.path.join(folder_path, 'DEQ_descriptive_folder')
os.makedirs(output_folder_path, exist_ok=True)

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

# Initialize dictionaries to store descriptive statistics
descriptive_stats_no_motion_sickness = {cond: {} for cond in conditions}
descriptive_stats_motion_sickness = {cond: {} for cond in conditions}
descriptive_stats_combined_conditions_no_ms = {}
descriptive_stats_combined_conditions_ms = {}
descriptive_stats_all_conditions_no_ms = {}
descriptive_stats_all_conditions_ms = {}

# Function to calculate descriptive statistics for a given dataset
def calculate_descriptive_stats(data, condition=None):
    stats = {}
    if condition is not None:
        data = data[data['Condition_x'] == condition]
    
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

# Calculate descriptive statistics for each condition separately
for cond in conditions:
    descriptive_stats_no_motion_sickness[cond] = calculate_descriptive_stats(data_no_ms, cond)
    descriptive_stats_motion_sickness[cond] = calculate_descriptive_stats(data_yes_ms, cond)

# Calculate descriptive statistics for combined conditions (1 and 2)
combined_conditions = [1, 2]
data_no_ms_combined = data_no_ms[data_no_ms['Condition_x'].isin(combined_conditions)]
data_yes_ms_combined = data_yes_ms[data_yes_ms['Condition_x'].isin(combined_conditions)]
descriptive_stats_combined_conditions_no_ms = calculate_descriptive_stats(data_no_ms_combined)
descriptive_stats_combined_conditions_ms = calculate_descriptive_stats(data_yes_ms_combined)

# Calculate descriptive statistics for all conditions combined
descriptive_stats_all_conditions_no_ms = calculate_descriptive_stats(data_no_ms)
descriptive_stats_all_conditions_ms = calculate_descriptive_stats(data_yes_ms)

# Convert the descriptive statistics dictionaries to DataFrames
def stats_to_dataframe(stats, labels=None):
    df = pd.DataFrame(stats).T
    if labels:
        df.columns = [f'{col} ({labels})' for col in df.columns]
    return df

# Convert the statistics to DataFrames
stats_no_motion_sickness_df = {cond: stats_to_dataframe(descriptive_stats_no_motion_sickness[cond], condition_labels[cond]) for cond in conditions}
stats_motion_sickness_df = {cond: stats_to_dataframe(descriptive_stats_motion_sickness[cond], condition_labels[cond]) for cond in conditions}

# Convert combined conditions and all conditions statistics to DataFrames
combined_conditions_no_ms_df = stats_to_dataframe(descriptive_stats_combined_conditions_no_ms, 'Conditions 1+2 Combined')
combined_conditions_ms_df = stats_to_dataframe(descriptive_stats_combined_conditions_ms, 'Conditions 1+2 Combined')
all_conditions_no_ms_df = stats_to_dataframe(descriptive_stats_all_conditions_no_ms, 'All Conditions')
all_conditions_ms_df = stats_to_dataframe(descriptive_stats_all_conditions_ms, 'All Conditions')

# Concatenate data for all conditions
combined_no_ms_df = pd.concat([stats_no_motion_sickness_df[0], stats_no_motion_sickness_df[1], stats_no_motion_sickness_df[2]], axis=1)
combined_yes_ms_df = pd.concat([stats_motion_sickness_df[0], stats_motion_sickness_df[1], stats_motion_sickness_df[2]], axis=1)

# Save the descriptive statistics to CSV files
combined_no_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_no_motion_sickness_by_condition.csv'))
combined_yes_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_motion_sickness_by_condition.csv'))
combined_conditions_no_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_no_motion_sickness_combined_conditions.csv'))
combined_conditions_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_motion_sickness_combined_conditions.csv'))
all_conditions_no_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_no_motion_sickness_all_conditions.csv'))
all_conditions_ms_df.to_csv(os.path.join(output_folder_path, 'descriptive_statistics_motion_sickness_all_conditions.csv'))

# Print the descriptive statistics for both conditions
print("Descriptive Statistics for No Motion Sickness by Condition:")
print(combined_no_ms_df)

print("\nDescriptive Statistics for Motion Sickness by Condition:")
print(combined_yes_ms_df)

print("\nDescriptive Statistics for No Motion Sickness for Combined Conditions 1+2:")
print(combined_conditions_no_ms_df)

print("\nDescriptive Statistics for Motion Sickness for Combined Conditions 1+2:")
print(combined_conditions_ms_df)

print("\nDescriptive Statistics for No Motion Sickness for All Conditions:")
print(all_conditions_no_ms_df)

print("\nDescriptive Statistics for Motion Sickness for All Conditions:")
print(all_conditions_ms_df)
