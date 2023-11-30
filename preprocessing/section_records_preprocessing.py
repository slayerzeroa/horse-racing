import pandas as pd
from date_preprocessing import date_preprocessing

#date_list
file_names = open('../data/file_names/seoul_racing_results_file_names.txt', 'r').read()
date_list = date_preprocessing(file_names)


# Importing the dataset
seoul_dataset = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')
jeju_dataset = pd.read_csv('../data/racing_results/preprocessed/jeju/jeju_racing_results.csv')
busan_dataset = pd.read_csv('../data/racing_results/preprocessed/busan/busan_racing_results.csv')


# 마명 추출
seoul_horse_name = seoul_dataset['hrName'].unique().tolist()
jeju_horse_name = jeju_dataset['hrName'].unique().tolist()
busan_horse_name = busan_dataset['hrName'].unique().tolist()

df = pd.DataFrame()
for idx, i in enumerate(date_list):
    if idx == len(date_list) - 1:
        break

    date_df = seoul_dataset[seoul_dataset['rcDate'] < int(i)].reset_index(drop=True)

    part_df = pd.DataFrame()
    # 경주날짜보다 적은 날짜의 데이터만 추출

    #G1F 통과기록
    part_df['seG1fAccTime_std'] = date_df.groupby('hrName')['seG1fAccTime'].std()
    part_df['seG1fAccTime_mean'] = date_df.groupby('hrName')['seG1fAccTime'].mean()
    part_df['seG1fAccTime_median'] = date_df.groupby('hrName')['seG1fAccTime'].median()
    part_df['seG1fAccTime_max'] = date_df.groupby('hrName')['seG1fAccTime'].max()
    part_df['seG1fAccTime_min'] = date_df.groupby('hrName')['seG1fAccTime'].min()
    part_df['seG1fAccTime_count'] = date_df.groupby('hrName')['seG1fAccTime'].count()
    part_df['seG1fAccTime_sum'] = date_df.groupby('hrName')['seG1fAccTime'].sum()
    part_df['seG1fAccTime_var'] = date_df.groupby('hrName')['seG1fAccTime'].var()
    part_df['seG1fAccTime_skew'] = date_df.groupby('hrName')['seG1fAccTime'].skew()
    part_df['seG1fAccTime_kurt'] = date_df.groupby('hrName')['seG1fAccTime'].apply(pd.DataFrame.kurt)

    part_df['seG3fAccTime_std'] = date_df.groupby('hrName')['seG3fAccTime'].std()
    part_df['seG3fAccTime_mean'] = date_df.groupby('hrName')['seG3fAccTime'].mean()
    part_df['seG3fAccTime_median'] = date_df.groupby('hrName')['seG3fAccTime'].median()
    part_df['seG3fAccTime_max'] = date_df.groupby('hrName')['seG3fAccTime'].max()
    part_df['seG3fAccTime_min'] = date_df.groupby('hrName')['seG3fAccTime'].min()
    part_df['seG3fAccTime_count'] = date_df.groupby('hrName')['seG3fAccTime'].count()
    part_df['seG3fAccTime_sum'] = date_df.groupby('hrName')['seG3fAccTime'].sum()
    part_df['seG3fAccTime_var'] = date_df.groupby('hrName')['seG3fAccTime'].var()
    part_df['seG3fAccTime_skew'] = date_df.groupby('hrName')['seG3fAccTime'].skew()
    part_df['seG3fAccTime_kurt'] = date_df.groupby('hrName')['seG3fAccTime'].apply(pd.DataFrame.kurt)

    part_df['seS1fAccTime_std'] = date_df.groupby('hrName')['seS1fAccTime'].std()
    part_df['seS1fAccTime_mean'] = date_df.groupby('hrName')['seS1fAccTime'].mean()
    part_df['seS1fAccTime_median'] = date_df.groupby('hrName')['seS1fAccTime'].median()
    part_df['seS1fAccTime_max'] = date_df.groupby('hrName')['seS1fAccTime'].max()
    part_df['seS1fAccTime_min'] = date_df.groupby('hrName')['seS1fAccTime'].min()
    part_df['seS1fAccTime_count'] = date_df.groupby('hrName')['seS1fAccTime'].count()
    part_df['seS1fAccTime_sum'] = date_df.groupby('hrName')['seS1fAccTime'].sum()
    part_df['seS1fAccTime_var'] = date_df.groupby('hrName')['seS1fAccTime'].var()
    part_df['seS1fAccTime_skew'] = date_df.groupby('hrName')['seS1fAccTime'].skew()
    part_df['seS1fAccTime_kurt'] = date_df.groupby('hrName')['seS1fAccTime'].apply(pd.DataFrame.kurt)

    part_df['se_1cAccTime_std'] = date_df.groupby('hrName')['se_1cAccTime'].std()
    part_df['se_1cAccTime_mean'] = date_df.groupby('hrName')['se_1cAccTime'].mean()
    part_df['se_1cAccTime_median'] = date_df.groupby('hrName')['se_1cAccTime'].median()
    part_df['se_1cAccTime_max'] = date_df.groupby('hrName')['se_1cAccTime'].max()
    part_df['se_1cAccTime_min'] = date_df.groupby('hrName')['se_1cAccTime'].min()
    part_df['se_1cAccTime_count'] = date_df.groupby('hrName')['se_1cAccTime'].count()
    part_df['se_1cAccTime_sum'] = date_df.groupby('hrName')['se_1cAccTime'].sum()
    part_df['se_1cAccTime_var'] = date_df.groupby('hrName')['se_1cAccTime'].var()
    part_df['se_1cAccTime_skew'] = date_df.groupby('hrName')['se_1cAccTime'].skew()
    part_df['se_1cAccTime_kurt'] = date_df.groupby('hrName')['se_1cAccTime'].apply(pd.DataFrame.kurt)

    part_df['se_2cAccTime_std'] = date_df.groupby('hrName')['se_2cAccTime'].std()
    part_df['se_2cAccTime_mean'] = date_df.groupby('hrName')['se_2cAccTime'].mean()
    part_df['se_2cAccTime_median'] = date_df.groupby('hrName')['se_2cAccTime'].median()
    part_df['se_2cAccTime_max'] = date_df.groupby('hrName')['se_2cAccTime'].max()
    part_df['se_2cAccTime_min'] = date_df.groupby('hrName')['se_2cAccTime'].min()
    part_df['se_2cAccTime_count'] = date_df.groupby('hrName')['se_2cAccTime'].count()
    part_df['se_2cAccTime_sum'] = date_df.groupby('hrName')['se_2cAccTime'].sum()
    part_df['se_2cAccTime_var'] = date_df.groupby('hrName')['se_2cAccTime'].var()
    part_df['se_2cAccTime_skew'] = date_df.groupby('hrName')['se_2cAccTime'].skew()
    part_df['se_2cAccTime_kurt'] = date_df.groupby('hrName')['se_2cAccTime'].apply(pd.DataFrame.kurt)

    part_df['se_3cAccTime_std'] = date_df.groupby('hrName')['se_3cAccTime'].std()
    part_df['se_3cAccTime_mean'] = date_df.groupby('hrName')['se_3cAccTime'].mean()
    part_df['se_3cAccTime_median'] = date_df.groupby('hrName')['se_3cAccTime'].median()
    part_df['se_3cAccTime_max'] = date_df.groupby('hrName')['se_3cAccTime'].max()
    part_df['se_3cAccTime_min'] = date_df.groupby('hrName')['se_3cAccTime'].min()
    part_df['se_3cAccTime_count'] = date_df.groupby('hrName')['se_3cAccTime'].count()
    part_df['se_3cAccTime_sum'] = date_df.groupby('hrName')['se_3cAccTime'].sum()
    part_df['se_3cAccTime_var'] = date_df.groupby('hrName')['se_3cAccTime'].var()
    part_df['se_3cAccTime_skew'] = date_df.groupby('hrName')['se_3cAccTime'].skew()
    part_df['se_3cAccTime_kurt'] = date_df.groupby('hrName')['se_3cAccTime'].apply(pd.DataFrame.kurt)

    part_df['se_4cAccTime_std'] = date_df.groupby('hrName')['se_4cAccTime'].std()
    part_df['se_4cAccTime_mean'] = date_df.groupby('hrName')['se_4cAccTime'].mean()
    part_df['se_4cAccTime_median'] = date_df.groupby('hrName')['se_4cAccTime'].median()
    part_df['se_4cAccTime_max'] = date_df.groupby('hrName')['se_4cAccTime'].max()
    part_df['se_4cAccTime_min'] = date_df.groupby('hrName')['se_4cAccTime'].min()
    part_df['se_4cAccTime_count'] = date_df.groupby('hrName')['se_4cAccTime'].count()
    part_df['se_4cAccTime_sum'] = date_df.groupby('hrName')['se_4cAccTime'].sum()
    part_df['se_4cAccTime_var'] = date_df.groupby('hrName')['se_4cAccTime'].var()
    part_df['se_4cAccTime_skew'] = date_df.groupby('hrName')['se_4cAccTime'].skew()
    part_df['se_4cAccTime_kurt'] = date_df.groupby('hrName')['se_4cAccTime'].apply(pd.DataFrame.kurt)

    part_df['rcTime_std'] = date_df.groupby('hrName')['rcTime'].std()
    part_df['rcTime_mean'] = date_df.groupby('hrName')['rcTime'].mean()
    part_df['rcTime_median'] = date_df.groupby('hrName')['rcTime'].median()
    part_df['rcTime_max'] = date_df.groupby('hrName')['rcTime'].max()
    part_df['rcTime_min'] = date_df.groupby('hrName')['rcTime'].min()
    part_df['rcTime_count'] = date_df.groupby('hrName')['rcTime'].count()
    part_df['rcTime_sum'] = date_df.groupby('hrName')['rcTime'].sum()
    part_df['rcTime_var'] = date_df.groupby('hrName')['rcTime'].var()
    part_df['rcTime_skew'] = date_df.groupby('hrName')['rcTime'].skew()
    part_df['rcTime_kurt'] = date_df.groupby('hrName')['rcTime'].apply(pd.DataFrame.kurt)

    part_df['rcDate'] = date_df['rcDate'].unique().tolist()[0]

    part_df = part_df.reset_index()
    part_df = part_df.rename(columns={'index': 'hrName'})

    df = pd.concat([df, part_df], axis=0)

    print(df)

# change the column sequence
df = df[['rcDate', 'hrName', 'se_2cAccTime_std', 'se_2cAccTime_mean', 'se_2cAccTime_median', 'se_2cAccTime_max', 'se_2cAccTime_min', 'se_2cAccTime_count', 'se_2cAccTime_sum', 'se_2cAccTime_var', 'se_2cAccTime_skew', 'se_2cAccTime_kurt', 'se_3cAccTime_std', 'se_3cAccTime_mean', 'se_3cAccTime_median', 'se_3cAccTime_max', 'se_3cAccTime_min', 'se_3cAccTime_count', 'se_3cAccTime_sum', 'se_3cAccTime_var', 'se_3cAccTime_skew', 'se_3cAccTime_kurt', 'se_4cAccTime_std', 'se_4cAccTime_mean', 'se_4cAccTime_median', 'se_4cAccTime_max', 'se_4cAccTime_min', 'se_4cAccTime_count', 'se_4cAccTime_sum', 'se_4cAccTime_var', 'se_4cAccTime_skew', 'se_4cAccTime_kurt', 'rcTime_std', 'rcTime_mean', 'rcTime_median', 'rcTime_max', 'rcTime_min', 'rcTime_count', 'rcTime_sum', 'rcTime_var', 'rcTime_skew', 'rcTime_kurt']]
df = df.reset_index(drop=True)

df.to_csv('../data/section_records/seoul/seoul_section_records.csv', index=False, encoding='utf-8-sig')