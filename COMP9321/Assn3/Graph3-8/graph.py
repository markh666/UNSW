import pandas as pd
from ggplot import *

df = pd.read_table("processed.cleveland.data", header = None, sep=',')
for i in df:
    df = df[~df[i].isin(['?'])]

#Q3
df_agg = df.loc[:,[0, 1, 2]]
df_agg[1][df_agg[1]==0] = 'Female'
df_agg[1][df_agg[1]==1] = 'Male'
df_agg[2][df_agg[2]==1] = 'Typical angin'
df_agg[2][df_agg[2]==2] = 'Atypical angina'
df_agg[2][df_agg[2]==3] = 'Non-anginal pain'
df_agg[2][df_agg[2]==4] = 'Asymptomatic'

df_agg.rename(columns={0:'Age', 1:'Sex', 2:'Chest Pain Type'}, inplace=True)

Q3 = ggplot(aes(x='Age', color='Chest Pain Type'), data=df_agg) + geom_density() + ggtitle("Chest Pain Type") + facet_wrap('Sex')
print(Q3)

#Q4
df_agg = df.loc[:,[0, 1, 3]]
df_agg[1][df_agg[1]==0] = 'female'
df_agg[1][df_agg[1]==1] = 'male'
df_agg[0][df[0]<40] = 'Younger than 40'
df_agg[0][df[0]>60] = 'Older than 60'
df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
df_agg.rename(columns={0: 'Age', 1:'Sex', 3:'Resting Blood Pressure'}, inplace=True)
Q4 = ggplot(aes(x='Resting Blood Pressure', color='Age'), data=df_agg) + geom_density() + ggtitle("Resting Blood Pressure") + facet_wrap('Sex')
print(Q4)

#Q5
df_agg = df.loc[:,[0, 1, 4]]
df_agg[1][df_agg[1]==0] = 'female'
df_agg[1][df_agg[1]==1] = 'male'
df_agg[0][df[0]<40] = 'Younger than 40'
df_agg[0][df[0]>60] = 'Older than 60'
df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
df_agg.rename(columns={0: 'Age', 1:'Sex', 4:'Serum Cholestoral in mg/dl'}, inplace=True)
Q5 = ggplot(aes(x='Serum Cholestoral in mg/dl', color='Age'), data=df_agg) + geom_density() + ggtitle("Serum Cholestoral in mg/dl") + facet_wrap('Sex')
print(Q5)

#Q6
df_agg = df.loc[:,[0, 1, 5]]
df_agg[1][df_agg[1]==0] = 'female'
df_agg[1][df_agg[1]==1] = 'male'
df_agg[5][df_agg[5]==0] = 'less or equal than 120 mg/dl'
df_agg[5][df_agg[5]==1] = 'greater than 120 mg/dl'
df_agg.rename(columns={0:'Age', 1:'Sex', 5:'Fasting Blood Sugar'}, inplace=True)
Q6 = ggplot(aes(x='Age', color='Fasting Blood Sugar'), data=df_agg) + geom_density() + ggtitle("Fasting Blood Sugar") + facet_wrap('Sex')
print(Q6)

#Q7
df_agg = df.loc[:,[0, 1, 6]]

df_agg[1][df_agg[1]==0] = 'Female'
df_agg[1][df_agg[1]==1] = 'Male'

df_agg[6][df_agg[6]==0.0] = 'Normal'
df_agg[6][df_agg[6]==1.0] = 'Normal'  # 太少了，和1归为一类？
df_agg[6][df_agg[6]==2.0] = "Showing probable or definite left ventricular hypertrophy"

df_agg.rename(columns={0:'Age', 1:'Sex', 6:'Resting'}, inplace=True)
Q7 = ggplot(aes(x='Age', color='Resting'), data=df_agg) + geom_density() + ggtitle("Resting Electrocardiographic Results") + facet_wrap('Sex')
print(Q7)

#Q8
df_agg = df.loc[:,[0, 1, 7]]
df_agg[1][df_agg[1]==0] = 'female'
df_agg[1][df_agg[1]==1] = 'male'
df_agg[0][df[0]<40] = 'Younger than 40'
df_agg[0][df[0]>60] = 'Older than 60'
df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
df_agg.rename(columns={0: 'Age', 1:'Sex', 7:'Maximum Heart Rate Achieved'}, inplace=True)
Q8 = ggplot(aes(x='Maximum Heart Rate Achieved', color='Age'), data=df_agg) + geom_density() + ggtitle("Maximum Heart Rate Achieved") + facet_wrap('Sex')
print(Q8)