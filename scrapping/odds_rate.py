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
url = "http://apis.data.go.kr/B551015/API160_1/integratedInfo_1"


file_names = open('../data/file_names/busan_racing_results_file_names.txt', 'r').read()

# change \n to \t
file_names = re.sub('\n', ' ', file_names)

# change many \t to one \t
file_names = re.sub('\t', ' ', file_names)
file_names = re.sub(' +', ' ', file_names)

# split by ' '
file_names = file_names.split(' ')

file_list = []
for idx, i in enumerate(file_names):
    if idx % 2 == 0:
        file_list.append(i[:8])


result_df = pd.DataFrame()
for date in file_list:
    try:
        params = {
            "serviceKey": decoding_key,
            "pageNo": 1,
            "numOfRows": 200000,
            "meet": 3,
            "rc_date": date,
            "_type": "json"
        }

        df = json2pandas(url, params)
        print(df)
        result_df = pd.concat([result_df, df])
    except:
        continue

    print(df)
    time.sleep(1)



result_df.to_csv('../data/odds/busan/busan_racing_odds.csv', index=False, encoding='utf-8-sig')
