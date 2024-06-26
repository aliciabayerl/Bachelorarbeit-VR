import pandas as pd
import pingouin as pg
import os

folder_path = 'POMS'
input_file = 'POMS_MS_participant_scores.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

data_long = pd.melt(data, 
                    id_vars=['Participant', 'Condition_x'], 
                    value_vars=['Before Tension', 'After Tension', 'Before Vigor', 'After Vigor', 'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 'Before Anger_x', 'After Anger_x', 'Before Depression', 'After Depression'],
                    var_name='Time_Mood', 
                    value_name='Score')

data_long['Time'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[0])
data_long['Mood'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[1])

data_long = data_long.rename(columns={'Condition_x': 'Group'})

moods = data_long['Mood'].unique()

# Perform separate mixed ANOVAs for each mood state
for mood in moods:
    mood_data = data_long[data_long['Mood'] == mood]
    aov = pg.mixed_anova(dv='Score', within='Time', between='Group', subject='Participant', data=mood_data)
    print(f"Mixed ANOVA results for {mood}:")
    print(aov)
    print("\n")
