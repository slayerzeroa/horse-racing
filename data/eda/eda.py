# eda

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rc('font', family='Malgun Gothic')
# sns.set_palette('coolwarm') 

# pandas all columns display
pd.set_option('display.max_columns', None)

# Importing the dataset
df = pd.read_csv('data/datasets/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')

print(list(df.columns))

data = df[['age', 'weather', 'jkName','hrName', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord', 'seG1fAccTime', 'seG3fAccTime', 'seS1fAccTime', 'se_1cAccTime', 'se_2cAccTime', 'se_3cAccTime', 'se_4cAccTime']]

# print(list(data.columns))

data['speed'] = data['rcDist'] / data['rcTime']
data = data[data['speed'] != float('inf')]


sns.set_palette('Set1')

# data speed distribution
sns.displot(data['speed'])
plt.title('Speed Distribution')
plt.show()

# age distribution
sns.displot(data['age'])
plt.title('Age Distribution')
plt.show()

# age & speed scatter plot
sns.scatterplot(x='age', y='speed', data=data)
plt.title('Age & Speed scatter plot')
plt.show()

# Measurement of average speed by age
statbyage = data.groupby(by=['age']).mean()[['wgBudam', 'rcDist', 'rcTime', 'ord', 'speed']]

print(statbyage)

statbyage['age'] = statbyage.index

# statbyage speed & age hist plot
sns.scatterplot(x='age', y='speed', data=statbyage)
plt.title('Group by age, speed scatter plot')
plt.show()

# statbyage ord & age hist plot
sns.scatterplot(x='age', y='ord', data=statbyage)
plt.title('Group by age, ord scatter plot')
plt.show()

statbysex = data.groupby(by=['sex']).mean()[['wgBudam', 'rcDist', 'rcTime', 'ord', 'speed']]

print(statbysex)

# statbysex speed & age scatter plot
sns.scatterplot(x='sex', y='speed', data=statbysex)
plt.title('Group by sex, speed scatter plot')
plt.show()

# statbysex ord & age scatter plot
sns.scatterplot(x='sex', y='ord', data=statbysex)
plt.title('Group by sex, ord scatter plot')
plt.show()