import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
no_ms_file = os.path.join(folder_path, 'POMS_MS_participant_scores.csv')
ms_file = os.path.join(folder_path, 'POMS_MSyes_participant_scores.csv')

# Load data
ipq_scores = pd.read_csv(ipq_scores_file)
no_ms_data = pd.read_csv(no_ms_file)
ms_data = pd.read_csv(ms_file)

# Calculate overall presence score
ipq_scores['Overall_Presence'] = ipq_scores[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

# Identify participants in each group
no_ms_participants = no_ms_data['Participant']
ms_participants = ms_data['Participant']

# Add group labels based on participant IDs
ipq_scores['Group'] = ipq_scores['Participant'].apply(lambda x: 'No Motion Sickness' if x in no_ms_participants.values else ('Motion Sickness' if x in ms_participants.values else 'Unknown'))

# Filter out participants that are not in either group
ipq_scores = ipq_scores[ipq_scores['Group'] != 'Unknown']

# Compute mean presence scores for each condition and group
condition_means = ipq_scores.groupby(['Group', 'Condition'])[['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']].mean().reset_index()

# Print the shape to verify the number of rows
print(condition_means.shape)

# Print a sample of the data to ensure it looks correct
print(condition_means.head())

# Melt the data for plotting
melted_data = condition_means.melt(id_vars=['Group', 'Condition'], var_name='Presence_Type', value_name='Mean_Score')

# Print the entire melted data to check if it includes all participants and conditions
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Set width to display all columns
print(melted_data)

# Optional: Reset options to default after printing
pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')
pd.reset_option('display.width')

# Create a FacetGrid to separate the groups
plt.figure(figsize=(14, 10))

g = sns.FacetGrid(melted_data, col='Group', hue='Presence_Type', col_wrap=2, height=6, aspect=1.5, palette='viridis')
g.map(sns.barplot, 'Condition', 'Mean_Score', order=condition_means['Condition'].unique(), errorbar=None)

# Add titles and labels
g.set_titles('{col_name}')
g.set_axis_labels('Condition', 'Mean Score')
g.add_legend(title='Presence Type')
plt.suptitle('Mean Presence Scores by Condition and Group', y=1.02)

# Save the plot
image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'IPQ_PresencePlot_Facet.png')
plt.tight_layout()
plt.savefig(output_image)
plt.show()