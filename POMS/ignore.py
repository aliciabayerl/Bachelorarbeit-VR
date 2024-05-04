import pandas as pd
import matplotlib.pyplot as plt
import os

# I tried to make them in one plot before and after of all conditions to compare, did not work out as intended :(

folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)

mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']

conditions = participant_scores['Condition'].unique()

fig, axs = plt.subplots(len(mood_states), figsize=(10, 12), sharex=True)

for i, mood_state in enumerate(mood_states):
    for condition in conditions:
        condition_data = participant_scores[participant_scores['Condition'] == condition]
        
        axs[i].plot(condition_data.index, condition_data[f'Before {mood_state}'], label=f'Condition {condition} (Before)')
        
        axs[i].plot(condition_data.index, condition_data[f'After {mood_state}'], label=f'Condition {condition} (After)')

    axs[i].set_ylabel('Score')
    axs[i].set_title(f'Before and After {mood_state} Scores')
    axs[i].legend()

axs[-1].set_xlabel('Participant')

plt.tight_layout()

plt.show()
