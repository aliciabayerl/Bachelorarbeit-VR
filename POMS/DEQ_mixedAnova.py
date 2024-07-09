import pandas as pd
import pingouin as pg
import os
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load your data
folder_path = 'POMS'
input_file = 'participant_scores_deq.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Reshape the data
data_long = pd.melt(data, 
                    id_vars=['Participant', 'Condition'], 
                    value_vars=['Before Anger', 'After Anger', 'Before Disgust', 'After Disgust', 'Before Fear', 'After Fear',
                                'Before Anxiety', 'After Anxiety', 'Before Sadness', 'After Sadness', 'Before Desire', 'After Desire',
                                'Before Relaxation', 'After Relaxation', 'Before Happiness', 'After Happiness'],
                    var_name='Time_Mood', 
                    value_name='Score')

data_long['Time'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[0])
data_long['Mood'] = data_long['Time_Mood'].apply(lambda x: x.split(' ')[1])

data_long = data_long.rename(columns={'Condition': 'Group'})

moods = data_long['Mood'].unique()

for mood in moods:
    mood_data = data_long[data_long['Mood'] == mood]
    aov = pg.mixed_anova(dv='Score', within='Time', between='Group', subject='Participant', data=mood_data)
    print(f"Mixed ANOVA results for {mood}:")
    print(aov)
    print("\n")

    # Perform post-hoc Tukey HSD test if the interaction is significant
    if aov.loc[(aov['Source'] == 'Time * Group') & (aov['p-unc'] < 0.05), 'p-unc'].any():
        mc = pairwise_tukeyhsd(mood_data['Score'], mood_data['Time'] + ' ' + mood_data['Group'])
        print(f"Post-hoc Tukey HSD tests for {mood}:")
        print(mc)
        print("\n")
