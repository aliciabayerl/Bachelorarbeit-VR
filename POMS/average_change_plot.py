import pandas as pd
import matplotlib.pyplot as plt
import os

folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)


mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Anger', 'Depression']

# Calculate the change for each mood state from before to after
for mood_state in mood_states:
    participant_scores[f'Change {mood_state}'] = participant_scores[f'After {mood_state}'] - participant_scores[f'Before {mood_state}']

conditions = participant_scores['Condition'].unique()

fig, ax = plt.subplots(figsize=(10, 6))

for condition in conditions:
    condition_data = participant_scores[participant_scores['Condition'] == condition]
    
    x_values = []
    y_values = []
    
    for mood_state in mood_states:
        x_values.append(mood_state)
        y_values.append(condition_data[f'Change {mood_state}'].mean())
    
    # Plot the average change in lines
    ax.plot(x_values, y_values, label=f'Condition {condition}')

ax.set_xlabel('Mood State')
ax.set_ylabel('Average Change')
ax.set_title('Average Change in Mood State Scores by Condition')
ax.legend(title='Condition')

output_image = os.path.join(image_path, 'average_change_plot.png')
plt.savefig(output_image)

plt.show()
