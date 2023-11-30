import pandas as pd
from date_preprocessing import date_preprocessing
from datetime import datetime

#date_list
file_names = open('../data/file_names/seoul_racing_results_file_names.txt', 'r').read()
date_list = date_preprocessing(file_names)


# Importing the dataset
seoul_dataset = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')

# 마명 추출
seoul_horse_name = seoul_dataset['hrName'].unique().tolist()



# print(seoul_dataset.columns)
seoul_dataset['rcDate'] = seoul_dataset['rcDate'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').date())

# print(seoul_dataset)

rcDate_diff = pd.DataFrame()
for hrn in seoul_horse_name:
    rcDate_diff = pd.concat([rcDate_diff, seoul_dataset[seoul_dataset['hrName'] == hrn].rcDate.diff()], axis=0)
    # print(rcDate_diff)

rcDate_diff.sort_index(inplace=True)

seoul_dataset['rcDate_diff'] = rcDate_diff
print(seoul_dataset)
print(seoul_dataset['rcDate_diff'])

seoul_dataset.to_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv', index=False)