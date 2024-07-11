import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import os

# Load data
folder_path = 'POMS'
file_path = os.path.join(folder_path, 'questionnaire_with_scores.csv')
data = pd.read_csv(file_path)

# Mapping VR experience levels to numeric values
data['VR_experience'] = data['Please indicate your previous experience with virtual reality:'].map({
    'No prior experience': 0,
    "I've had limited exposure to virtual environment, having tried them once or twice": 1,
    'I engage occasionally with virtual environments': 2,
    'I frequently use virtual reality as part of my activities/work': 3
})

# Convert 'yes/no' motion sickness to binary
data['Motion_Sickness_Binary'] = data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'].apply(lambda x: 1 if x == 'Yes' else 0)

# Calculate correlation
correlation, p_value = spearmanr(data['VR_experience'].dropna(), data['Motion_Sickness_Binary'].dropna())

# Create plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='VR_experience', y='Motion_Sickness_Binary', data=data, palette='coolwarm')
plt.title('Correlation between VR Experience and Motion Sickness')
plt.xlabel('Level of VR Experience')
plt.ylabel('Motion Sickness Binary')
plt.xticks(ticks=[0, 1, 2, 3], labels=['No Experience', 'Limited Exposure', 'Occasional Engagement', 'Frequent Use'])
plt.grid(True)
plt.tight_layout()
plt.show()

print("Spearman correlation coefficient:", correlation)
print("P-value:", p_value)
