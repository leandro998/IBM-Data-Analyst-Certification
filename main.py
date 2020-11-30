import pandas as pd
df = pd.read_csv('/Users/leandro998/PycharmProjects/StackOverflowSurvey2019/Datasets/m1_survey_data.csv')

# Find and remove duplicates
df.groupby(df.duplicated(), as_index=False).size()
df = df.drop_duplicates()

# Replace isnull values:
most_freq = df.WorkLoc.mode()
# print(most_freq)
df['WorkLoc'].fillna(value='Office', inplace=True)

# Normalizing salaries:
df.loc[df['CompFreq'] == 'Yearly', 'NormalizedAnnualCompensation'] = df['CompTotal']
df.loc[df['CompFreq'] == 'Monthly', 'NormalizedAnnualCompensation'] = df['CompTotal'] * 12
df.loc[df['CompFreq'] == 'Weekly', 'NormalizedAnnualCompensation'] = df['CompTotal'] * 52

# Finding and removing outliers of salaries:
# df.boxplot(column='ConvertedComp').show()
q1 = df['ConvertedComp'].quantile(0.25)
q3 = df['ConvertedComp'].quantile(0.75)
iqr = q3 - q1
print('Q1: ' + str(q1) + ' Q3: ' + str(q3) + ' IQR: ' + str(iqr))

lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

print('lower bounds: ' + str(lower_limit))
print('upper bounds: ' + str(upper_limit))

anomalies = []
for outlier in df['ConvertedComp']:
    if outlier > upper_limit or outlier < lower_limit:
        anomalies.append(outlier)

# print(anomalies)
# print(len(anomalies))

df = df[~((df['ConvertedComp'] < lower_limit) |(df['ConvertedComp'] > upper_limit))]

print(df.describe())

