from data.preprocess import tools
import requests
import datetime
import pandas as pd

encoding_key, decoding_key = tools.get_env('KRA')

def get_rcPlan(rc_date:str=datetime.datetime.today().strftime('%Y%m%d'), meet:str=None):
    '''
    일별 경기계획
    input: rc_date(경주일자; 20240816), meet(경마장; 1:서울, 2:제주, 3:부산)
    output: DataFrame
    '''
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    params = {'serviceKey': decoding_key, 'pageNo': 1, 'numOfRows': 50, 'rc_date': rc_date, 'meet': meet, '_type': 'json'}
    
    # 통신
    response = requests.get(url, params)
    response_json = response.json()

    if response.status_code == 200:
        print("API Connected!")
    else:
        print(f'error {response.status_code} occurred')
        return -1

    if response_json['response']['body']['totalCount'] == 0:
        print('No data')
        return -1

    
    # 전처리
    rcPlan_df = tools.json2df(response_json)

    # rcId = rcDate + meet + rcNo
    # 시행경마장구분(1:서울 2:제주 3:부산)
    rcPlan_df['rcDate'] = rcPlan_df['rcDate'].astype(str)

    rcPlan_df['meet'] = rcPlan_df['meet'].apply(lambda x: tools.location_to_meet(x))
    rcPlan_df['meet'] = rcPlan_df['meet'].astype(str)

    rcPlan_df['rcNo'] = rcPlan_df['rcNo'].apply(lambda x: tools.preprocess_rcNo(x))
    rcPlan_df['rcNo'] = rcPlan_df['rcNo'].astype(str)

    rcPlan_df['rcId'] = rcPlan_df['rcDate'] + rcPlan_df['meet'] + rcPlan_df['rcNo']

    cols = rcPlan_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    rcPlan_df = rcPlan_df[cols]

    return rcPlan_df


def get_rcResult(rc_date:str, meet:str=None, rc_no:str=None, pageNo:str=1, numOfRows:str=250):
    '''
    경주결과 조회
    '''
    url = "http://apis.data.go.kr/B551015/API4_3/raceResult_3"

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

    # 통신
    response = requests.get(url, params)
    if response.status_code == 200:
        response_json = response.json()
        print("API Connected!")
    else:
        print(f'error {response.status_code} occurred')
        return -1
    
    rcResult_df = tools.json2df(response_json=response_json)

    # 전처리
    # globalUnique = rcDate + meet + rcNo + hrNo
    # rcId = rcDate + meet + rcNo
    # 시행경마장구분(1:서울 2:제주 3:부산)
    rcResult_df['rcDate'] = rcResult_df['rcDate'].astype(str)

    rcResult_df['meet'] = rcResult_df['meet'].apply(lambda x: tools.location_to_meet(x))
    rcResult_df['meet'] = rcResult_df['meet'].astype(str)

    rcResult_df['rcNo'] = rcResult_df['rcNo'].apply(lambda x: tools.preprocess_rcNo(x))
    rcResult_df['rcNo'] = rcResult_df['rcNo'].astype(str)

    rcResult_df['hrNo'] = rcResult_df['hrNo'].astype(str)

    rcResult_df['globalUnique'] = rcResult_df['rcDate'] + rcResult_df['meet'] + rcResult_df['rcNo'] + rcResult_df['hrNo']
    rcResult_df['rcId'] = rcResult_df['rcDate'] + rcResult_df['meet'] + rcResult_df['rcNo']

    # rcName 제거
    rcResult_df = rcResult_df.drop(['rcName'], axis=1)

    cols = rcResult_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    rcResult_df = rcResult_df[cols]
    
    return rcResult_df


def get_rcDate(start:str=None, end:str=None, meet:str=None):
    '''
    경기일자 조회
    '''
    datetime_start = datetime.datetime.strptime(start, '%Y%m%d')
    datetime_end = datetime.datetime.strptime(end, '%Y%m%d')
    
    url = 'http://apis.data.go.kr/B551015/API72_2/racePlan_2'
    
    rcDate_list = []
    while datetime_start <= datetime_end:
        rc_date = datetime_start.strftime('%Y%m%d')
        params = {'serviceKey': decoding_key, 'pageNo': 1, 'numOfRows': 50, 'rc_date': rc_date, 'meet':meet, '_type': 'json'}
        response = requests.get(url, params)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['response']['body']['totalCount'] != 0:
                rcDate_list.append(rc_date)
        datetime_start += datetime.timedelta(days=1)

    return rcDate_list



def get_modelData(rcmodelData_df:pd.DataFrame):
    '''
    modelData는 항상 rcResult가 필요하므로
    Input: DataFrame of rcResult
    Output: DataFrame of modelData
    '''
    hrNo_list = rcmodelData_df['hrNo'].tolist()
    rcmodelData_df = rcmodelData_df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcTime', 'rcDist',  'sex',  'ord', 'winOdds', 'plcOdds']]

    rcDate_diff_list = []
    avg_past_speed_list = []
    for hrNo in hrNo_list:
        aps, rd = get_aps_rd(hrNo, None)
        avg_past_speed_list.append(aps)
        rcDate_diff_list.append(rd)

    rcmodelData_df['rcDate_diff'] = rcDate_diff_list
    rcmodelData_df['avg_past_speed'] = avg_past_speed_list

    rcmodelData_df['rcDate_diff'] = rcmodelData_df['rcDate_diff'].fillna(99999)
    rcmodelData_df['avg_past_speed'] = rcmodelData_df['avg_past_speed'].fillna(-99999)

    rcmodelData_df = rcmodelData_df[['globalUnique', 'rcId', 'meet', 'hrName', 'age', 'jkName', 'weather', 'wgBudam', 'rcDate', 'rcNo', 'rcDist',
             'rcDate_diff', 'sex', 'avg_past_speed', 'ord', 'winOdds', 'plcOdds']]
    rcmodelData_df = rcmodelData_df.sort_values(by=['rcId', 'globalUnique'])
    return rcmodelData_df


def get_hrRecord(hrNo:str, hrName:str=None):

    '''
    240829 현재 500 internal server error 발생
    '''
    result = pd.DataFrame()
    url = 'http://apis.data.go.kr/B551015/API37_1//sectionRecord_1'

    # for문: 한마리 말에 대한 모든 경주기록을 가져옴
    for i in range(1, 5):
        try:
            params = {'serviceKey': decoding_key, 'pageNo': i, 'numOfRows': 50, 'hr_no':hrNo, 'hr_name':hrName, '_type': 'json'}
            params = tools.exclude_none(params)

            # 통신
            response = requests.get(url, params)
            if response.status_code == 200:
                response_json = response.json()
                print("API Connected!")
            else:
                print(f'error {response.status_code} occurred')
                return -1
    
            hrRecord_df = tools.json2df(response_json=response_json)
            print(hrRecord_df)
            result = pd.concat([result, hrRecord_df])
        except:
            break
    # print(result)
    # 말이 첫 경기를 치르는 경우
    if result.empty:
        pass
    else:
        result['speed'] = result['rcDist'] / result['rcTime']
        result['avg_past_speed'] = result['speed'].expanding().mean().shift(1)
        result['rcDate_bin'] = result['rcDate'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())
        result['rcDate_diff'] = result['rcDate_bin'].diff()
        result['rcDate_diff'] = result['rcDate_diff'].apply(lambda x: x.days if isinstance(x, pd.Timedelta) else x)
        result = result.drop(['rcDate_bin'], axis=1)
    return result

print(get_hrRecord('0041600'))

# average past speed, rcDate_diff
def get_aps_rd(hrNo, hrName):
    df = get_hrRecord(hrNo, hrName)
    if df.empty:
        return -99999, 99999
    return df['avg_past_speed'].iloc[-1], df['rcDate_diff'].iloc[-1]


'''
Feature 추가 함수
'''
def cal_rcDate_diff(df):
    '''
    각 말의 이전 경기와의 날짜 차이 계산
    '''
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
    '''
    시간 단위당 이동거리 계산 (속도)
    '''
    df['speed'] = df['rcDist'].astype(int) / df['rcTime'].astype(float)
    return df


def calculate_past_avg_speed(df):
    '''
    마명별 과거 경기의 평균 속도 계산
    '''
    df = cal_speed(df)

    # 경주일자 기준으로 정렬
    df = df.sort_values(by=['hrName', 'rcDate'])

    

    return df

# rcPlan = get_rcPlan(rc_date='20240615')
# print(rcPlan)
# rcDate = get_rcDate(start='20240615', end='20240615', meet='1')
# rcResult1 = get_rcResult(pageNo='1', numOfRows='50', meet=None, rc_date='20240615')
# print(rcResult1)
# modelData1 = get_modelData(rcResult1)
# print(modelData1)