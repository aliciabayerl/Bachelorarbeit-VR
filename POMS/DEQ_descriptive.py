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

# Print the descriptive statistics
print(stats_df)

stats_df.to_csv('descriptive_statistics_deq.csv')


# Display summary statistics for each condition
print("\nSummary Statistics by Condition:")
print(data.groupby('Condition').describe().T)
