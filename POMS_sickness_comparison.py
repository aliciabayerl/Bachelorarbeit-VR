import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os



folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'Yes']
no_motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'No']

mood_states = ['Tension', 'Depression', 'Anger', 'Vigor', 'Fatigue', 'Confusion']
data.rename(columns={'After Anger_x': 'After Anger', 'Before Anger_x': 'Before Anger'}, inplace=True)

# Calculate the change in mood states for participants with and without motion sickness
for mood_state in mood_states:
    motion_sickness[f'Change {mood_state}'] = motion_sickness[f'After {mood_state}'] - motion_sickness[f'Before {mood_state}']
    no_motion_sickness[f'Change {mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

avg_change_motion_sickness = motion_sickness[[f'Change {state}' for state in mood_states]].mean()
avg_change_no_motion_sickness = no_motion_sickness[[f'Change {state}' for state in mood_states]].mean()

plt.figure(figsize=(12, 8))
bar_width = 0.35
index = np.arange(len(mood_states)) 

plt.bar(index, avg_change_motion_sickness, bar_width, label='Motion Sickness', color="#4575b4")
plt.bar(index + bar_width, avg_change_no_motion_sickness, bar_width, label='No Motion Sickness', color="#abd9e9")

plt.xlabel('Mood State')
plt.ylabel('Average Change')
#plt.title('Average Change in Mood States for Participants with and without Motion Sickness')
plt.xticks(index + bar_width / 2, mood_states)
plt.legend()
plt.tight_layout()

# Save plot
output_image = os.path.join('POMS/Plot_Images', 'POMS_sickness_comparison_plot.png')
plt.savefig(output_image)

plt.show()

# new csv POMS no motion sickness
columns_to_select = ['Participant', 'Condition_x', 'Before Tension', 'After Tension', 'Before Vigor', 'After Vigor', 
                     'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 
                     'Before Anger', 'After Anger', 'Before Depression', 'After Depression']

participant_scores = no_motion_sickness[columns_to_select]
participant_scores_ms = motion_sickness[columns_to_select]


output_file = 'POMS_MS_participant_scores.csv'
output_path = os.path.join(folder_path, output_file)
participant_scores.to_csv(output_path, index=False)

output_file_ms = 'POMS_MSyes_participant_scores.csv'
output_path_ms = os.path.join(folder_path, output_file_ms)
participant_scores_ms.to_csv(output_path_ms, index=False)
