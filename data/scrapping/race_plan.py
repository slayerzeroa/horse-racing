import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
from json_to_pandas import json2pandas
from list_of_url import urls
import re
import time

# pd columns 모두 출력
pd.set_option('display.max_columns', None)

encoding_key = "aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3%2BbNdINTAIQFTzdMNfpD%2FaemMvFyVQ%3D%3D"
decoding_key = "aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3+bNdINTAIQFTzdMNfpD/aemMvFyVQ=="

# 한국마사회 경주계획표
url = "http://apis.data.go.kr/B551015/API23_1/entryRaceHorse_1"

params = {
    "serviceKey": decoding_key,
    "pageNo": 1,
    "numOfRows": 1000,
    "meet": 1,
    "rc_date": '20231222',
    "_type": "json"
}

df = json2pandas(url, params)
today = 20231209
df = df[(df['pgDate'] == today) & (df['pgNo'] == 6)]
hr_list = (list(map(int, df.hrNo.unique())))
from sklearn.preprocessing import LabelEncoder
race_df = pd.read_csv('C:/Users/slaye/PycharmProjects/Horse_Racing/data/datasets/test/seoul_horse_records.csv')
race_df = race_df.drop(['jkName', 'rcNo', 'rcTime', 'speed', 'rcTime_mean', 'weather'], axis=1)
le = LabelEncoder()
race_df['sex'] = le.fit_transform(race_df['sex'])

# print(race_df)

race_sheet = pd.DataFrame()
for hrNo in hr_list:
    try:
        race_sheet = pd.concat([race_sheet, (race_df[race_df['hrNo'] == hrNo].iloc[-1])], axis=1)
    except:
        continue
from datetime import datetime
race_sheet = race_sheet.T
race_sheet['rcDate_diff'] = race_sheet['rcDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').date()) - datetime.strptime(str(today), '%Y%m%d').date()
race_sheet['rcDate_diff'] = race_sheet['rcDate_diff'].apply(lambda x: float(str(x).split(' ')[0]))

import numpy as np
# race sheet inf -> mean
race_sheet = race_sheet.replace([np.inf, -np.inf], np.nan)
race_sheet = race_sheet.fillna(race_sheet.mean())
print(race_sheet)
from xgboost import XGBClassifier
classifier = XGBClassifier() # 모델 초기화
classifier.load_model('../../models/tree_model/boosting_model/xgb_model.model') # 모델 불러오기

X = race_sheet.drop(['ord'], axis=1)
y_pred = classifier.predict(X)

race_sheet['predict'] = y_pred
print(race_sheet)
