import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
import datetime

from dotenv import load_dotenv
import os

def json2df(response_json):
    df = pd.json_normalize(response_json['response']['body']['items']['item'])
    return df

def get_api_url_list():
    urls = {"기수성적": "http://apis.data.go.kr/B551015/API11_1/jockeyResult_1",
            "경주마성적": "http://apis.data.go.kr/B551015/API15_2/raceHorseResult_2",
            "확정배당율": "http://apis.data.go.kr/B551015/API160_1/integratedInfo_1", }

    return urls


'''
api_name: "KRA"(마사회), output: encoding_key, decoding_key
'''
def get_env(env):
    load_dotenv()
    if env == 'KRA':
        KRA_ENCODING = os.getenv("KRA_ENCODING")
        KRA_DECODING = os.getenv("KRA_DECODING")
        return KRA_ENCODING, KRA_DECODING

    elif env == 'DB':
        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")
        return DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

    elif env == 'TELEGRAM':
        TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
        TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        return TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def location_to_meet(location):
    if location == '서울':
        return 1
    elif location == '제주':
        return 2
    elif location == '부산경남':
        return 3
    else:
        return None

def preprocess_rcNo(x):
    if x < 10:
        return '0' + str(x)
    else:
        return str(x)

# value값이 None이면 해당 key를 제외하는 함수
def exclude_none(params):
    result = {}
    for key, value in params.items():
        if value is not None:
            result[key] = value
    return result


def get_start_end():
    # 오늘 날짜 연월일
    today = datetime.datetime.today()
    start = today
    end = today + datetime.timedelta(days=10)
    start = start.strftime('%Y%m%d')
    end = end.strftime('%Y%m%d')
    return start, end


def filter_only_winner(df):
    df = df[df['pred'] == 1]
    return df


# 이전 경기 날짜와의 차이 계산
def cal_rcDate_diff(df):
    # 마명 추출
    horse_name = df['hrName'].unique().tolist()
    # 자료형 변경
    df['rcDate'] = df['rcDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').date())
    # 빈 DataFrame 생성
    rcDate_diff = pd.DataFrame()
    # 마명별로 rcDate_diff 계산
    for hrn in horse_name:
        rcDate_diff = pd.concat([rcDate_diff, df[df['hrName'] == hrn].rcDate.diff()], axis=0)
    rcDate_diff.sort_index(inplace=True)
    df['rcDate_diff'] = rcDate_diff
    return 

def cal_mean_speed(speed_list):
    mean_speed_list = []
    for _ in range(len(speed_list)):
        mean_speed = np.mean(speed_list[:_+1])
        mean_speed_list.append(mean_speed)
    return mean_speed_list