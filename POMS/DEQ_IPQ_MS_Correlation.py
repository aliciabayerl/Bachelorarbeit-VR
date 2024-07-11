import pandas as pd
from scipy.stats import pointbiserialr, spearmanr
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
folder_path = 'POMS'
file_path = os.path.join(folder_path, 'questionnaire_with_scores.csv')
data = pd.read_csv(file_path)

# Load IPQ scores
ipq_file_path = os.path.join(folder_path, 'IPQ_scores.csv')
ipq_data = pd.read_csv(ipq_file_path)

# Combine datasets assuming 'Participant' is a common key
combined_data = pd.merge(data, ipq_data, on='Participant')
combined_data['Overall_Presence'] = combined_data[['SP_mean', 'INV_mean', 'REAL_mean']].mean(axis=1)

# Convert 'yes/no' to binary and handle missing values
combined_data['Motion_Sickness_Binary'] = combined_data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'].apply(lambda x: 1 if x == 'Yes' else 0)
combined_data['Please indicate how much this affected your overall experience.'].fillna(0, inplace=True)

# Calculate correlations
point_biserial_corr = pointbiserialr(combined_data['Overall_Presence'], combined_data['Motion_Sickness_Binary'])
spearman_corr = spearmanr(combined_data['Overall_Presence'], combined_data['Please indicate how much this affected your overall experience.'])

print(f"Point-biserial Correlation between Overall Presence and Motion Sickness Experience: r={point_biserial_corr.correlation:.3f}, p-value={point_biserial_corr.pvalue:.4f}")
print(f"Spearman Correlation between Overall Presence and Motion Sickness Degree: rho={spearman_corr.correlation:.3f}, p-value={spearman_corr.pvalue:.4f}")

# Create the scatter plot for participants who experienced motion sickness
motion_sickness_affected = combined_data[combined_data['Motion_Sickness_Binary'] == 1]
plt.figure(figsize=(10, 6))
sns.regplot(x='Overall_Presence', y='Please indicate how much this affected your overall experience.', data=motion_sickness_affected, scatter_kws={'alpha':0.5})

plt.title('Correlation between Overall Presence and Degree of Motion Sickness')
plt.xlabel('Overall Presence Score')
plt.ylabel('Degree of Motion Sickness Impact')
plt.grid(True)
plt.show()
