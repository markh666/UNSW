import pandas as pd
from ggplot import *

df = pd.read_table("processed.cleveland.data", header = None, sep=',')
for i in df:
    df = df[~df[i].isin(['?'])]

def q3():
	df_agg = df.loc[:,[0, 1, 2]]
	df_agg[1][df_agg[1]==0] = 'Female'
	df_agg[1][df_agg[1]==1] = 'Male'
	df_agg[2][df_agg[2]==1] = 'Angina'
	df_agg[2][df_agg[2]==2] = 'Angina'
	df_agg[2][df_agg[2]==3] = 'Non-Anginal or Asymptomatic'
	df_agg[2][df_agg[2]==4] = 'Non-Anginal or Asymptomatic'

	df_agg.rename(columns={0:'Age', 1:'Sex', 2:'Chest Pain Type'}, inplace=True)

	Q3 = ggplot(aes(x='Age', color='Chest Pain Type'), data=df_agg) + geom_density() + ggtitle("Chest Pain Type") + facet_wrap('Sex')
	print(Q3)

def q4():
	df_agg = df.loc[:,[0, 1, 3]]
	df_agg[1][df_agg[1]==0] = 'female'
	df_agg[1][df_agg[1]==1] = 'male'
	df_agg[0][df[0]<40] = 'Younger than 40'
	df_agg[0][df[0]>60] = 'Older than 60'
	df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
	df_agg.rename(columns={0: 'Age', 1:'Sex', 3:'Resting Blood Pressure'}, inplace=True)
	Q4 = ggplot(aes(x='Resting Blood Pressure', color='Age'), data=df_agg) + geom_density() + ggtitle("Resting Blood Pressure") + facet_wrap('Sex')
	print(Q4)

def q5_box():
	df_agg = df.loc[:,[0, 1, 4]]
	df_agg[1][df_agg[1]==0] = 'female'
	df_agg[1][df_agg[1]==1] = 'male'
	df_agg[0][df[0]<40] = 'Younger than 40'
	df_agg[0][df[0]>60] = 'Older than 60'
	df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
	df_agg.rename(columns={0: 'Age', 1:'Sex', 4:'Serum Cholestoral in mg/dl'}, inplace=True)
	Q5 = ggplot(aes(x='Serum Cholestoral in mg/dl', color='Age'), data=df_agg) + geom_density() + ggtitle("Serum Cholestoral in mg/dl") + facet_wrap('Sex')
	print(Q5)

def q5():
    df_agg = df.loc[:, [0,1,4]]
    df_agg[1][df_agg[1]==0] = 'female'
    df_agg[1][df_agg[1]==1] = 'male'
    df_agg.rename(columns={0: 'age', 1: 'sex', 4: 'Serum Cholestoral in mg/dl'}, inplace=True)
    # df[['age', 'sex', 'oldpeak']] = df[[1,2,10]].apply(pd[2].to_string)
    g = ggplot(df_agg, aes(x='sex',y='Serum Cholestoral in mg/dl')) + geom_boxplot() + labs(title='Q5') + labs(x="sex") + labs(y="Serum Cholestoral in mg/dl")
    print(g)

def q6():
	df_agg = df.loc[:,[0, 1, 5]]
	df_agg[1][df_agg[1]==0] = 'female'
	df_agg[1][df_agg[1]==1] = 'male'
	df_agg[5][df_agg[5]==0] = 'Less or Equal than 120 mg/dl'
	df_agg[5][df_agg[5]==1] = 'Greater than 120 mg/dl'
	df_agg.rename(columns={0:'Age', 1:'Sex', 5:'Fasting Blood Sugar'}, inplace=True)
	Q6 = ggplot(aes(x='Age', color='Fasting Blood Sugar'), data=df_agg) + geom_density() + ggtitle("Fasting Blood Sugar") + facet_wrap('Sex')
	print(Q6)

def q7():
	df_agg = df.loc[:,[0, 1, 6]]

	df_agg[1][df_agg[1]==0] = 'Female'
	df_agg[1][df_agg[1]==1] = 'Male'

	df_agg[6][df_agg[6]==0.0] = 'Normal'
	df_agg[6][df_agg[6]==1.0] = 'Abnormal'  # 太少了，和1归为一类？
	df_agg[6][df_agg[6]==2.0] = "Abnormal"

	df_agg.rename(columns={0:'Age', 1:'Sex', 6:'Resting Electrocardiographic Results'}, inplace=True)
	Q7 = ggplot(aes(x='Age', color='Resting Electrocardiographic Results'), data=df_agg) + geom_density() + ggtitle("Resting Electrocardiographic Results") + facet_wrap('Sex')
	print(Q7)

def q8():
	df_agg = df.loc[:,[0, 1, 7]]
	df_agg[1][df_agg[1]==0] = 'female'
	df_agg[1][df_agg[1]==1] = 'male'
	df_agg[0][df[0]<40] = 'Younger than 40'
	df_agg[0][df[0]>60] = 'Older than 60'
	df_agg[0][abs(df[0]-50)<11] = 'Between 40 to 60'
	df_agg.rename(columns={0: 'Age', 1:'Sex', 7:'Maximum Heart Rate Achieved'}, inplace=True)
	Q8 = ggplot(aes(x='Maximum Heart Rate Achieved', color='Age'), data=df_agg) + geom_density() + ggtitle("Maximum Heart Rate Achieved") + facet_wrap('Sex')
	print(Q8)

def q8_box():
    df_agg = df.loc[:, [0,1,7]]
    df_agg[1][df_agg[1]==0] = 'female'
    df_agg[1][df_agg[1]==1] = 'male'
    df_agg.rename(columns={0: 'age', 1: 'sex', 7: 'Maximum Heart Rate Achieved'}, inplace=True)
    # df[['age', 'sex', 'oldpeak']] = df[[1,2,10]].apply(pd[2].to_string)
    g = ggplot(df_agg, aes(x='sex',y='Maximum Heart Rate Achieved')) + geom_boxplot() + labs(title='Q8') + labs(x="sex") + labs(y="Maximum Heart Rate Achieved")
    print(g)

