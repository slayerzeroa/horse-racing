# Importing the libraries
import numpy as np
import pandas as pd
import math

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, roc_curve, auc

from statsmodels.stats.outliers_influence import variance_inflation_factor

from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import seaborn as sns

from api.kra import *


# '''Version 1'''
# df = pd.read_csv('../../data/datasets/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')
# data = df[['age', 'weather', 'jkName','hrName', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord', 'winOdds', 'plcOdds']]
# data['speed'] = data['rcDist'] / data['rcTime_mean']
# data['rcUnique'] = data['rcDate'].astype(str) + data['rcNo'].astype(str)
# # ord == 1 -> 1 else 0 (1위만 1 나머지 0)
# data = data[data['ord']<10]
# data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)
# # Label Encoding (Categorical Data)
# le = LabelEncoder()
# data['weather'] = le.fit_transform(data['weather'])
# data['jkName'] = le.fit_transform(data['jkName'])
# data['hrName'] = le.fit_transform(data['hrName'])
# data['rcUnique'] = le.fit_transform(data['rcUnique'])
# data['sex'] = le.fit_transform(data['sex'])
# # drop rcDate
# data.drop(['rcDate', 'rcNo', 'rcTime'], axis=1, inplace=True)
# # rcDate_diff str -> float
# data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: float('nan') if type(x) != str else float(x[:-5]))
# data['rcDate_diff'] = data['rcDate_diff'].fillna(99999)
# # infinite value -> nan
# data['speed'] = data['speed'].apply(lambda x: float('nan') if x == float('inf') else x)
# data = data.dropna()
#
# # 재학습
# X = data.drop(['ord', 'rcDist', 'rcTime_mean'], axis=1)
# y = data.ord


'''Version 2'''
df = get_modelData_from_db(3)
def preprocess_for_train(df):
    df = df.sort_values(by=['rcDate', 'rcNo'])
    df = df.reset_index(drop=True)
    df = df[(df['rcDate'] > '2010-01-01')]
    df = df[(df['rcDate'] < '2024-05-01')]
    df = df[df['ord'] < 10]
    df['ord'] = df['ord'].apply(lambda x: 1 if x == 1 else 0)

    # calculate season
    df['rcDate'] = pd.to_datetime(df['rcDate'])
    df['season'] = df['rcDate'].dt.month.apply(
        lambda x: 1 if x in [3, 4, 5] else 2 if x in [6, 7, 8] else 3 if x in [9, 10, 11] else 4)

    le = LabelEncoder()
    df['weather'] = le.fit_transform(df['weather'])
    df['jkName'] = le.fit_transform(df['jkName'])
    df['hrName'] = le.fit_transform(df['hrName'])
    df['sex'] = le.fit_transform(df['sex'])

    # rcDate_diff 변환
    df['rcDate_diff'] = df['rcDate_diff'].fillna(pd.Timedelta(days=99999))
    df['rcDate_diff'] = df['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else int(x))

    # inf 값 처리
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df = df.dropna()

    X = df.drop(['ord', 'globalUnique', 'rcId', 'meet', 'rcNo', 'rcDate'], axis=1)
    y = df.ord

    return X, y

X, y = preprocess_for_train(df)

X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)

XGBClassifier = XGBClassifier(n_estimators=10000, random_state=42, max_depth=6, learning_rate=0.01)
XGBClassifier.fit(X_train, y_train)

y_pred = XGBClassifier.predict(X_test)

# result = []
# for i in y_pred:
#     if i == 1:
#         result.append(1)
#     else:
#         result.append(0)
#
# result = np.array(result)

print(accuracy_score(y_test[y_test==1], y_pred[y_test==1]))


# XGBClassifier = XGBClassifier(n_estimators=10000, random_state=42, max_depth=6, learning_rate=0.01)
# XGBClassifier.fit(X_train, y_train)
# LGBMClassifier = LGBMClassifier(n_estimators=10000, random_state=42, max_depth=6, learning_rate=0.01)
# LGBMClassifier.fit(X_train, y_train)
# RandomForestClassifier = RandomForestClassifier(n_estimators=10000, random_state=42, max_depth=6)
# RandomForestClassifier.fit(X_train, y_train)

# xgb_y_pred = XGBClassifier.predict(X_test)
# lgbm_y_pred = LGBMClassifier.predict(X_test)
# rf_y_pred = RandomForestClassifier.predict(X_test)

# combined_y_pred = xgb_y_pred + lgbm_y_pred + rf_y_pred

# combined_y_pred = xgb_y_pred
#
# result = []
# for i in combined_y_pred:
#     if i >= 2:
#         result.append(1)
#     else:
#         result.append(0)
#
# result = np.array(result)
#
# print(accuracy_score(y_test[y_test==1], result[y_test==1]))