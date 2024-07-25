import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define the plotting parameters for consistency
plt.rcParams.update({
    'axes.labelsize': 14,   # Fontsize of the x and y labels
    'xtick.labelsize': 14,  # Fontsize of the x tick labels
    'ytick.labelsize': 14,  # Fontsize of the y tick labels
    'legend.fontsize': 14,  # Fontsize of the legend
    'font.family': 'sans-serif',
    'font.sans-serif': 'Arial'
})

# Plot 1: Mood States for DEQ
folder_path = 'POMS'
image_path = 'POMS/Plot_Images'
input_file = 'participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
participant_scores = pd.read_csv(file_path)

mood_states_deq = ['Tension', 'Depression', 'Anger', 'Vigor', 'Fatigue', 'Confusion']
participant_scores.rename(columns={'After Anger_x': 'After Anger', 'Before Anger_x': 'Before Anger'}, inplace=True)

# Calculate the overall average scores before and after the intervention
overall_average_before_deq = participant_scores[[f'Before {mood}' for mood in mood_states_deq]].mean()
overall_average_after_deq = participant_scores[[f'After {mood}' for mood in mood_states_deq]].mean()

# Plot 2: Mood States for POMS
input_file_deq = 'participant_scores_deq.csv'
file_path_deq = os.path.join(folder_path, input_file_deq)
participant_scores_deq = pd.read_csv(file_path_deq)

mood_states_poms = ['Anger', 'Disgust', 'Fear', 'Anxiety', 'Sadness', 'Desire', 'Relaxation', 'Happiness']

# Calculate the overall average scores before and after the intervention
overall_average_before_poms = participant_scores_deq[[f'Before {mood}' for mood in mood_states_poms]].mean()
overall_average_after_poms = participant_scores_deq[[f'After {mood}' for mood in mood_states_poms]].mean()

# Create the subplots
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(9, 6))  # Increase width to fit both plots
# Plot 1
x1 = np.arange(len(mood_states_deq))
bar_width = 0.35

before_bars_deq = ax1.bar(x1 - bar_width/2, overall_average_before_deq, bar_width, label='Before', color='#abd9e9')
after_bars_deq = ax1.bar(x1 + bar_width/2, overall_average_after_deq, bar_width, label='After', color='#4575b4')

ax1.set_xlabel('Mood State')
ax1.set_ylabel('Average Score')
ax1.set_xticks(x1)
ax1.set_xticklabels(mood_states_deq, rotation=45, ha='right')
ax1.legend(loc='upper left')
#ax1.set_title('DEQ: Mood States Before and After Intervention')

# Annotate bars with values
for before_bar, after_bar in zip(before_bars_deq, after_bars_deq):
    before_yval = before_bar.get_height()
    after_yval = after_bar.get_height()
    before_xloc = before_bar.get_x() + before_bar.get_width() / 2 - 0.05# Move left bar text slightly left
    after_xloc = after_bar.get_x() + after_bar.get_width() / 2  + 0.05 # Move right bar text slightly right
    ax1.text(before_xloc, before_yval + 0.05, f'{before_yval:.1f}', ha='center', va='bottom', fontsize=11, color='black')
    ax1.text(after_xloc, after_yval + 0.05, f'{after_yval:.1f}', ha='center', va='bottom', fontsize=11, color='black')

# Plot 2
x2 = np.arange(len(mood_states_poms))
before_bars_poms = ax2.bar(x2 - bar_width/2, overall_average_before_poms, bar_width, label='Before', color='#abd9e9')
after_bars_poms = ax2.bar(x2 + bar_width/2, overall_average_after_poms, bar_width, label='After', color='#4575b4')

ax2.set_xlabel('Mood State')
ax2.set_ylabel('Average Score')
ax2.set_xticks(x2)
ax2.set_xticklabels(mood_states_poms, rotation=45, ha='right')
ax2.legend(loc='upper left')
#ax2.set_title('POMS: Mood States Before and After Intervention')

# Annotate bars with values
for before_bar, after_bar in zip(before_bars_poms, after_bars_poms):
    before_yval = before_bar.get_height()
    after_yval = after_bar.get_height()
    before_xloc = before_bar.get_x() + before_bar.get_width() / 2 - 0.15  # Move left bar text slightly left
    after_xloc = after_bar.get_x() + after_bar.get_width() / 2 + 0.1  # Move right bar text slightly right
    ax2.text(before_xloc, before_yval + 0.05, f'{before_yval:.1f}', ha='center', va='bottom', fontsize=11, color='black')
    ax2.text(after_xloc, after_yval + 0.05, f'{after_yval:.1f}', ha='center', va='bottom', fontsize=11, color='black')

# Adjust layout and save the plot
plt.tight_layout()
output_image = os.path.join(image_path, 'Mood_States_Comparison.png')
plt.savefig(output_image, dpi=300)
plt.show()