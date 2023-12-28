import pandas as pd

section_records = pd.read_csv('../data/section_records/seoul/seoul_section_records.csv')

racing_results = pd.read_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv')

# racing_results.to_csv('../data/racing_results/preprocessed/seoul/seoul_racing_results.csv', index=False)

a = racing_results.merge(section_records, on=['rcDate', 'hrName'], how='left')

a.to_csv('../data/racing_results/preprocessed/seoul/merged_seoul_racing_results.csv', index=False)

#
#
# df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
# df2 = pd.DataFrame([[1, 2, 9], [4, 5, 12], [7, 8, 15]])
#
# df1.columns = ['a', 'b', 'c']
# df2.columns = ['a', 'b', 'd']
#
# print(df1)
# print(df2)
# print(df1.merge(df2, on=['a', 'b'], how='left'))