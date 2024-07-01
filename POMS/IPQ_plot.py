import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = 'POMS'
ipq_scores_file = os.path.join(folder_path, 'ipq_scores.csv')
ipq_scores = pd.read_csv(ipq_scores_file)

ipq_scores['Overall_Presence'] = ipq_scores[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

print(ipq_scores)

condition_means = ipq_scores.groupby('Condition')[['SP_mean', 'INV_mean', 'REAL_mean', 'Overall_Presence']].mean().reset_index()

melted_data = condition_means.melt(id_vars='Condition', var_name='Presence_Type', value_name='Mean_Score')

plt.figure(figsize=(12, 8))
sns.barplot(x='Condition', y='Mean_Score', hue='Presence_Type', data=melted_data, palette='viridis')
plt.title('Mean Presence Scores by Condition')
plt.xlabel('Condition')
plt.ylabel('Mean Score')
plt.legend(title='Presence Type')
plt.grid(True)

image_path = 'POMS/Plot_Images'
output_image = os.path.join(image_path, 'IPQ_PresencePlot')
plt.tight_layout()
plt.savefig(output_image)
plt.show()
