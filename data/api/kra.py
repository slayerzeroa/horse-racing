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
import time


encoding_key, decoding_key = get_env('KRA')

# About rcPlan
# 경기계획
def get_yearly_rcPlan(pageNo, numOfRows, raceYear):
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    params = {'serviceKey': decoding_key, 'pageNo': pageNo, 'numOfRows': numOfRows, 'rc_year': raceYear, '_type': 'json'}
    df = tools.json2pandas(url, params)
    df = preprocess_rcPlan(df)
    return df

def get_daily_rcPlan(rc_date, meet):
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    params = {'serviceKey': decoding_key, 'pageNo': 1, 'numOfRows': 50, 'rc_date': rc_date, 'meet': meet, '_type': 'json'}
    df = tools.json2pandas(url, params)
    df = preprocess_rcPlan(df)
    return df

def get_all_rcPlan(raceYear):
    result = pd.DataFrame()
    for i in range(1, 100):
        try:
            result = pd.concat([result, get_yearly_rcPlan(i, 50, raceYear)])
        except:
            break
    return result


def preprocess_rcPlan(df):
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
def get_rcDate_from_db()->list:
    result = []

    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # rcPlan 테이블에 있는 모든 rcDate를 가져옴
    sql = "SELECT rcDate FROM rcPlan"
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

def get_closest_rcDate(meet)->str:
    # 날짜만 yyyymmdd 형식
    today = datetime.datetime.today()
    for _ in range(10):
        today_str = today.strftime('%Y%m%d')
        try:
            df = get_daily_rcPlan(today_str, meet)
            return today_str
        except:
            pass
        finally:
            today -= datetime.timedelta(days=1)

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

    params = tools.exclude_none(params)
    df = tools.json2pandas(url, params)
    df = preprocess_rcResult(df)
    return df


def get_daily_rcResult(meet, rc_date):
    result = pd.DataFrame()
    for i in range(1, 10):
        try:
            df = get_rcResult(i, 50, meet, rc_date, None)
            result = pd.concat([result, df])
        except:
            pass
    return result


def get_daily_rcId(meet, rc_date):
    df = get_daily_rcResult(meet, rc_date)
    rcId = df['rcId'].unique().tolist()
    return rcId

def get_all_rcResult(start, end):
    result = pd.DataFrame()
    for meet in [1, 2, 3]:
        for rc_date in get_rcDate_from_db():
            if start <= rc_date <= end:
                try:
                    df = get_daily_rcResult(meet, rc_date)
                    result = pd.concat([result, df])
                except:
                    pass
    return result

# df = get_all_rcResult('20240607', '20240609')
# print(df)

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
    df['rcDate_bin'] = df['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
    # 빈 DataFrame 생성
    rcDate_diff = pd.DataFrame()
    # 마명별로 rcDate_diff 계산
    for hrn in horse_name:
        rcDate_diff = pd.concat([rcDate_diff, df[df['hrName'] == hrn].rcDate_bin.diff()], axis=0)
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

    # # 7년 내 데이터만 가져옴
    # df = df[df['rcDate'] >= (datetime.datetime.now() - datetime.timedelta(days=365*7)).strftime('%Y-%m-%d')]
    df = preprocess_for_model_data(df)
    df = cal_rcDate_diff(df)
    df = calculate_past_avg_speed(df)
    df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist', 'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]

    df = df.sort_values(by=['rcId', 'globalUnique'])
    return df


'''숙제'''
# hrNo의 rcDate_diff 계산하는 함수
# hrNo의 avg_past_speed 계산하는 함수

def get_rcDate_diff_from_db(hrNo):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()
    # hrNo 열 값이 hrName인 데이터만 가져옴
    data_sql = f"SELECT * FROM rcResult WHERE hrNo={hrNo}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    df = df.sort_values(by=['rcDate'])
    df['rcDate_bin'] = df['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
    # 마지막 경기 날짜와의 차이 한 개의 값만 가져옴
    df['rcDate_diff'] = df['rcDate_bin'].diff()
    df['rcDate_diff'] = df['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
    df['rcDate_diff'].replace({pd.NaT: 99999}, inplace=True)
    df['rcDate_diff'] = df['rcDate_diff'].fillna(99999).astype(int)

    rcDate_diff = df['rcDate_diff'].iloc[-1]
    return rcDate_diff

def get_avg_past_speed_from_db(hrNo):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()
    # hrName 열 값이 hrName인 데이터만 가져옴
    data_sql = f"SELECT * FROM rcResult WHERE hrNo={hrNo}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    df = df.sort_values(by=['rcDate'])
    df = cal_speed(df)
    df['avg_past_speed'] = df['speed'].expanding().mean().shift(1)
    # 마지막 경기의 평균 속도만 가져옴
    avg_past_speed = df['avg_past_speed'].iloc[-1]
    return avg_past_speed

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

def get_modelData_period(meet, start, end):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()
    # meet 열 값이 meet인 데이터만 가져옴
    data_sql = f"SELECT * FROM model WHERE meet={meet} AND rcDate BETWEEN {start} AND {end}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'model'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    return df

# start부터 end까지의 모델 데이터 가져오기
def get_all_modelData(start, end):
    host, user, password, db = get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # rcDate가 start부터 end까지의 값 가져오기
    data_sql = f"SELECT * FROM rcResult WHERE rcDate BETWEEN {start} AND {end}"
    curs.execute(data_sql)
    data_rows = curs.fetchall()

    # column 이름 가져오기
    columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
    curs.execute(columns_sql)
    columns = curs.fetchall()

    conn.close()

    df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
    hrNo_list = df['hrNo'].tolist()
    df = preprocess_for_model_data(df)

    rcDate_diff_list = []
    avg_past_speed_list = []
    for hrNo in hrNo_list:
        aps, rd = get_aps_rd(hrNo, None)
        avg_past_speed_list.append(aps)
        rcDate_diff_list.append(rd)

    df['rcDate_diff'] = rcDate_diff_list
    df['avg_past_speed'] = avg_past_speed_list

    df = df[
        ['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist',
         'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]

    return df



def get_hrRecord(hrNo, hrName):
    result = pd.DataFrame()
    url = 'http://apis.data.go.kr/B551015/API37_1/sectionRecord_1'

    for i in range(1, 5):
        try:
            params = {'serviceKey': decoding_key, 'pageNo': i, 'numOfRows': 50, 'hr_no':hrNo, 'hr_name':hrName, '_type': 'json'}
            params = tools.exclude_none(params)

            df = tools.json2pandas(url, params)
            result = pd.concat([result, df])
        except:
            break

    result['speed'] = result['rcDist'] / result['rcTime']
    result['avg_past_speed'] = result['speed'].expanding().mean().shift(1)
    result['rcDate_bin'] = result['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
    result['rcDate_diff'] = result['rcDate_bin'].diff()
    result['rcDate_diff'] = result['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
    result = result.drop(['rcDate_bin'], axis=1)
    return result


# average past speed, rcDate_diff
def get_aps_rd(hrNo, hrName):
    df = get_hrRecord(hrNo, hrName)
    return df['avg_past_speed'].iloc[-1], df['rcDate_diff'].iloc[-1]

