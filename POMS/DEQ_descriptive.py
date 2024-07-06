import pandas as pd
import os

# Load the data from the CSV file
folder_path = 'POMS'
participant_scores_file = os.path.join(folder_path, 'participant_scores_deq.csv')
data = pd.read_csv(participant_scores_file)

# List of mood states
mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Initialize a dictionary to store descriptive statistics
descriptive_stats = {}

# Calculate descriptive statistics for each mood state
for mood in mood_states:
    before_col = f'Before {mood}'
    after_col = f'After {mood}'

    descriptive_stats[mood] = {
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

# Convert the descriptive statistics dictionary to a DataFrame
stats_df = pd.DataFrame(descriptive_stats).T

# Save the descriptive statistics to a CSV file
stats_df.to_csv('descriptive_statistics_deq.csv')

# Calculate summary statistics by condition
summary_by_condition = data.groupby('Condition').describe().T

# Save summary statistics by condition to a CSV file
summary_by_condition.to_csv('summary_statistics_by_condition.csv')

# Print the descriptive statistics and summary statistics by condition
print("Descriptive Statistics:")
print(stats_df)
print("\nSummary Statistics by Condition:")
print(summary_by_condition)
