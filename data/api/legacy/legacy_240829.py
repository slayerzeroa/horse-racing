# import requests
# from urllib.request import Request, urlopen
# from urllib.parse import urlencode, quote_plus

# import pandas as pd

# import json

# from data.preprocess import tools

# import re
# import time

# import pymysql

# import datetime
# import time



# encoding_key, decoding_key = tools.get_env('KRA')


# '''경기계획'''
# def get_yearly_rcPlan(pageNo, numOfRows, raceYear):
#     url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
#     params = {'serviceKey': decoding_key, 'pageNo': pageNo, 'numOfRows': numOfRows, 'rc_year': raceYear, '_type': 'json'}
#     df = tools.json2df(url, params)
#     df = preprocess_rcPlan(df)
#     return df

# def get_daily_rcPlan(rc_date, meet):
#     url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
#     params = {'serviceKey': decoding_key, 'pageNo': 1, 'numOfRows': 50, 'rc_date': rc_date, 'meet': meet, '_type': 'json'}
#     df = tools.json2df(url, params)
#     df = preprocess_rcPlan(df)
#     return df

# def get_every_rcPlan():
#     result = pd.DataFrame()
#     for rcYear in range(2010, 2024):
#         for i in range(1, 100):
#             try:
#                 result = pd.concat([result, get_yearly_rcPlan(i, 50, rcYear)])
#             except:
#                 break
#     return result


# def preprocess_rcPlan(df):
#     # rcId = rcDate + meet + rcNo
#     # 시행경마장구분(1:서울 2:제주 3:부산)
#     df['rcDate'] = df['rcDate'].astype(str)

#     df['meet'] = df['meet'].apply(lambda x: tools.location_to_meet(x))
#     df['meet'] = df['meet'].astype(str)

#     df['rcNo'] = df['rcNo'].apply(lambda x: tools.preprocess_rcNo(x))
#     df['rcNo'] = df['rcNo'].astype(str)

#     df['rcId'] = df['rcDate'] + df['meet'] + df['rcNo']

#     cols = df.columns.tolist()
#     cols = cols[-1:] + cols[:-1]
#     df = df[cols]

#     return df


# '''경주날짜'''
# def get_rcDate_from_db()->list:
#     result = []

#     host, user, password, db = tools.get_env('DB')

#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()

#     # rcPlan 테이블에 있는 모든 rcDate를 가져옴
#     sql = "SELECT rcDate FROM rcPlan"
#     curs.execute(sql)
#     rows = curs.fetchall()
#     conn.close()

#     for row in rows:
#         result.append(row[0])


#     # unique한 값만 남김
#     result = list(set(result))

#     # 오름차순 정렬
#     result.sort(reverse=True)

#     return result

# # 가장 가까운 경기 날짜
# # input: meet(1: 서울, 2: 제주, 3: 부경)
# def get_closest_rcDate(meet)->str:
#     # 날짜만 yyyymmdd 형식
#     today = datetime.datetime.today()
#     for _ in range(10):
#         today_str = today.strftime('%Y%m%d')
#         try:
#             df = get_daily_rcPlan(today_str, meet)
#             return today_str
#         except:
#             pass
#         finally:
#             today -= datetime.timedelta(days=1)


# '''경주결과'''
# def preprocess_rcResult(df):
#     # globalUnique = rcDate + meet + rcNo + hrNo
#     # rcId = rcDate + meet + rcNo
#     # 시행경마장구분(1:서울 2:제주 3:부산)
#     df['rcDate'] = df['rcDate'].astype(str)

#     df['meet'] = df['meet'].apply(lambda x: tools.location_to_meet(x))
#     df['meet'] = df['meet'].astype(str)

#     df['rcNo'] = df['rcNo'].apply(lambda x: tools.preprocess_rcNo(x))
#     df['rcNo'] = df['rcNo'].astype(str)

#     df['hrNo'] = df['hrNo'].astype(str)

#     df['globalUnique'] = df['rcDate'] + df['meet'] + df['rcNo'] + df['hrNo']
#     df['rcId'] = df['rcDate'] + df['meet'] + df['rcNo']

#     # rcName 제거
#     df = df.drop(['rcName'], axis=1)

#     cols = df.columns.tolist()
#     cols = cols[-2:] + cols[:-2]
#     df = df[cols]

#     return df


# # 경주결과 가져오기
# def get_rcResult(pageNo, numOfRows, meet, rc_date, rc_no):
#     url = "http://apis.data.go.kr/B551015/API4_2/raceResult_2"

#     params = {
#         "serviceKey": decoding_key,
#         "pageNo": pageNo,
#         "numOfRows": numOfRows,
#         "meet": meet,
#         "rc_date": rc_date,
#         "rc_no": rc_no,
#         "_type": "json"
#     }

#     params = tools.exclude_none(params)
#     print(params)
#     df = tools.json2df(url, params)
#     print(df)
#     df = preprocess_rcResult(df)
#     return df




# # 일별 경주결과 가져오기
# def get_daily_rcResult(meet, rc_date):
#     result = pd.DataFrame()
#     for i in range(1, 10):
#         try:
#             df = get_rcResult(i, 50, meet, rc_date, None)
#             result = pd.concat([result, df])
#         except:
#             break
#     return result

# # print(get_daily_rcResult(1, '20240615'))


# # 일별 경주ID 가져오기 (Unique in rcPlan)
# def get_daily_rcId(meet, rc_date):
#     df = get_daily_rcResult(meet, rc_date)
#     rcId = df['rcId'].unique().tolist()
#     return rcId


# # start부터 end까지의 경주결과 가져오기
# def get_period_rcResult(start=None, end=None, meet=None):
#     if meet is None:
#         if (start == None) and (end == None):
#             result = pd.DataFrame()
#             for meet in [1, 2, 3]:
#                 for rc_date in get_rcDate_from_db():
#                     try:
#                         df = get_daily_rcResult(meet, rc_date)
#                         result = pd.concat([result, df])
#                     except:
#                         pass
#         if (start == None) and (end != None):
#             result = pd.DataFrame()
#             for meet in [1, 2, 3]:
#                 for rc_date in get_rcDate_from_db():
#                     if rc_date <= end:
#                         try:
#                             df = get_daily_rcResult(meet, rc_date)
#                             result = pd.concat([result, df])
#                         except:
#                             pass
#         if (start != None) and (end == None):
#             result = pd.DataFrame()
#             for meet in [1, 2, 3]:
#                 for rc_date in get_rcDate_from_db():
#                     if start <= rc_date:
#                         try:
#                             df = get_daily_rcResult(meet, rc_date)
#                             result = pd.concat([result, df])
#                         except:
#                             pass
#         if (start != None) and (end != None):
#             result = pd.DataFrame()
#             for meet in [1, 2, 3]:
#                 for rc_date in get_rcDate_from_db():
#                     if start <= rc_date <= end:
#                         df = get_daily_rcResult(meet, rc_date)
#                         result = pd.concat([result, df])

#     else:
#         if (start == None) and (end == None):
#             result = pd.DataFrame()
#             for rc_date in get_rcDate_from_db():
#                 try:
#                     df = get_daily_rcResult(meet, rc_date)
#                     result = pd.concat([result, df])
#                 except:
#                     pass
#         if (start == None) and (end != None):
#             result = pd.DataFrame()
#             for rc_date in get_rcDate_from_db():
#                 if rc_date <= end:
#                     try:
#                         df = get_daily_rcResult(meet, rc_date)
#                         result = pd.concat([result, df])
#                     except:
#                         pass
#         if (start != None) and (end == None):
#             result = pd.DataFrame()
#             for rc_date in get_rcDate_from_db():
#                 if start <= rc_date:
#                     try:
#                         df = get_daily_rcResult(meet, rc_date)
#                         result = pd.concat([result, df])
#                     except:
#                         pass
#         if (start != None) and (end != None):
#             result = pd.DataFrame()
#             for rc_date in get_rcDate_from_db():
#                 if start <= rc_date <= end:
#                     try:
#                         df = get_daily_rcResult(meet, rc_date)
#                         result = pd.concat([result, df])
#                     except:
#                         pass

#     return result


# # rcResult 데이터를 db에서 받아오는 함수
# def get_period_rcResult_from_db(start=None, end=None, meet=None):
#     host, user, password, db = tools.get_env('DB')

#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()
#     # meet 열 값이 meet인 데이터와 rcDate가 start부터 end까지의 데이터만 가져옴

#     if meet == None:
#         if (start == None) and (end == None):
#             data_sql = f"SELECT * FROM rcResult"
#         if (start == None) and (end != None):
#             data_sql = f"SELECT * FROM rcResult WHERE rcDate<={end}"
#         if (start != None) and (end == None):
#             data_sql = f"SELECT * FROM rcResult WHERE rcDate>={start}"
#         if (start != None) and (end != None):
#             data_sql = f"SELECT * FROM rcResult WHERE rcDate BETWEEN {start} AND {end}"
#     else:
#         if (start == None) and (end == None):
#             data_sql = f"SELECT * FROM rcResult WHERE meet={meet}"
#         if (start == None) and (end != None):
#             data_sql = f"SELECT * FROM rcResult WHERE meet={meet} AND rcDate<={end}"
#         if (start != None) and (end == None):
#             data_sql = f"SELECT * FROM rcResult WHERE meet={meet} AND rcDate>={start}"
#         if (start != None) and (end != None):
#             data_sql = f"SELECT * FROM rcResult WHERE rcDate BETWEEN {start} AND {end} AND meet={meet}"

#     curs.execute(data_sql)
#     data_rows = curs.fetchall()

#     # column 이름 가져오기
#     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
#     curs.execute(columns_sql)
#     columns = curs.fetchall()

#     conn.close()

#     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
#     return df

# def get_every_rcResult():
#     result = pd.DataFrame()
#     for rc_date in get_rcDate_from_db():
#         for meet in [1, 2, 3]:
#             for i in range(1, 20):
#                 try:
#                     df = get_rcResult(i, 50, meet, rc_date, None)
#                     result = pd.concat([result, df])
#                 except:
#                     break
#     return result

# # 이전 경기 날짜와의 차이 계산
# # rcDate_diff
# def cal_rcDate_diff(df):
#     # 마명 추출
#     horse_name = df['hrName'].unique().tolist()
#     # 자료형 변경
#     df['rcDate_bin'] = df['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
#     # 빈 DataFrame 생성
#     rcDate_diff = pd.DataFrame()
#     # 마명별로 rcDate_diff 계산
#     for hrn in horse_name:
#         rcDate_diff = pd.concat([rcDate_diff, df[df['hrName'] == hrn].rcDate_bin.diff()], axis=0)
#     rcDate_diff.sort_index(inplace=True)
#     df['rcDate_diff'] = rcDate_diff
#     return df

# def cal_speed(df):
#     df['speed'] = df['rcDist'].astype(int) / df['rcTime'].astype(float)
#     return df

# # 마명별 과거 경기의 평균 속도 계산
# def calculate_past_avg_speed(df):
#     df = cal_speed(df)

#     # 경주일자 기준으로 정렬
#     df = df.sort_values(by=['hrName', 'rcDate'])

#     # 각 말의 이전 경기들의 평균 속도를 계산
#     df['avg_past_speed'] = df.groupby('hrName')['speed'].transform(lambda x: x.expanding().mean().shift(1))

#     return df

# def get_every_modelData():
#     df = get_period_rcResult()
#     df = preprocess_for_modelData(df)
#     df = cal_rcDate_diff(df)
#     df = calculate_past_avg_speed(df)
#     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist', 'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]

#     df = df.sort_values(by=['rcId', 'globalUnique'])
#     df = df.reset_index(drop=True)
#     return df


# def get_rcDate_diff_from_db(hrNo):
#     host, user, password, db = tools.get_env('DB')

#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()
#     # hrNo 열 값이 hrName인 데이터만 가져옴
#     data_sql = f"SELECT * FROM rcResult WHERE hrNo={hrNo}"
#     curs.execute(data_sql)
#     data_rows = curs.fetchall()

#     # column 이름 가져오기
#     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
#     curs.execute(columns_sql)
#     columns = curs.fetchall()

#     conn.close()

#     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
#     df = df.sort_values(by=['rcDate'])
#     df['rcDate_bin'] = df['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
#     # 마지막 경기 날짜와의 차이 한 개의 값만 가져옴
#     df['rcDate_diff'] = df['rcDate_bin'].diff()
#     df['rcDate_diff'] = df['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
#     df['rcDate_diff'].replace({pd.NaT: 99999}, inplace=True)
#     df['rcDate_diff'] = df['rcDate_diff'].fillna(99999).astype(int)

#     rcDate_diff = df['rcDate_diff'].iloc[-1]
#     return rcDate_diff

# def get_avg_past_speed_from_db(hrNo):
#     host, user, password, db = tools.get_env('DB')

#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()
#     # hrName 열 값이 hrName인 데이터만 가져옴
#     data_sql = f"SELECT * FROM rcResult WHERE hrNo={hrNo}"
#     curs.execute(data_sql)
#     data_rows = curs.fetchall()

#     # column 이름 가져오기
#     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
#     curs.execute(columns_sql)
#     columns = curs.fetchall()

#     conn.close()

#     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
#     df = df.sort_values(by=['rcDate'])
#     df = cal_speed(df)
#     df['avg_past_speed'] = df['speed'].expanding().mean().shift(1)
#     # 마지막 경기의 평균 속도만 가져옴
#     avg_past_speed = df['avg_past_speed'].iloc[-1]
#     return avg_past_speed

# def get_modelData_from_db(meet=None):
#     host, user, password, db = tools.get_env('DB')

#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()

#     if meet == None:
#         data_sql = f"SELECT * FROM model"
#     else:
#         # meet 열 값이 meet인 데이터만 가져옴
#         data_sql = f"SELECT * FROM model WHERE meet={meet}"
#     curs.execute(data_sql)
#     data_rows = curs.fetchall()

#     # column 이름 가져오기
#     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'model'"
#     curs.execute(columns_sql)
#     columns = curs.fetchall()

#     conn.close()

#     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
#     return df


# def get_modelData_from_api(start=None, end=None, meet=None):
#     df = get_period_rcResult(start, end, meet)
#     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcTime', 'rcDist',  'sex',  'ord', 'winOdds', 'plcOdds']]
#     df = cal_rcDate_diff(df)
#     df = calculate_past_avg_speed(df)
#     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcTime', 'rcDist',  'sex',  'ord', 'winOdds', 'plcOdds']]
#     return df


# # def get_period_modelData(start, end, meet=None):
# #     host, user, password, db = get_env('DB')
# #
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #     curs = conn.cursor()
# #
# #     if meet == None:
# #         data_sql = f"SELECT * FROM model WHERE rcDate BETWEEN {start} AND {end}"
# #     else:
# #         data_sql = f"SELECT * FROM model WHERE meet={meet} AND rcDate BETWEEN {start} AND {end}"
# #     curs.execute(data_sql)
# #     data_rows = curs.fetchall()
# #
# #     # column 이름 가져오기
# #     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'model'"
# #     curs.execute(columns_sql)
# #     columns = curs.fetchall()
# #
# #     conn.close()
# #
# #     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
# #     return df


# def get_period_modelData(start=None, end=None, meet=None):
#     df = get_period_rcResult_from_db(start=start, end=end, meet=meet)
#     hrNo_list = df['hrNo'].tolist()
#     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcTime', 'rcDist',  'sex',  'ord', 'winOdds', 'plcOdds']]

#     rcDate_diff_list = []
#     avg_past_speed_list = []
#     for hrNo in hrNo_list:
#         aps, rd = get_aps_rd(hrNo, None)
#         avg_past_speed_list.append(aps)
#         rcDate_diff_list.append(rd)

#     df['rcDate_diff'] = rcDate_diff_list
#     df['avg_past_speed'] = avg_past_speed_list

#     df['rcDate_diff'] = df['rcDate_diff'].fillna(99999)
#     df['avg_past_speed'] = df['avg_past_speed'].fillna(-99999)

#     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist',
#              'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]
#     df = df.sort_values(by=['rcId', 'globalUnique'])
#     return df

# def get_hrRecord(hrNo, hrName):
#     result = pd.DataFrame()
#     url = 'http://apis.data.go.kr/B551015/API37_1/sectionRecord_1'

#     # for문: 한마리 말에 대한 모든 경주기록을 가져옴
#     for i in range(1, 5):
#         try:
#             params = {'serviceKey': decoding_key, 'pageNo': i, 'numOfRows': 50, 'hr_no':hrNo, 'hr_name':hrName, '_type': 'json'}
#             params = tools.exclude_none(params)

#             df = tools.json2df(url, params)
#             result = pd.concat([result, df])
#         except:
#             break
#     # print(result)
#     # 말이 첫 경기를 치르는 경우
#     if result.empty:
#         pass
#     else:
#         result['speed'] = result['rcDist'] / result['rcTime']
#         result['avg_past_speed'] = result['speed'].expanding().mean().shift(1)
#         result['rcDate_bin'] = result['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
#         result['rcDate_diff'] = result['rcDate_bin'].diff()
#         result['rcDate_diff'] = result['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
#         result = result.drop(['rcDate_bin'], axis=1)
#     return result

# # average past speed, rcDate_diff
# def get_aps_rd(hrNo, hrName):
#     df = get_hrRecord(hrNo, hrName)
#     if df.empty:
#         return -99999, 99999
#     return df['avg_past_speed'].iloc[-1], df['rcDate_diff'].iloc[-1]


# # def update_modelData(start=None, end=None, meet=None):
# #     df = pd.DataFrame()
# #     if meet is None:
# #         for meet in [1, 2, 3]:
# #             df = pd.concat([df, get_modelData(start, end, meet)])
# #     else:
# #         df = get_modelData(meet)
# #     df['rcDate_diff'] = df['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
# #     df['rcDate_diff'].replace({pd.NaT: 99999}, inplace=True)
# #     df['rcDate_diff'] = df['rcDate_diff'].fillna(99999).astype(int)
# #
# #     # avg_past_speed의 NaN 값을 -99999으로 대체
# #     df['avg_past_speed'] = df['avg_past_speed'].fillna(-99999)
# #     # DB에 저장
# #     host, user, password, db = get_env('DB')
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #     curs = conn.cursor()
# #
# #     for index, row in df.iterrows():
# #         update_values = []
# #         for col in df.columns:
# #             if col != 'globalUnique':  # Skip the primary key column
# #                 value = row[col]
# #                 if pd.isna(value):
# #                     value = 'NULL'
# #                 elif isinstance(value, str):
# #                     value = f"'{value}'"
# #                 else:
# #                     value = str(value)
# #                 update_values.append(f"{col} = {value}")
# #
# #         update_sql = f"UPDATE model SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
# #         curs.execute(update_sql)
# #
# #     conn.commit()
# #     conn.close()


# # start부터 end까지의 모델 데이터 가져오기

# #
# # def get_period_modelData(start=None, end=None, meet=None):
# #     host, user, password, db = get_env('DB')
# #
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #     curs = conn.cursor()
# #
# #     if meet == None:
# #         if (start == None) and (end == None):
# #             data_sql = f"SELECT * FROM model"
# #         if (start == None) and (end != None):
# #             data_sql = f"SELECT * FROM model WHERE rcDate<={end}"
# #         if (start != None) and (end == None):
# #             data_sql = f"SELECT * FROM model WHERE rcDate>={start}"
# #         if (start != None) and (end != None):
# #             data_sql = f"SELECT * FROM model WHERE rcDate BETWEEN {start} AND {end}"
# #     else:
# #         if (start == None) and (end == None):
# #             data_sql = f"SELECT * FROM model WHERE meet={meet}"
# #         if (start == None) and (end != None):
# #             data_sql = f"SELECT * FROM model WHERE meet={meet} AND rcDate<={end}"
# #         if (start != None) and (end == None):
# #             data_sql = f"SELECT * FROM model WHERE meet={meet} AND rcDate>={start}"
# #         if (start != None) and (end != None):
# #             data_sql = f"SELECT * FROM model WHERE meet={meet} AND rcDate BETWEEN {start} AND {end}"
# #
# #     curs.execute(data_sql)
# #     data_rows = curs.fetchall()
# #
# #     # column 이름 가져오기
# #     columns_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rcResult'"
# #     curs.execute(columns_sql)
# #     columns = curs.fetchall()
# #
# #     conn.close()
# #
# #     df = pd.DataFrame(data_rows, columns=[column[0] for column in columns])
# #     hrNo_list = df['hrNo'].tolist()
# #     df = preprocess_for_modelData(df)
# #
# #     rcDate_diff_list = []
# #     avg_past_speed_list = []
# #     for hrNo in hrNo_list:
# #         aps, rd = get_aps_rd(hrNo, None)
# #         avg_past_speed_list.append(aps)
# #         rcDate_diff_list.append(rd)
# #
# #     df['rcDate_diff'] = rcDate_diff_list
# #     df['avg_past_speed'] = avg_past_speed_list
# #
# #     df = df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist',
# #              'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]
# #
# #     return df
# def just_update_modelData(df):
#     host, user, password, db = tools.get_env('DB')
#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()

#     for index, row in df.iterrows():
#         update_values = []
#         for col in df.columns:
#             if col != 'globalUnique':  # Skip the primary key column
#                 value = row[col]
#                 if pd.isna(value):
#                     value = 'NULL'
#                 elif isinstance(value, str):
#                     value = f"'{value}'"
#                 else:
#                     value = str(value)
#                 update_values.append(f"{col} = {value}")

#         update_sql = f"UPDATE model SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
#         curs.execute(update_sql)

#     conn.commit()
#     conn.close()



# # 최종 DB 관련 함수

# # meet {1: 서울, 2: 제주, 3: 부경}
# # date = 'yyyymmdd'
# def update_rcPlan(start, end):
#     # start to datetime from string %Y%m%d
#     start = datetime.datetime.strptime(start, '%Y%m%d')
#     end = datetime.datetime.strptime(end, '%Y%m%d')
#     while start <= end:
#         for meet in [1, 2, 3]:
#             try:
#                 start_str = start.strftime('%Y%m%d')
#                 df = get_daily_rcPlan(start_str, meet)

#                 host, user, password, db = tools.get_env('DB')

#                 conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#                 curs = conn.cursor()

#                 # 만약 rcId가 이미 존재한다면 update 하고 없으면 insert
#                 for row in df.iterrows():
#                     sql = f"""
#                     INSERT INTO rcPlan (rcId, ageCond, budam, buga1, buga2, buga3, chaksun1, chaksun2, chaksun3, chaksun4, chaksun5, 
#                                         ilsu, meet, rank, rcDate, rcDist, rcNo, schStTime, sexCond, spRating, stRating) 
#                     VALUES ('{row[1]['rcId']}', '{row[1]['ageCond']}', '{row[1]['budam']}', '{row[1]['buga1']}', '{row[1]['buga2']}', 
#                             '{row[1]['buga3']}', '{row[1]['chaksun1']}', '{row[1]['chaksun2']}', '{row[1]['chaksun3']}', 
#                             '{row[1]['chaksun4']}', '{row[1]['chaksun5']}', '{row[1]['ilsu']}', '{row[1]['meet']}', '{row[1]['rank']}', 
#                             '{row[1]['rcDate']}', '{row[1]['rcDist']}', '{row[1]['rcNo']}', '{row[1]['schStTime']}', '{row[1]['sexCond']}', 
#                             '{row[1]['spRating']}', '{row[1]['stRating']}')
#                     ON DUPLICATE KEY UPDATE
#                         ageCond=VALUES(ageCond), 
#                         budam=VALUES(budam), 
#                         buga1=VALUES(buga1), 
#                         buga2=VALUES(buga2), 
#                         buga3=VALUES(buga3), 
#                         chaksun1=VALUES(chaksun1), 
#                         chaksun2=VALUES(chaksun2), 
#                         chaksun3=VALUES(chaksun3), 
#                         chaksun4=VALUES(chaksun4), 
#                         chaksun5=VALUES(chaksun5), 
#                         ilsu=VALUES(ilsu), 
#                         meet=VALUES(meet), 
#                         rank=VALUES(rank), 
#                         rcDate=VALUES(rcDate), 
#                         rcDist=VALUES(rcDist), 
#                         rcNo=VALUES(rcNo), 
#                         schStTime=VALUES(schStTime), 
#                         sexCond=VALUES(sexCond), 
#                         spRating=VALUES(spRating), 
#                         stRating=VALUES(stRating)
#                     """
#                     curs.execute(sql)

#                 conn.commit()
#                 conn.close()
#             except:
#                 pass
#         start += datetime.timedelta(days=1)
#     return 1
# # def insert_rcResult(start=None, end=None, meet=None):
# #     df = get_period_rcResult(start, end, meet)
# #     # DB에 저장
# #     host, user, password, db = get_env('DB')
# #
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #
# #     curs = conn.cursor()
# #
# #     for row in df.iterrows():
# #         sql = f"INSERT INTO rcResult VALUES ('{row[1]['globalUnique']}', '{row[1]['rcId']}', '{row[1]['age']}', '{row[1]['ageCond']}', '{row[1]['buG1fAccTime']}', '{row[1]['buG1fOrd']}', '{row[1]['buG2fAccTime']}', '{row[1]['buG2fOrd']}', '{row[1]['buG3fAccTime']}', '{row[1]['buG3fOrd']}', '{row[1]['buG4fAccTime']}', '{row[1]['buG4fOrd']}', '{row[1]['buG6fAccTime']}', '{row[1]['buG6fOrd']}', '{row[1]['buG8fAccTime']}', '{row[1]['buG8fOrd']}', '{row[1]['buS1fAccTime']}', '{row[1]['buS1fOrd']}', '{row[1]['buS1fTime']}', '{row[1]['bu_10_8fTime']}', '{row[1]['bu_1fGTime']}', '{row[1]['bu_2fGTime']}', '{row[1]['bu_3fGTime']}', '{row[1]['bu_4_2fTime']}', '{row[1]['bu_6_4fTime']}', '{row[1]['bu_8_6fTime']}', '{row[1]['budam']}', '{row[1]['buga1']}', '{row[1]['buga2']}', '{row[1]['buga3']}', '{row[1]['chaksun1']}', '{row[1]['chaksun2']}', '{row[1]['chaksun3']}', '{row[1]['chaksun4']}', '{row[1]['chaksun5']}', '{row[1]['chulNo']}', '{row[1]['diffUnit']}', '{row[1]['hrName']}', '{row[1]['hrNo']}', '{row[1]['ilsu']}', '{row[1]['jeG1fTime']}', '{row[1]['jeG3fTime']}', '{row[1]['jeS1fTime']}', '{row[1]['je_1cTime']}', '{row[1]['je_2cTime']}', '{row[1]['je_3cTime']}', '{row[1]['je_4cTime']}', '{row[1]['jkName']}', '{row[1]['jkNo']}', '{row[1]['meet']}', '{row[1]['name']}', '{row[1]['ord']}', '{row[1]['owName']}', '{row[1]['owNo']}', '{row[1]['plcOdds']}', '{row[1]['prizeCond']}', '{row[1]['rank']}', '{row[1]['rating']}', '{row[1]['rcDate']}', '{row[1]['rcDay']}', '{row[1]['rcDist']}', '{row[1]['rcNo']}', '{row[1]['rcTime']}', '{row[1]['seG1fAccTime']}', '{row[1]['seG3fAccTime']}', '{row[1]['seS1fAccTime']}', '{row[1]['se_1cAccTime']}', '{row[1]['se_2cAccTime']}', '{row[1]['se_3cAccTime']}', '{row[1]['se_4cAccTime']}', '{row[1]['sex']}', '{row[1]['sjG1fOrd']}', '{row[1]['sjG3fOrd']}', '{row[1]['sjS1fOrd']}', '{row[1]['sj_1cOrd']}', '{row[1]['sj_2cOrd']}', '{row[1]['sj_3cOrd']}', '{row[1]['sj_4cOrd']}', '{row[1]['trName']}', '{row[1]['trNo']}', '{row[1]['track']}', '{row[1]['weather']}', '{row[1]['wgBudam']}', '{row[1]['wgHr']}', '{row[1]['winOdds']}')"
# #         curs.execute(sql)
# #
# #     conn.commit()
# # def update_rcResult(start=None, end=None, meet=None):
# #     df = get_period_rcResult(start, end, meet)
# #
# #     # DB에 저장
# #     host, user, password, db = get_env('DB')
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #     curs = conn.cursor()
# #
# #     for index, row in df.iterrows():
# #         update_values = []
# #         for col in df.columns:
# #             if col != 'globalUnique':  # Skip the primary key column
# #                 value = row[col]
# #                 if pd.isna(value):
# #                     value = 'NULL'
# #                 elif isinstance(value, str):
# #                     value = f"'{value}'"
# #                 else:
# #                     value = str(value)
# #                 update_values.append(f"{col} = {value}")
# #
# #         update_sql = f"UPDATE rcResult SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
# #         curs.execute(update_sql)
# #
# #     conn.commit()
# #     conn.close()
# # def update_modelData(start=None, end=None, meet=None):
# #     just_update_modelData(get_period_modelData(start, end, meet))
# # def insert_modelData(start=None, end=None, meet=None):
# #     df = get_period_modelData(start, end, meet)
# #
# #     # DB에 저장
# #     host, user, password, db = get_env('DB')
# #
# #     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
# #
# #     curs = conn.cursor()
# #
# #     for row in df.iterrows():
# #         sql = f"INSERT INTO model VALUES ('{row[1]['globalUnique']}', '{row[1]['rcId']}', '{row[1]['meet']}', '{row[1]['hrName']}', '{row[1]['age']}', '{row[1]['jkName']}', '{row[1]['weather']}', '{row[1]['wgBudam']}', '{row[1]['rcDate']}', '{row[1]['rcNo']}', '{row[1]['rcDist']}', '{row[1]['rcDate_diff']}', '{row[1]['sex']}' , '{row[1]['avg_past_speed']}', '{row[1]['ord']}', '{row[1]['winOdds']}', '{row[1]['plcOdds']}')"
# #         curs.execute(sql)
# #
# #     conn.commit()

# def update_rcResult(start=None, end=None, meet=None):
#     df = get_period_rcResult(start, end, meet)
#     print(df)
#     # DB에 저장
#     host, user, password, db = tools.get_env('DB')
#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()

#     # 기존 rcResult 테이블의 globalUnique 키 목록 가져오기
#     curs.execute("SELECT globalUnique FROM rcResult")
#     existing_keys = {row[0] for row in curs.fetchall()}

#     for index, row in df.iterrows():
#         if row['globalUnique'] in existing_keys:
#             # 중복되는 행은 업데이트
#             update_values = []
#             for col in df.columns:
#                 if col != 'globalUnique':  # Skip the primary key column
#                     value = row[col]
#                     if pd.isna(value):
#                         value = 'NULL'
#                     elif isinstance(value, str):
#                         value = f"'{value}'"
#                     else:
#                         value = str(value)
#                     update_values.append(f"{col} = {value}")

#             update_sql = f"UPDATE rcResult SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
#             curs.execute(update_sql)
#         else:
#             # 중복되지 않는 행은 삽입
#             insert_values = []
#             for col in df.columns:
#                 value = row[col]
#                 if pd.isna(value):
#                     value = 'NULL'
#                 elif isinstance(value, str):
#                     value = f"'{value}'"
#                 else:
#                     value = str(value)
#                 insert_values.append(value)

#             insert_sql = f"INSERT INTO rcResult ({', '.join(df.columns)}) VALUES ({', '.join(insert_values)})"
#             curs.execute(insert_sql)

#     conn.commit()
#     conn.close()

# def update_modelData(start=None, end=None, meet=None):
#     df = get_period_modelData(start, end, meet)

#     # DB에 저장
#     host, user, password, db = tools.get_env('DB')
#     conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
#     curs = conn.cursor()

#     # 기존 model 테이블의 globalUnique 키 목록 가져오기
#     curs.execute("SELECT globalUnique FROM model")
#     existing_keys = {row[0] for row in curs.fetchall()}

#     for index, row in df.iterrows():
#         if row['globalUnique'] in existing_keys:
#             # 중복되는 행은 업데이트
#             update_values = []
#             for col in df.columns:
#                 if col != 'globalUnique':  # Skip the primary key column
#                     value = row[col]
#                     if pd.isna(value):
#                         value = 'NULL'
#                     elif isinstance(value, str):
#                         value = f"'{value}'"
#                     else:
#                         value = str(value)
#                     update_values.append(f"{col} = {value}")

#             update_sql = f"UPDATE model SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
#             curs.execute(update_sql)
#         else:
#             # 중복되지 않는 행은 삽입
#             insert_values = []
#             for col in df.columns:
#                 value = row[col]
#                 if pd.isna(value):
#                     value = 'NULL'
#                 elif isinstance(value, str):
#                     value = f"'{value}'"
#                 else:
#                     value = str(value)
#                 insert_values.append(value)

#             insert_sql = f"INSERT INTO model ({', '.join(df.columns)}) VALUES ({', '.join(insert_values)})"
#             curs.execute(insert_sql)

#     conn.commit()
#     conn.close()