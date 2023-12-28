# Importing the libraries
import numpy as np
import pandas as pd
import math

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, roc_curve, auc

from statsmodels.stats.outliers_influence import variance_inflation_factor

from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('coolwarm') 

# pandas all columns display
pd.set_option('display.max_columns', None)

data = pd.read_csv('C:/Users/slaye/PycharmProjects/Horse_Racing/data/test/seoul_horse_records.csv')
# ord == 1 -> 1 else 0 (1위만 1 나머지 0)
data = data[data['ord']<10]
data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)

# Label Encoding (Categorical Data)
le = LabelEncoder()
data['weather'] = le.fit_transform(data['weather'])
data['jkName'] = le.fit_transform(data['jkName'])
data['sex'] = le.fit_transform(data['sex'])

# rcDate_diff str -> float
data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: float('nan') if type(x) != str else float(x[:-5]))
data['rcDate_diff'] = data['rcDate_diff'].fillna(99999)

# fill inf
data = data.replace([np.inf, -np.inf], np.nan)

data = data.dropna()

# X, y split
X = data.drop(['ord'], axis=1)
y = data.ord

# train, test split
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)

# Fitting XGBoost Regression to the dataset
classifier = XGBClassifier(n_estimators=10000, random_state=0, max_depth=4, learning_rate=0.01, min_child_weight=5, gamma=0.1, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.005)
classifier.fit(X_train, y_train)

# Predicting a new result
y_pred = classifier.predict(X_test)
print(y_pred)

# accuracy
print('Mean Squared Error: ', mean_squared_error(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))
print('When Hit 1 Accuracy:', accuracy_score(y_test[y_test==1], y_pred[y_test==1]))

print(y_test)
print(y_pred)

# print()
# pd.set_option('display.max_rows', None)
# verify = pd.DataFrame([y_test, y_pred], index=['real', 'pred']).T
# print(verify)

