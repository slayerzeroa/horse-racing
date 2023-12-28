import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def cal_mean_speed(speed_list):
    mean_speed_list = []
    for _ in range(len(speed_list)):
        mean_speed = np.mean(speed_list[:_+1])
        mean_speed_list.append(mean_speed)
    return mean_speed_list

pd.set_option('display.max_columns', None)

df = pd.read_csv('C:/Users/slaye/PycharmProjects/Horse_Racing/data/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')

data = df[['age', 'weather', 'jkName','hrNo', 'wgBudam','rcDate', 'rcNo', 'rcDist', 'rcTime', 'rcDate_diff', 'sex', 'rcTime_mean', 'ord', 'winOdds', 'plcOdds']]
hrNo_list = data.hrNo.unique().tolist()

# for hrNo in hrNo_list:
#     data[data.hrNo == hrNo].sort_values(by=['rcDate']).to_pickle('C:/Users/slaye/PycharmProjects/Horse_Racing/data/horse_records/seoul/' + str(hrNo) + '.pkl')


result = pd.DataFrame()
for hrNo in hrNo_list:
    df = pd.read_pickle('C:/Users/slaye/PycharmProjects/Horse_Racing/data/horse_records/seoul/' + str(hrNo) + '.pkl')
    df['speed'] = df['rcDist'] / df['rcTime']
    df['speed_mean'] = cal_mean_speed(df.speed)
    result = pd.concat([result, df], axis=0)


result.to_csv('C:/Users/slaye/PycharmProjects/Horse_Racing/data/test/seoul_horse_records.csv', index=False)

