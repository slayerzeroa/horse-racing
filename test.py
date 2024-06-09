import pandas as pd


def cal_speed(df):
    df['speed'] = df['rcDist'] / df['rcTime']
    return df


def calculate_past_avg_speed(df):
    df = cal_speed(df)

    # 경주일자 기준으로 정렬
    df = df.sort_values(by=['hrName', 'rcDate'])

    # 각 말의 이전 경기들의 평균 속도를 계산
    df['avg_past_speed'] = df.groupby('hrName')['speed'].transform(lambda x: x.expanding().mean().shift(1))

    return df


# 예시 데이터프레임
data = {
    'hrName': ['Horse1', 'Horse2', 'Horse1', 'Horse2', 'Horse1'],
    'rcDist': [1000, 1200, 1100, 1300, 1200],
    'rcTime': [60, 70, 66, 78, 72],
    'rcDate': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
}

df = pd.DataFrame(data)

# 평균 속도 계산
result_df = calculate_past_avg_speed(df)
print(result_df)