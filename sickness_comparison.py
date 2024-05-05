import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

folder_path = 'POMS'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'Yes']
no_motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'No']

mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Calculate the change in mood states for participants with and without motion sickness
for mood_state in mood_states:
    motion_sickness[f'Change {mood_state}'] = motion_sickness[f'After {mood_state}'] - motion_sickness[f'Before {mood_state}']
    no_motion_sickness[f'Change {mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

avg_change_motion_sickness = motion_sickness[[f'Change {state}' for state in mood_states]].mean()
avg_change_no_motion_sickness = no_motion_sickness[[f'Change {state}' for state in mood_states]].mean()

plt.figure(figsize=(12, 8))
bar_width = 0.35
index = np.arange(len(mood_states)) 

plt.bar(index, avg_change_motion_sickness, bar_width, label='Motion Sickness')
plt.bar(index + bar_width, avg_change_no_motion_sickness, bar_width, label='No Motion Sickness')

plt.xlabel('Mood State')
plt.ylabel('Average Change')
plt.title('Average Change in Mood States for Participants with and without Motion Sickness')
plt.xticks(index + bar_width / 2, mood_states)
plt.legend()
plt.tight_layout()
plt.show()


