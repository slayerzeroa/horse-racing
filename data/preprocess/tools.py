import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd

def json2pandas(url, params):
    r = urlopen(Request(url + '?' + urlencode(params)))
    json_api = r.read().decode('utf-8')
    json_file = json.loads(json_api)
    df = pd.json_normalize(json_file['response']['body']['items']['item'])
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
    if env == 'KRA':
        path = ('C:/Users/slaye/PycharmProjects/Horse_Racing/env/kra_api.txt')
        with open(path, 'r') as f:
            encoding_key = f.readline().strip()
            decoding_key = f.readline().strip()
        return encoding_key, decoding_key

    elif env == 'DB':
        path = ('C:/Users/slaye/PycharmProjects/Horse_Racing/env/db_env.txt')
        with open(path, 'r') as f:
            host = f.readline().strip()
            user = f.readline().strip()
            password = f.readline().strip()
            db = f.readline().strip()
        return host, user, password, db


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