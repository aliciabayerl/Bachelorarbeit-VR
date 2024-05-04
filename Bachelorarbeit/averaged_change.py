import pandas as pd
import matplotlib.pyplot as plt

# Load the participant scores
participant_scores = pd.read_csv('participant_scores.csv')

# Define the mood states you want to plot
mood_states = ['Tension', 'Vigor', 'Confusion', 'Fatigue', 'Depression']

# Calculate the change for each mood state
for mood_state in mood_states:
    # Calculate the change from before to after for each participant
    participant_scores[f'Change {mood_state}'] = participant_scores[f'After {mood_state}'] - participant_scores[f'Before {mood_state}']

# Set the number of conditions
conditions = participant_scores['Condition'].unique()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Iterate through each condition and plot the average change for each mood state
for condition in conditions:
    # Filter the data for the current condition
    condition_data = participant_scores[participant_scores['Condition'] == condition]
    
    # Initialize lists to store x and y values
    x_values = []
    y_values = []
    
    # Calculate the average change for each mood state
    for mood_state in mood_states:
        x_values.append(mood_state)
        y_values.append(condition_data[f'Change {mood_state}'].mean())
    
    # Plot the average change for each mood state
    ax.plot(x_values, y_values, label=f'Condition {condition}')

# Add labels, title, and legend
ax.set_xlabel('Mood State')
ax.set_ylabel('Average Change')
ax.set_title('Average Change in Mood State Scores by Condition')
ax.legend(title='Condition')

# Show the plot
plt.show()
