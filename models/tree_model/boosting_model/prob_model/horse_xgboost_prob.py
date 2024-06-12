## Random Forest Model

'''version 3'''

import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import xgboost as xgb
from lightgbm import LGBMRegressor
import matplotlib.pyplot as plt
#
# from data.db.kra_db import get_modelData_from_db, get_period_modelData

from kra import *

pd.set_option('display.max_columns', None)

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

    # 2010-01-08 -> 20100108
    df['rcDate'] = df['rcDate'].apply(lambda x: x.strftime('%Y%m%d'))

    # rcDate_diff 변환
    df['rcDate_diff'] = df['rcDate_diff'].fillna(pd.Timedelta(days=99999))
    df['rcDate_diff'] = df['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else int(x))

    # inf 값 처리
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df = df.dropna()

    X = df.drop(['ord', 'globalUnique', 'meet', 'rcNo', 'rcDate'], axis=1)
    y = df.ord

    return X, y
def preprocess_for_test(df):
    df = df.sort_values(by=['rcDate', 'rcNo'])
    df = df.reset_index(drop=True)
    # df = df[df['ord'] < 10]
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

    # inf 값 처리
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df['rcDate_diff'] = df['rcDate_diff'].fillna(99999)
    df['avg_past_speed'] = df['avg_past_speed'].fillna(-99999)
    X = df.drop(['ord', 'globalUnique', 'meet', 'rcNo', 'rcDate'], axis=1)
    y = df.ord

    return X, y

# prob의 합을 1로 맞추는 함수
def fit_prob(x):
    return x / x.sum(axis=0) # only difference

# x 중 가장 큰 값을 1로 맞추고 나머지는 0으로 만드는 함수
def fit_rank(x):
    return [1 if i == x.max() else 0 for i in x]


def train():
    # 데이터 로드
    df = get_modelData_from_db(meet=None)
    X, y = preprocess_for_train(df)
    X_columns = X.columns


    # # train, test split
    # X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, shuffle=False, test_size=0.2, random_state=0)
    X = X.values
    y = y.values
    # For binary classification
    param = {'objective': 'binary:logistic', 'eval_metric': 'logloss'}

    # Fitting XGBoost Classifier to the dataset
    classifier = xgb.XGBClassifier(n_estimators=10000, random_state=42, max_depth=6, learning_rate=0.01)
    classifier.fit(X, y)

    # For binary classification
    preds_proba = classifier.predict_proba(X)[:, 1]

    # print(preds_proba)
    df_test = pd.DataFrame(X, columns=X_columns)
    df_test['winprob'] = preds_proba

    ## softmax to df_test['winprob'] by df_test['rcId']
    df_test['winprob'] = df_test.groupby('rcId')['winprob'].transform(lambda x: fit_prob(x))
    df_test['winprob'] = df_test.groupby('rcId')['winprob'].transform(lambda x: fit_rank(x))
    y_pred = df_test['winprob'].to_numpy()

    print('Mean Squared Error: ', mean_squared_error(y, y_pred))
    print('Accuracy:', accuracy_score(y, y_pred))
    print('When Hit 1 Accuracy:', accuracy_score(y[y==1], y_pred[y==1]))
    print('When Pred 1 Accuracy:', accuracy_score(y[y_pred==1], y_pred[y_pred==1]))

    # feature importance
    importance = classifier.feature_importances_
    print(importance)

    return classifier

def predict(test_df, classifier):
    X_test, y_test = preprocess_for_test(test_df)
    X_test = X_test.to_numpy()


    # binary classification prediction
    preds_proba = classifier.predict_proba(X_test)[:, 1]

    test_df['winprob'] = preds_proba

    ## softmax to df_test['winprob'] by df_test['rcId']
    test_df['winprob'] = test_df.groupby('rcId')['winprob'].transform(lambda x: fit_prob(x))
    test_df['winprob'] = test_df.groupby('rcId')['winprob'].transform(lambda x: fit_rank(x))
    y_pred = test_df['winprob'].to_numpy()

    test_df['pred'] = y_pred

    pd.set_option('display.max_rows', None)
    return(test_df[['rcId', 'hrName', 'winprob', 'pred']])


# 숙제: 모델 불러와서 추가 데이터 학습

# classifier = train()
# classifier.save_model('xgboost_model.json')

def xgb_load_model():
    classifier = xgb.XGBClassifier()
    classifier.load_model('C:/Users/slaye/PycharmProjects/Horse_Racing/models/tree_model/boosting_model/prob_model/xgboost_model.json')
    return classifier

def get_predict_data(start, end):
    classifier = xgb_load_model()
    df = get_period_modelData(start, end)
    result = predict(df, classifier)
    return result

