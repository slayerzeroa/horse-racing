import pandas as pd

# seoul_dataset = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')
#
#
# seoul_dataset['rcDate'] = seoul_dataset['rcDate'].apply(lambda x: x[:4] + x[5:7] + x[8:])
#
#
# seoul_dataset.to_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv', index=False)


merged_dataset = pd.read_csv('../data/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv')
pd.set_option('display.max_columns', None)
print(merged_dataset.iloc[100:110, :])