## Random Forest Model

# Importing the libraries
import numpy as np
import pandas as pd
import math

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, roc_curve, auc, f1_score

from statsmodels.stats.outliers_influence import variance_inflation_factor

# from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor
import xgboost as xgb


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('coolwarm') 

# pandas all columns display
pd.set_option('display.max_columns', None)

# Importing the dataset
df = pd.read_csv('data/datasets/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')

# data selection
data = df[['age', 'weather', 'jkName','hrName', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord', 'winOdds', 'plcOdds']]
data['speed'] = data['rcDist'] / data['rcTime_mean']
data['rcUnique'] = data['rcDate'].astype(str) + data['rcNo'].astype(str)
# print(data['rcUnique'])

# Labeling
# ord == 1 -> 1 else 0 (1위만 1 나머지 0)
# data = data[data['ord']<10]
data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)

# Label Encoding (Categorical Data)
le = LabelEncoder()
data['weather'] = le.fit_transform(data['weather'])
data['jkName'] = le.fit_transform(data['jkName'])
data['hrName'] = le.fit_transform(data['hrName'])
# data['rcUnique'] = le.fit_transform(data['rcUnique'])
data['sex'] = le.fit_transform(data['sex'])

# drop rcDate
data.drop(['rcDate', 'rcNo', 'rcTime', 'winOdds', 'plcOdds'], axis=1, inplace=True)

# data sort by rcUnique
data = data.sort_values(by=['rcUnique'])
data.reset_index(drop=True, inplace=True)

# rcDate_diff str -> float
data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: float('nan') if type(x) != str else float(x[:-5]))
data['rcDate_diff'] = data['rcDate_diff'].fillna(99999)

# infinite value -> nan
data['speed'] = data['speed'].apply(lambda x: float('nan') if x == float('inf') else x)


# fill nan value
data = data.fillna(data.mean())
# data = data.dropna()

# X, y split
X = data.drop(['ord'], axis=1)
y = data.ord

# train, test split
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# For binary classification
param = {'objective': 'binary:logistic', 'eval_metric': 'logloss'}

# Fitting XGBoost Classifier to the dataset
# classifier = xgb(n_estimators=1000, random_state=42, max_depth=6, learning_rate=0.01)
bst = xgb.train(param, dtrain, num_boost_round=1000)

# For binary classification
preds_proba = bst.predict(dtest)

# print(preds_proba)
df_test = pd.DataFrame(X_test, columns=X.columns)
df_test['winprob'] = preds_proba


# prob의 합을 1로 맞추는 함수
def fit_prob(x):
    return x / x.sum(axis=0) # only difference

# x 중 가장 큰 값을 1로 맞추고 나머지는 0으로 만드는 함수
def fit_rank(x):
    return [1 if i == x.max() else 0 for i in x]

## softmax to df_test['winprob'] by df_test['rcUnique']
# print(df_test[df_test['rcUnique'] == '200706094'])
df_test['winprob'] = df_test.groupby('rcUnique')['winprob'].transform(lambda x: fit_prob(x))
df_test['winprob'] = df_test.groupby('rcUnique')['winprob'].transform(lambda x: fit_rank(x))
y_pred = df_test['winprob'].to_numpy()

print('Mean Squared Error: ', mean_squared_error(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))
print('When Hit 1 Accuracy:', accuracy_score(y_test[y_test==1], y_pred[y_test==1]))
print('When Pred 1 Accuracy:', accuracy_score(y_test[y_pred==1], y_pred[y_pred==1]))
