import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the participant scores CSV file into a pandas DataFrame
participant_scores = pd.read_csv('participant_scores.csv')

# Exclude the first column (presumably participant ID or name)
participant_scores = participant_scores.iloc[:, 1:]

# Calculate the mean scores for each mood state
mean_scores = participant_scores.mean().reset_index()

# Melt the DataFrame to make it suitable for plotting
melted_scores = mean_scores.melt(id_vars=['index'], var_name='Time', value_name='Mean Score')

# Plot the average mood states before and after
plt.figure(figsize=(12, 8))
sns.barplot(x='index', y='Mean Score', hue='Time', data=melted_scores)
plt.title('Average Mood States Before and After')
plt.xlabel('Mood State')
plt.ylabel('Mean Score')
plt.xticks(rotation=45)
plt.legend(title='Time', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

