import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

## DEQ 
folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'questionnaire_with_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'Yes']
no_motion_sickness = data[data['Did you experience any discomfort or adverse effects (physical or emotional, like nausea/dizziness due to motion sickness) during or after the virtual reality experience?'] == 'No']

motion_sickness_counts = motion_sickness.groupby('Condition_x').size()
total_people_in_condition = data.groupby('Condition_x').size()

motion_sickness_percentage = (motion_sickness_counts / total_people_in_condition) * 100

print("Percentage of people with motion sickness in each condition:")
print(motion_sickness_percentage)

mood_states = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Calculate the change in mood states for participants with and without motion sickness
for mood_state in mood_states:
    motion_sickness[f'Change {mood_state}'] = motion_sickness[f'After {mood_state}'] - motion_sickness[f'Before {mood_state}']
    no_motion_sickness[f'Change {mood_state}'] = no_motion_sickness[f'After {mood_state}'] - no_motion_sickness[f'Before {mood_state}']

avg_change_motion_sickness = motion_sickness[[f'Change {state}' for state in mood_states]].mean()
avg_change_no_motion_sickness = no_motion_sickness[[f'Change {state}' for state in mood_states]].mean()

plt.figure(figsize=(12, 8))
plt.figure(figsize=(6, 4))  # Adjust figure size to be smaller
plt.rc('axes', labelsize=10)  # Fontsize of the x and y labels
plt.rc('xtick', labelsize=9)  # Fontsize of the x tick labels
plt.rc('ytick', labelsize=9)  # Fontsize of the y tick labels
plt.rc('legend', fontsize=9)  # Fontsize of the legend
plt.rc('font', family='sans-serif')  # Use a sans-serif font
plt.rc('font', **{'sans-serif': 'Arial'})  # Specifically use Arial

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
output_image = os.path.join('POMS/Plot_Images', 'DEQ_sickness_comparison_plot.png')
plt.savefig(output_image)

plt.show()

# new csv POMS no motion sickness
columns_to_select = ['Participant', 'Condition_x', 'Before Anger', 'After Anger', 'Before Disgust', 'After Disgust', 
                     'Before Fear', 'After Fear', 'Before Anxiety', 'After Anxiety', 
                     'Before Sadness', 'After Sadness', 'Before Desire', 'After Desire', 'Before Relaxation', 'After Relaxation', 'Before Happiness', 'After Happiness']

participant_scores = no_motion_sickness[columns_to_select]
participant_scores_ms = motion_sickness[columns_to_select]

output_file = 'DEQ_MS_participant_scores.csv'
output_path = os.path.join(folder_path, output_file)
participant_scores.to_csv(output_path, index=False)

output_file_ms = 'DEQ_MSyes_participant_scores.csv'
output_path_ms = os.path.join(folder_path, output_file_ms)
participant_scores_ms.to_csv(output_path_ms, index=False)
