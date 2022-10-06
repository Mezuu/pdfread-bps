import os
import re
import pandas as pd


def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


files = sorted_alphanumeric(os.listdir('csv'))

df1 = pd.read_csv('csv/'+files[0])

for i in range(len(files) - 1):
    i += 1
    cols = list(pd.read_csv('csv/'+files[i], nrows=1))
    df2 = pd.read_csv('csv/'+files[i], usecols=[c for c in cols if c != '0'])

    df1 = pd.concat([df1, df2], axis=1)

df1.to_csv('result.csv', index=False, na_rep='')
