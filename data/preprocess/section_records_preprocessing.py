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

    part_df['rcTime_std'] = date_df.groupby('hrName')['rcTime'].std()
    part_df['rcTime_mean'] = date_df.groupby('hrName')['rcTime'].mean()
    part_df['rcTime_median'] = date_df.groupby('hrName')['rcTime'].median()
    part_df['rcTime_max'] = date_df.groupby('hrName')['rcTime'].max()
    part_df['rcTime_min'] = date_df.groupby('hrName')['rcTime'].min()

    part_df['rcDate'] = date_df['rcDate'].unique().tolist()[0]

    part_df = part_df.reset_index()
    part_df = part_df.rename(columns={'index': 'hrName'})

    df = pd.concat([df, part_df], axis=0)

    print(df)

# change the column sequence
df = df[['rcDate', 'hrName', 'se_2cAccTime_std', 'se_2cAccTime_mean', 'se_2cAccTime_median', 'se_2cAccTime_max', 'se_2cAccTime_min', 'se_2cAccTime_count', 'se_2cAccTime_sum', 'se_2cAccTime_var', 'se_2cAccTime_skew', 'se_2cAccTime_kurt', 'se_3cAccTime_std', 'se_3cAccTime_mean', 'se_3cAccTime_median', 'se_3cAccTime_max', 'se_3cAccTime_min', 'se_3cAccTime_count', 'se_3cAccTime_sum', 'se_3cAccTime_var', 'se_3cAccTime_skew', 'se_3cAccTime_kurt', 'se_4cAccTime_std', 'se_4cAccTime_mean', 'se_4cAccTime_median', 'se_4cAccTime_max', 'se_4cAccTime_min', 'se_4cAccTime_count', 'se_4cAccTime_sum', 'se_4cAccTime_var', 'se_4cAccTime_skew', 'se_4cAccTime_kurt', 'rcTime_std', 'rcTime_mean', 'rcTime_median', 'rcTime_max', 'rcTime_min', 'rcTime_count', 'rcTime_sum', 'rcTime_var', 'rcTime_skew', 'rcTime_kurt']]
df = df.reset_index(drop=True)

df.to_csv('../data/section_records/seoul/seoul_section_records.csv', index=False, encoding='utf-8-sig')