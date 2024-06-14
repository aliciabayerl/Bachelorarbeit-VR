import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np



folder_path = 'POMS'
input_file = 'questionnaire2.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

df = pd.DataFrame(data)

# Gender
gender_counts = data['Gender'].value_counts()

# Filter participants in the age range
age_range_18_24 = data[data['Age Range'] == '18-24']
age_range_25_34 = data[data['Age Range'] == '25-34']

num_participants_18_24 = len(age_range_18_24)
num_participants_25_34 = len(age_range_25_34)

# Occupation
employed = data[data['Occupation'] == 'Employed']
num_employed = len(employed)

# Previous VR Experience
percentage_experience = df['Please indicate your previous experience with virtual reality:'].value_counts(normalize=True) * 100

print("Percentage of Previous Experience with Virtual Reality:")
print(percentage_experience)



print("Number of participants in the age range 18-24:", num_participants_18_24)
print("Number of participants in the age range 25-34:", num_participants_25_34)

print("Num ppl employed:", num_employed)
print("Number of male participants:", gender_counts.get('Male', 0))
print("Number of female participants:", gender_counts.get('Female', 0))
print("Number of diverse participants:", gender_counts.get('Another gender', 0))