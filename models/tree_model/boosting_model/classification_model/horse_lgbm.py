## Random Forest Model

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from lightgbm import LGBMRegressor

from api.kra import *

# # pandas all columns display
# pd.set_option('display.max_columns', None)
#
# # Importing the dataset
# df = pd.read_csv('data/datasets/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')
# # pd.set_option('display.max_columns', None)
# # print(df)
#
# print(list(df.columns))
# print(df['ord'].unique())
#
# # train 구하기
# data = df[['age', 'weather', 'jkName','hrName', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord']]
# data['speed'] = data['rcDist'] / data['rcTime']
# data['rcUnique'] = data['rcDate'].astype(str) + data['rcNo'].astype(str)
#
# # ord == 1 -> 1 else 0 (1위만 1 나머지 0)
# data = data[data['ord']<10]
# data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)
#
# # Label Encoding (Categorical Data)
# le = LabelEncoder()
# data['weather'] = le.fit_transform(data['weather'])
# data['jkName'] = le.fit_transform(data['jkName'])
# data['hrName'] = le.fit_transform(data['hrName'])
# data['rcUnique'] = le.fit_transform(data['rcUnique'])
# data['sex'] = le.fit_transform(data['sex'])
#
# # drop rcDate
# data.drop(['rcDate', 'rcNo', 'rcTime', 'jkName', 'hrName'], axis=1, inplace=True)
#
# # rcDate_diff str -> float
# data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: float('nan') if type(x) != str else float(x[:-5]))
# data['rcDate_diff'] = data['rcDate_diff'].fillna(99999)
# # data['rcDate_diff'] = data['rcDate_diff'].dropna()
# # print(data['rcDate_diff'])
#
# data = data.dropna()

data = get_modelData_from_db(3)
data = data.sort_values(by=['rcDate'])
data = data.reset_index(drop=True)
data = data[(data['rcDate'] > '2010-01-01')]
data = data[(data['rcDate'] < '2024-05-01')]
data = data[data['ord']<10]
data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)

# calculate season
data['rcDate'] = pd.to_datetime(data['rcDate'])
data['season'] = data['rcDate'].dt.month.apply(lambda x: 1 if x in [3, 4, 5] else 2 if x in [6, 7, 8] else 3 if x in [9, 10, 11] else 4)

le = LabelEncoder()
data['weather'] = le.fit_transform(data['weather'])
data['jkName'] = le.fit_transform(data['jkName'])
data['hrName'] = le.fit_transform(data['hrName'])
data['sex'] = le.fit_transform(data['sex'])
print(data)
print(data.columns)

# rcDate_diff 변환
data['rcDate_diff'] = data['rcDate_diff'].fillna(pd.Timedelta(days=99999))
data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else int(x))

# inf 값 처리
data.replace([np.inf, -np.inf], np.nan, inplace=True)

# 결측값 처리
data.fillna(99999, inplace=True)

# # inf 값의 개수 확인
# inf_count = data.apply(lambda x: np.isinf(x).sum())
# print(inf_count)

# X, y split
X = data.drop(['ord', 'globalUnique', 'rcId', 'meet', 'rcNo', 'rcDate'], axis=1)
X_columns = X.columns
X = X.values
y = data.ord.values


# train, test split
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2, random_state=0)

# Fitting LGBM Regression to the dataset
regressor = LGBMRegressor(learning_rate=0.005, n_estimators=300, max_depth=4, random_state=0)
regressor.fit(X_train, y_train)


# Predicting a new result
y_pred = regressor.predict(X_test)
print(y_pred)

# accuracy
print('Mean Squared Error: ', mean_squared_error(y_test, y_pred))
print('R2 Score: ', r2_score(y_test, y_pred))

# feature importance
importance = regressor.feature_importances_
print(importance)

# feature importance visualization
plt.bar([x for x in range(len(importance))], importance)
plt.xticks([x for x in range(len(importance))], X_columns)
plt.show()