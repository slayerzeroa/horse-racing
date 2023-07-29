import re
import pandas as pd
from io import StringIO

# read file names
file = open('../data/racing_results/raw_text/seoul/seoul_20230722.txt', 'r').read()

file = re.sub(' +', ' ', file)
file = re.sub('\n+', '\n', file)
file = re.sub('-+', '-', file)



file = file.split('-')


TESTDATA = StringIO(file[2])

df = pd.read_csv(TESTDATA, sep=" ", header=None, names=['순위', '마번', '마명', '산지', '성별', '연령', '부담중량', '기수명', '조교사', '마주명', '레이팅'])
df.reset_index(drop=True, inplace=True)
print(df)