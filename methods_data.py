import pandas as pd
import os

folder_path = 'POMS'
input_file = 'questionnaire2.csv'
file_path = os.path.join(folder_path, input_file)
data = pd.read_csv(file_path)

# Gender distribution
gender_counts = data['Gender'].value_counts()
gender_percentages = data['Gender'].value_counts(normalize=True) * 100

# Age distribution
age_counts = data['Age Range'].value_counts()
age_percentages = data['Age Range'].value_counts(normalize=True) * 100

# Employment status
employment_counts = data['Occupation'].value_counts()
employment_percentages = data['Occupation'].value_counts(normalize=True) * 100

# Previous VR Experience
vr_experience_counts = data['Please indicate your previous experience with virtual reality:'].value_counts()
vr_experience_percentages = data['Please indicate your previous experience with virtual reality:'].value_counts(normalize=True) * 100

# Walking in nature relaxation response
nature_relaxation_counts = data['Is walking in nature in real life relaxing for you?'].value_counts()
nature_relaxation_percentages = data['Is walking in nature in real life relaxing for you?'].value_counts(normalize=True) * 100

# Combine all the data into a DataFrame for a comprehensive table
demographics_table = pd.DataFrame({
    'Category': ['Gender', 'Age Range', 'Occupation', 'VR Experience', 'Nature Relaxation'],
    'Counts': [gender_counts.to_dict(), age_counts.to_dict(), employment_counts.to_dict(), vr_experience_counts.to_dict(), nature_relaxation_counts.to_dict()],
    'Percentages': [gender_percentages.to_dict(), age_percentages.to_dict(), employment_percentages.to_dict(), vr_experience_percentages.to_dict(), nature_relaxation_percentages.to_dict()]
})

pd.set_option('display.max_rows', None)  # Ensure all rows are displayed
pd.set_option('display.max_columns', None)  # Ensure all columns are displayed
pd.set_option('display.width', None)  # Ensure the display width fits the data
pd.set_option('display.max_colwidth', None)  # Ensure full width of column content is shown
print(demographics_table)

folder_path = 'POMS'
output_file = 'demographics_table.csv'
output_path = os.path.join(folder_path, output_file)
demographics_table.to_csv(output_path, index=False)

