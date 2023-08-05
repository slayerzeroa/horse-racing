import pandas as pd

# Importing the dataset
seoul_dataset = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')
jeju_dataset = pd.read_csv('../data/racing_results/preprocessed/jeju/jeju_racing_results.csv')
busan_dataset = pd.read_csv('../data/racing_results/preprocessed/busan/busan_racing_results.csv')


# 마명 추출
seoul_horse_name = seoul_dataset['hrName'].unique().tolist()
jeju_horse_name = jeju_dataset['hrName'].unique().tolist()
busan_horse_name = busan_dataset['hrName'].unique().tolist()


print(seoul_dataset.groupby('hrName')['seG1fAccTime'].std())
print(jeju_dataset.groupby('hrName')['seG1fAccTime'].std())
print(busan_dataset.groupby('hrName')['seG1fAccTime'].std())