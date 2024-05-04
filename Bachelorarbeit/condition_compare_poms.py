import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the participant scores
participant_scores = pd.read_csv('participant_scores.csv')

# Exclude the 'Participant' column from the average calculation
average_scores = participant_scores.groupby('Condition').mean().drop(columns='Participant')

# Define the mood states you want to plot
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']

# Set the width of the bars
bar_width = 0.35

# Set the number of conditions
conditions = len(average_scores.index)

# Set the position of the bars on the x-axis
x = np.arange(conditions)

# Create a figure and subplots
fig, axs = plt.subplots(len(mood_states), figsize=(12, 10))

# Iterate through each mood state and create a subplot
for i, mood_state in enumerate(mood_states):
    # Get the before and after scores for the selected mood state
    before_scores = average_scores[f'Before {mood_state}']
    after_scores = average_scores[f'After {mood_state}']
    
    # Plot the before and after scores
    before_bars = axs[i].bar(x - bar_width/2, before_scores, bar_width, label='Before')
    after_bars = axs[i].bar(x + bar_width/2, after_scores, bar_width, label='After')

    # Add labels, title, and legend
    axs[i].set_xlabel('Condition')
    axs[i].set_ylabel('Average Score')
    axs[i].set_title(f'Comparison of Before and After {mood_state} Scores by Condition')
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(average_scores.index)
    axs[i].legend()

# Adjust layout
plt.tight_layout()

# Save the plot as an image
plt.savefig('before_after_comparison.png')

# Show the plot
plt.show()