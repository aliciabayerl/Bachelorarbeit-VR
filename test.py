import pandas as pd
import os

# Define the folder path and file names
folder_path = 'POMS'
file_path_no_ms = os.path.join(folder_path, 'DEQ_MS_participant_scores.csv')
file_path_yes_ms = os.path.join(folder_path, 'DEQ_MSyes_participant_scores.csv')

# Load the data from the CSV files
data_no_ms = pd.read_csv(file_path_no_ms)
data_yes_ms = pd.read_csv(file_path_yes_ms)

# List of mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Function to calculate median and IQR for a given dataset
def calculate_median_iqr(data, condition):
    results = {}
    for mood in mood_states:
        before_col = f'Before {mood}'
        after_col = f'After {mood}'
        results[mood] = {
            'Before Median': data[before_col].median(),
            'Before IQR': data[before_col].quantile(0.75) - data[before_col].quantile(0.25),
            'After Median': data[after_col].median(),
            'After IQR': data[after_col].quantile(0.75) - data[after_col].quantile(0.25)
        }
    return results

# Gather stats across all conditions for participants with and without motion sickness
combined_stats_no_ms = calculate_median_iqr(data_no_ms, 'No MS')
combined_stats_yes_ms = calculate_median_iqr(data_yes_ms, 'Yes MS')

# Convert the combined stats to DataFrame
combined_stats_no_ms_df = pd.DataFrame(combined_stats_no_ms).T
combined_stats_yes_ms_df = pd.DataFrame(combined_stats_yes_ms).T

# Concatenate the two DataFrames for easy comparison
combined_stats_df = pd.concat([combined_stats_no_ms_df.add_suffix(' (No MS)'), 
                               combined_stats_yes_ms_df.add_suffix(' (Yes MS)')], axis=1)

# Save the combined statistics to a CSV file
combined_stats_df.to_csv('combined_median_iqr_motion_sickness.csv')

# Print the combined statistics
print("Combined Median and IQR for Motion Sickness and No Motion Sickness:")
print(combined_stats_df)
