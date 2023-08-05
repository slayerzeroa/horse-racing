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
url = "http://apis.data.go.kr/B551015/API37_1/sectionRecord_1"


file_names = open('../data/file_names/seoul_racing_results_file_names.txt', 'r').read()

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


results = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')
horse_name_list = results['hrName'].unique().tolist()


params = {
    "serviceKey": decoding_key,
    "pageNo": 1,
    "numOfRows": 1000,
    "hr_name": horse_name_list[1],
    "meet": 1,
    "rc_date": 20230805,
    "_type": "json"
}

df = json2pandas(url, params)


# result_df = pd.DataFrame()
# for date in file_list:
#     try:
#         params = {
#             "serviceKey": decoding_key,
#             "pageNo": 1,
#             "numOfRows": 200,
#             "meet": 1,
#             "rc_date": date,
#             "_type": "json"
#         }
#         df = json2pandas(url, params)
#         result_df = pd.concat([result_df, df])
#     except:
#         continue
#     print(df)
#     time.sleep(1)
#
#
# result_df.to_csv('../data/odds/busan/busan_racing_odds.csv', index=False, encoding='utf-8-sig')
