import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
no_ms_file = os.path.join(folder_path, 'DEQ_MS_participant_scores.csv')
ms_file = os.path.join(folder_path, 'DEQ_MSyes_participant_scores.csv')

ipq_scores = pd.read_csv(ipq_scores_file)
no_ms_data = pd.read_csv(no_ms_file)
ms_data = pd.read_csv(ms_file)

# Calculate the overall presence
ipq_scores['Overall_Presence'] = ipq_scores[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

# Determine if participants belong to the motion sickness group or not
no_ms_participants = no_ms_data['Participant'].unique()
ms_participants = ms_data['Participant'].unique()

ipq_scores['Group'] = ipq_scores['Participant'].apply(lambda x: 'No Motion Sickness' if x in no_ms_participants else ('Motion Sickness' if x in ms_participants else 'Unknown'))
ipq_scores = ipq_scores[ipq_scores['Group'] != 'Unknown']

# Group the data and prepare for plotting
condition_means = ipq_scores.groupby(['Group', 'Condition'])[['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']].mean().reset_index()
melted_data = condition_means.melt(id_vars=['Group', 'Condition'], var_name='Presence_Type', value_name='Mean_Score')

# Customize the plot
plt.figure(figsize=(14, 10))
palette = {"SP_mean": "#74add1", "INV_mean": "#4575b4", "REAL_mean": "#313695", "Overall_Presence": "#800080"}  # Purple for 'Overall_Presence'

g = sns.FacetGrid(melted_data, col='Group', hue='Presence_Type', col_wrap=2, height=6, aspect=1.5, palette=palette)
g.map(sns.barplot, 'Condition', 'Mean_Score', order=condition_means['Condition'].unique())

g.set_titles('{col_name}')
g.set_axis_labels('Condition', 'Mean Score')
g.add_legend(title='Presence Type')

plt.suptitle('Mean Presence Scores by Condition and Group', y=1.02)

# Save the plot
image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'IPQ_PresencePlot_Facet_Updated.png')
plt.tight_layout()
plt.savefig(output_image)
plt.show()
