import pandas as pd

data = pd.read_csv('data/datasets/racing_results/preprocessed/seoul/seoul_racing_results.csv', encoding='utf-8-sig')

pd.set_option('display.max_columns', None)

print(data.columns)
print(f'한국마사회 경주기록 정보 데이터셋의 columns 개수는 {len(data.columns)}개 입니다.')

print(data)