import os
import pandas as pd
import json


class Reader(object):
    @staticmethod
    def readcsv(source='rates/'):
        df = []
        for rates_file in sorted(os.listdir(source)):
            key, ext = os.path.splitext(rates_file)
            df.append({'name': key, 'rates': pd.read_csv(
                source + rates_file, names=['date', 'rate'])})
        return df

    @staticmethod
    def readjson(source: str) -> list:
        df = []
        for rates_file in sorted(os.listdir(source)):
            key, ext = os.path.splitext(rates_file)
            with open(source + rates_file, 'r') as pf:
                df.append({'name': key, 'rates': json.load(pf)})
        return df
