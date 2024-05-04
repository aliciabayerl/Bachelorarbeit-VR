import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Plot average before and after scores of each condition of all mood states

folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)

average_scores = participant_scores.groupby('Condition').mean().drop(columns='Participant')

mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']

bar_width = 0.35

conditions = len(average_scores.index)

x = np.arange(conditions)

fig, axs = plt.subplots(len(mood_states), figsize=(12, 10))

for i, mood_state in enumerate(mood_states):
    before_scores = average_scores[f'Before {mood_state}']
    after_scores = average_scores[f'After {mood_state}']
    
    before_bars = axs[i].bar(x - bar_width/2, before_scores, bar_width, label='Before')
    after_bars = axs[i].bar(x + bar_width/2, after_scores, bar_width, label='After')

    axs[i].set_xlabel('Condition')
    axs[i].set_ylabel('Average Score')
    axs[i].set_title(f'Comparison of Before and After {mood_state} Scores by Condition')
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(average_scores.index)
    axs[i].legend()

plt.tight_layout()

output_image = os.path.join(image_path, 'before_after_bar.png')
plt.savefig(output_image)

plt.show()