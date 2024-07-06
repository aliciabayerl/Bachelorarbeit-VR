import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt

# Plot average before and after mood of all conditions

folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
image_path = 'POMS/Plot_Images'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)

participant_scores = participant_scores.iloc[:, 2:]

mean_scores = participant_scores.mean().reset_index()

melted_scores = mean_scores.melt(id_vars=['index'], var_name='Time', value_name='Mean Score')

plt.figure(figsize=(12, 8))
sns.barplot(x='index', y='Mean Score', data=melted_scores)
plt.title('Average Mood States Before and After')
plt.xlabel('Mood State')
plt.ylabel('Mean Score')
plt.xticks(rotation=45)
plt.tight_layout()

output_image = os.path.join(image_path, 'DEQ_all_conditions_plot.png')
plt.savefig(output_image)

plt.show()