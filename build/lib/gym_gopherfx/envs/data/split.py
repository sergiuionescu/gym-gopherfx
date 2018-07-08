import pandas as pd

month_file = 'DAT_XLSX_USDJPY_M1_201804.csv'
prefix = 'USDJPY'

df = pd.read_csv(month_file)

split = {}

for index in df.iterrows():
    date = index[1][0]
    rate = index[1][1]

    key_date = pd.to_datetime(date).strftime('%Y%m%d')
    if not key_date in split:
        split[key_date] = []
    split[key_date].append([date, rate])


for key_date in split:
    with open('rates/' + prefix + key_date + ".csv", 'wb') as file:
        for line in split[key_date]:
            file.write(str(line[0]) + ',' + str(line[1]) + '\n')


