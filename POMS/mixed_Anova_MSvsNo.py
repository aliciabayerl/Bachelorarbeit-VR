import pandas as pd
import pingouin as pg
import os
from statsmodels.stats.multicomp import MultiComparison

folder_path = 'POMS'
file_yes = 'POMS_MSyes_participant_scores.csv'
file_no = 'POMS_MS_participant_scores.csv'

file_path_yes = os.path.join(folder_path, file_yes)
file_path_no = os.path.join(folder_path, file_no)

data_yes = pd.read_csv(file_path_yes)
data_no = pd.read_csv(file_path_no)

def perform_mixed_anova(data, label):
    data_long = pd.melt(data, 
                        id_vars=['Condition_x', 'Participant'], 
                        value_vars=['Before Tension', 'After Tension', 'Before Vigor', 'After Vigor', 
                                    'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 
                                    'Before Anger_x', 'After Anger_x', 'Before Depression', 'After Depression'],
                        var_name='Time_Mood', 
                        value_name='Score')

    data_long['Time'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[0])
    data_long['Mood'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[1])

    data_long = data_long.rename(columns={'Condition_x': 'Group'})

    moods = data_long['Mood'].unique()

    for mood in moods:
        mood_data = data_long[data_long['Mood'] == mood]
        aov = pg.mixed_anova(dv='Score', within='Time', between='Group', subject='Participant', data=mood_data)
        print(f"Mixed ANOVA results for {label} - {mood}:")
        print(aov)
        print("\n")

perform_mixed_anova(data_yes, "Motion Sickness (Yes)")

perform_mixed_anova(data_no, "Motion Sickness (No)")

def perform_posthoc_tests(data_long, mood):
    mood_data = data_long[data_long['Mood'] == mood]

    mc = MultiComparison(mood_data['Score'], mood_data['Time'])

    result = mc.tukeyhsd()
    
    print(f"Post-hoc tests for {mood}:")
    print(result)
    print("\n")

interactions = ['Tension', 'Confusion', 'Fatigue', 'Anger_x', 'Depression']

data_yes_long = pd.melt(data_yes, 
                        id_vars=['Condition_x', 'Participant'], 
                        value_vars=['Before Tension', 'After Tension', 'Before Vigor', 'After Vigor', 
                                    'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 
                                    'Before Anger_x', 'After Anger_x', 'Before Depression', 'After Depression'],
                        var_name='Time_Mood', 
                        value_name='Score')
data_no_long = pd.melt(data_no, 
                       id_vars=['Condition_x', 'Participant'], 
                       value_vars=['Before Tension', 'After Tension', 'Before Vigor', 'After Vigor', 
                                   'Before Confusion', 'After Confusion', 'Before Fatigue', 'After Fatigue', 
                                   'Before Anger_x', 'After Anger_x', 'Before Depression', 'After Depression'],
                       var_name='Time_Mood', 
                       value_name='Score')

data_yes_long['Time'] = data_yes_long['Time_Mood'].apply(lambda x: x.split(' ')[0])
data_yes_long['Mood'] = data_yes_long['Time_Mood'].apply(lambda x: x.split(' ')[1])
data_no_long['Time'] = data_no_long['Time_Mood'].apply(lambda x: x.split(' ')[0])
data_no_long['Mood'] = data_no_long['Time_Mood'].apply(lambda x: x.split(' ')[1])

data_yes_long = data_yes_long.rename(columns={'Condition_x': 'Group'})
data_no_long = data_no_long.rename(columns={'Condition_x': 'Group'})

for mood in interactions:
    perform_posthoc_tests(data_yes_long, mood)
    perform_posthoc_tests(data_no_long, mood)
