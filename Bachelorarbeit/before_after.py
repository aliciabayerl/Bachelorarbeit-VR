import pandas as pd
import matplotlib.pyplot as plt

# Load the participant scores
participant_scores = pd.read_csv('participant_scores.csv')

# Define the mood states you want to plot
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']

# Set the number of conditions
conditions = participant_scores['Condition'].unique()

# Create a figure and axis for each mood state
fig, axs = plt.subplots(len(mood_states), figsize=(10, 12), sharex=True)

# Iterate through each mood state
for i, mood_state in enumerate(mood_states):
    # Iterate through each condition and plot the before and after scores
    for condition in conditions:
        # Filter the data for the current condition
        condition_data = participant_scores[participant_scores['Condition'] == condition]
        
        # Plot the before scores
        axs[i].plot(condition_data.index, condition_data[f'Before {mood_state}'], label=f'Condition {condition} (Before)')
        
        # Plot the after scores
        axs[i].plot(condition_data.index, condition_data[f'After {mood_state}'], label=f'Condition {condition} (After)')

    # Add labels, title, and legend for each subplot
    axs[i].set_ylabel('Score')
    axs[i].set_title(f'Before and After {mood_state} Scores')
    axs[i].legend()

# Add a common x-axis label
axs[-1].set_xlabel('Participant')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
