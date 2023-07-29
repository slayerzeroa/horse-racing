import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd


encoding_key = "	aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3%2BbNdINTAIQFTzdMNfpD%2FaemMvFyVQ%3D%3D"

url = "http://apis.data.go.kr/B551015/API214_1/RaceDetailResult_1"


params = {
    "serviceKey": encoding_key,
    "pageNo": 1,
    "numOfRows": 10,
    "meet": 1,
    "rc_date": '20230722',
    "rc_no": 3,
    "_type": "json"
}

r = urlopen(Request(url + '?' + urlencode(params)))
# r = requests.get(url, params=params)
json_api = r.read().decode('utf-8')

json_file = json.loads(json_api)
print(json_file)

df = pd.json_normalize(json_file['response']['body']['items']['item'])
print(df)