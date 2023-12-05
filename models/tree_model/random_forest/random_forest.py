## Random Forest Model

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
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('coolwarm') 

# pandas all columns display
pd.set_option('display.max_columns', None)

# Importing the dataset
df = pd.read_csv('data/datasets/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')
# pd.set_option('display.max_columns', None)
# print(df)

print(list(df.columns))
print(df['ord'].unique())

# train 구하기
data = df[['age', 'weather', 'jkName','hrName', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord', 'winOdds', 'plcOdds']]
data['speed'] = data['rcDist'] / data['rcTime_mean']
data['rcUnique'] = data['rcDate'].astype(str) + data['rcNo'].astype(str)

# ord == 1 -> 1 else 0 (1위만 1 나머지 0)
data = data[data['ord']<10]
data['ord'] = data['ord'].apply(lambda x: 1 if x==1 else 0)

# Label Encoding (Categorical Data)
le = LabelEncoder()
data['weather'] = le.fit_transform(data['weather'])
data['jkName'] = le.fit_transform(data['jkName'])
data['hrName'] = le.fit_transform(data['hrName'])
data['rcUnique'] = le.fit_transform(data['rcUnique'])
data['sex'] = le.fit_transform(data['sex'])

# drop rcDate
data.drop(['rcDate', 'rcNo', 'rcTime'], axis=1, inplace=True)

# rcDate_diff str -> float
data['rcDate_diff'] = data['rcDate_diff'].apply(lambda x: float('nan') if type(x) != str else float(x[:-5]))
data['rcDate_diff'] = data['rcDate_diff'].fillna(99999)
# print(data['rcDate_diff'])

data = data.dropna()

# X, y split
X = data.drop(['ord'], axis=1)
y = data.ord

# train, test split
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)


# Fitting Random Forest Regression to the dataset
classifier = RandomForestClassifier(n_estimators=1000, random_state=0, max_features=5, max_depth=5, min_samples_leaf=5)
classifier.fit(X_train, y_train)

# Predicting a new result
y_pred = classifier.predict(X_test)
print(y_pred)

# accuracy
print('Mean Squared Error: ', mean_squared_error(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))
print('When Hit 1 Accuracy:', accuracy_score(y_test[y_test==1], y_pred[y_test==1]))

fpr, tpr, thresholds = roc_curve(y, classifier.predict_proba(X)[:,1])
plt.figure()
lw = 2
plt.plot(
    fpr,
    tpr,
    color="darkorange",
    lw=lw,
    label="ROC curve",
)
plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC")
plt.legend(loc="lower right")
plt.show()

roc_auc = auc(fpr, tpr)
print("AUC:", roc_auc)

# feature importance
importance = classifier.feature_importances_
print(importance)

# feature importance visualization
sns.barplot(x=X.columns, y=importance)
plt.xticks(rotation=0)
plt.show()


# VIF
vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(
    X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns
plt.figure(figsize=(12, 8))
sns.set_palette('pastel')
sns.barplot(data=vif, x='features' , y='VIF Factor')

plt.title('VIF')
plt.xlabel('feature')
plt.ylabel('VIF factor')
plt.xticks(rotation=45)

plt.show()


# 재학습
X = data.drop(['ord', 'rcDist', 'rcTime_mean'], axis=1)
y = data.ord

X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)
classifier = RandomForestClassifier(n_estimators=1000, random_state=0, max_features=5, max_depth=5, min_samples_leaf=5)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(y_pred)
print('재학습 Mean Squared Error: ', mean_squared_error(y_test, y_pred))
print('재학습 Accuracy:', accuracy_score(y_test, y_pred))
print('재학습 When Hit 1 Accuracy:', accuracy_score(y_test[y_test==1], y_pred[y_test==1]))