import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
no_ms_file = os.path.join(folder_path, 'POMS_MS_participant_scores.csv')
ms_file = os.path.join(folder_path, 'POMS_MSyes_participant_scores.csv')

ipq_scores = pd.read_csv(ipq_scores_file)
no_ms_data = pd.read_csv(no_ms_file)
ms_data = pd.read_csv(ms_file)

ipq_scores['Overall_Presence'] = ipq_scores[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

no_ms_participants = no_ms_data['Participant']
ms_participants = ms_data['Participant']

ipq_scores['Group'] = ipq_scores['Participant'].apply(lambda x: 'No Motion Sickness' if x in no_ms_participants.values else ('Motion Sickness' if x in ms_participants.values else 'Unknown'))

ipq_scores = ipq_scores[ipq_scores['Group'] != 'Unknown']

condition_means = ipq_scores.groupby(['Group', 'Condition'])[['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']].mean().reset_index()

print(condition_means.shape)

print(condition_means.head())

melted_data = condition_means.melt(id_vars=['Group', 'Condition'], var_name='Presence_Type', value_name='Mean_Score')

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', None)  
print(melted_data)

pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')
pd.reset_option('display.width')

plt.figure(figsize=(14, 10))

g = sns.FacetGrid(melted_data, col='Group', hue='Presence_Type', col_wrap=2, height=6, aspect=1.5, palette='viridis')
g.map(sns.barplot, 'Condition', 'Mean_Score', order=condition_means['Condition'].unique(), errorbar=None)

g.set_titles('{col_name}')
g.set_axis_labels('Condition', 'Mean Score')
g.add_legend(title='Presence Type')
plt.suptitle('Mean Presence Scores by Condition and Group', y=1.02)

image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'IPQ_PresencePlot_Facet.png')
plt.tight_layout()
plt.savefig(output_image)
plt.show()