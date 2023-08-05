import requests
from fake_useragent import UserAgent
import pandas as pd
import re

ua = UserAgent(use_cache_server=True)
headers = {'User-Agent': ua.random}

file_names = open('../data/file_names/jeju_racing_results_file_names.txt', 'r').read()

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

# print(file_list)
#
# # 서울
# for date in file_list:
#     url = f'https://race.kra.co.kr/dbdata/fileDownLoad.do?fn=chollian/seoul/jungbo/rcresult/{date}dacom11.rpt&meet=1'
#
#     # get data from url
#     r = requests.get(url, headers=headers)
#
#     textData = r.text
#
#     # save data to file
#     with open(f'../data/racing_results/raw_text/seoul/seoul_{date}.txt', 'w') as f:
#         f.write(textData)
#
#     # read data from file
#     fwfData = pd.read_fwf(url, header=None, widths=[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], encoding='cp949')
#     fwfData.to_csv(f'../data/racing_results/raw_fwf/seoul/seoul_{date}.csv', index=False, header=False, encoding='cp949')
#
#     print(f'{date} is done')
#
# print('All done')



for date in file_list:
    # 제주
    url = f'https://race.kra.co.kr/dbdata/fileDownLoad.do?fn=chollian/jeju/jungbo/rcresult/{date}dacom11.rpt&meet=2'

    # get data from url
    r = requests.get(url, headers=headers)

    textData = r.text

    # save data to file
    if len(textData) > 0:
        with open(f'../data/racing_results/raw_text/jeju/jeju_{date}.txt', 'w') as f:
            f.write(textData)
    else:
        print(f'{date} is empty')

    # read data from file
    try:
        fwfData = pd.read_fwf(url, header=None, widths=[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], encoding='cp949')
        fwfData.to_csv(f'../data/racing_results/raw_fwf/jeju/jeju_{date}.csv', index=False, header=False, encoding='cp949')
    except:
        print(f'{date} is empty')
    print(f'{date} is done')

print('All done')

# 경북
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


for date in file_list:
    # 부산
    url = f'https://race.kra.co.kr/dbdata/fileDownLoad.do?fn=chollian/busan/jungbo/rcresult/{date}dacom11.rpt&meet=3'

    # get data from url
    r = requests.get(url, headers=headers)

    textData = r.text

    # save data to file
    if len(textData) > 0:
        with open(f'../data/racing_results/raw_text/busan/busan_{date}.txt', 'w') as f:
            f.write(textData)
    else:
        print(f'{date} is empty')

    # read data from file
    try:
        fwfData = pd.read_fwf(url, header=None, widths=[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], encoding='cp949')
        fwfData.to_csv(f'../data/racing_results/raw_fwf/busan/busan_{date}.csv', index=False, header=False, encoding='cp949')
    except:
        print(f'{date} is empty')


    print(f'{date} is done')