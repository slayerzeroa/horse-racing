import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
from json_to_pandas import json2pandas
from list_of_url import urls
import re
import time


encoding_key = "aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3%2BbNdINTAIQFTzdMNfpD%2FaemMvFyVQ%3D%3D"
decoding_key = "aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3+bNdINTAIQFTzdMNfpD/aemMvFyVQ=="

# 경주기록정보
url = "http://apis.data.go.kr/B551015/horseecgsensor/gethorseecgsensor"

params = {
    "serviceKey": decoding_key,
    "pageNo": 1,
    "numOfRows": 2000000,
    "meet": 3,
    # "mesur_dy": 20210722,
    "hr_no": "0039575",
    "_type": "json"
}

df = json2pandas(url, params)
print(df)

# df.to_csv("../data/horse_training/heart_rate/horse_training_heart_rate.csv", index=False, encoding="utf-8-sig")