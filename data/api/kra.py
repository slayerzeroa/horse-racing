import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

import pandas as pd

import json

import tools
from tools import *

import re
import time

import pymysql

import datetime


encoding_key, decoding_key = get_env('KRA')

# About rcData
# 경주정보 (언제, 어떤 경기를 하는지)
def get_rcData(pageNo, numOfRows, raceYear):
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    params = {'serviceKey': encoding_key, 'pageNo': pageNo, 'numOfRows': numOfRows, 'rc_year': raceYear, '_type': 'json'}
    df = tools.json2pandas(url, params)
    df = preprocess_rcData(df)
    return df

def get_update_rcData(rc_date):
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    params = {'serviceKey': encoding_key, 'pageNo': 1, 'numOfRows': 50, 'rc_date': rc_date, '_type': 'json'}
    df = tools.json2pandas(url, params)
    df = preprocess_rcData(df)
    return df

def get_all_rcData(raceYear):
    result = pd.DataFrame()
    for i in range(1, 100):
        try:
            result = pd.concat([result, get_rcData(i, 50, raceYear)])
        except:
            break
    return result


def preprocess_rcData(df):
    # rcId = rcDate + meet + rcNo
    # 시행경마장구분(1:서울 2:제주 3:부산)
    df['rcDate'] = df['rcDate'].astype(str)

    df['meet'] = df['meet'].apply(lambda x: location_to_meet(x))
    df['meet'] = df['meet'].astype(str)

    df['rcNo'] = df['rcNo'].apply(lambda x: preprocess_rcNo(x))
    df['rcNo'] = df['rcNo'].astype(str)

    df['rcId'] = df['rcDate'] + df['meet'] + df['rcNo']

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    return df


# 경주날짜 가져오기
def get_rcDate()->list:
    result = []

    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # rcData 테이블에 있는 모든 rcDate를 가져옴
    sql = "SELECT rcDate FROM rcData"
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()

    for row in rows:
        result.append(row[0])


    # unique한 값만 남김
    result = list(set(result))

    # 오름차순 정렬
    result.sort(reverse=True)

    return result



#  경주기록 정보
def preprocess_rcResult(df):
    # globalUnique = rcDate + meet + rcNo + hrNo
    # rcId = rcDate + meet + rcNo
    # 시행경마장구분(1:서울 2:제주 3:부산)
    df['rcDate'] = df['rcDate'].astype(str)

    df['meet'] = df['meet'].apply(lambda x: location_to_meet(x))
    df['meet'] = df['meet'].astype(str)

    df['rcNo'] = df['rcNo'].apply(lambda x: preprocess_rcNo(x))
    df['rcNo'] = df['rcNo'].astype(str)

    df['hrNo'] = df['hrNo'].astype(str)

    df['globalUnique'] = df['rcDate'] + df['meet'] + df['rcNo'] + df['hrNo']
    df['rcId'] = df['rcDate'] + df['meet'] + df['rcNo']

    # rcName 제거
    df = df.drop(['rcName'], axis=1)

    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]

    return df



def get_rcResult(pageNo, numOfRows, meet, rc_date, rc_no):
    url = "http://apis.data.go.kr/B551015/API4_2/raceResult_2"
    params = {
        "serviceKey": decoding_key,
        "pageNo": pageNo,
        "numOfRows": numOfRows,
        "meet": meet,
        "rc_date": rc_date,
        "rc_no": rc_no,
        "_type": "json"
    }
    df = tools.json2pandas(url, params)
    df = preprocess_rcResult(df)
    return df




# 모델용 데이터
def get_rcResult_from_db(meet):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()
    # meet 열이 2인 데이터만 가져옴
    data_sql = f"SELECT * FROM rcResult WHERE meet={meet}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    return df


# 'rcDate_diff','rcTime_mean',
def preprocess_for_model_data(df):
    df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcTime', 'rcDist',  'sex',  'ord', 'winOdds', 'plcOdds']]
    return df

# 이전 경기 날짜와의 차이 계산
# rcDate_diff
def cal_rcDate_diff(df):
    # 마명 추출
    horse_name = df['hrName'].unique().tolist()
    # 자료형 변경
    df['rcDate'] = df['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
    # 빈 DataFrame 생성
    rcDate_diff = pd.DataFrame()
    # 마명별로 rcDate_diff 계산
    for hrn in horse_name:
        rcDate_diff = pd.concat([rcDate_diff, df[df['hrName'] == hrn].rcDate.diff()], axis=0)
    rcDate_diff.sort_index(inplace=True)
    df['rcDate_diff'] = rcDate_diff
    return df

def cal_speed(df):
    df['speed'] = df['rcDist'].astype(int) / df['rcTime'].astype(float)
    return df


# 마명별 과거 경기의 평균 속도 계산

def calculate_past_avg_speed(df):
    df = cal_speed(df)

    # 경주일자 기준으로 정렬
    df = df.sort_values(by=['hrName', 'rcDate'])

    # 각 말의 이전 경기들의 평균 속도를 계산
    df['avg_past_speed'] = df.groupby('hrName')['speed'].transform(lambda x: x.expanding().mean().shift(1))

    return df


def get_modelData(meet):
    df = get_rcResult_from_db(meet)
    df = preprocess_for_model_data(df)
    df = cal_rcDate_diff(df)
    df = calculate_past_avg_speed(df)
    df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist', 'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]
    return df

def get_modelData_from_db(meet):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()
    # meet 열 값이 meet인 데이터만 가져옴
    data_sql = f"SELECT * FROM model WHERE meet={meet}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'model'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    return df